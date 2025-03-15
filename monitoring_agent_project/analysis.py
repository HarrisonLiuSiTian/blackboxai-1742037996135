import openai
from typing import Dict, List, Tuple, Optional
import json
from logger import get_logger
import time

logger = get_logger()

class SentimentAnalyzer:
    def __init__(self, config: dict):
        """Initialize the sentiment analyzer with OpenAI configuration"""
        self.api_key = config['openai_api_key']
        openai.api_key = self.api_key
        self.retries = config.get('retries', 3)
        self.retry_delay = 1  # Initial delay in seconds

    def _call_openai_api(self, text: str) -> Dict:
        """
        Make API call to OpenAI with retry logic and error handling
        """
        for attempt in range(self.retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": """
                        You are a sentiment analysis expert. Analyze the following text and provide:
                        1. Overall sentiment (positive, negative, or neutral)
                        2. Confidence score (0-1)
                        3. Key phrases or topics
                        4. Any potential risks or concerns
                        Format the response as JSON.
                        """},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.3
                )
                
                # Extract the JSON response from the message
                result = json.loads(response.choices[0].message.content)
                return result

            except openai.error.RateLimitError:
                if attempt < self.retries - 1:
                    sleep_time = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limit hit, retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Rate limit error, max retries exceeded")
                    raise

            except openai.error.APIError as e:
                logger.error(f"OpenAI API error: {str(e)}")
                raise

            except json.JSONDecodeError:
                logger.error("Failed to parse OpenAI response as JSON")
                raise

    def analyze_content(self, content: Dict) -> Dict:
        """
        Analyze the sentiment of a single piece of content
        
        Args:
            content (Dict): Dictionary containing content details (title, snippet, etc.)
            
        Returns:
            Dict: Original content enriched with sentiment analysis
        """
        try:
            # Combine title and snippet for analysis
            text_to_analyze = f"{content.get('title', '')} {content.get('snippet', '')}"
            
            # Skip empty content
            if not text_to_analyze.strip():
                logger.warning(f"Empty content received for analysis from {content.get('source')}")
                return content
            
            # Get sentiment analysis
            analysis = self._call_openai_api(text_to_analyze)
            
            # Enrich original content with analysis
            content.update({
                'sentiment_analysis': {
                    'sentiment': analysis.get('sentiment'),
                    'confidence': analysis.get('confidence'),
                    'key_phrases': analysis.get('key_phrases', []),
                    'risks': analysis.get('risks', [])
                }
            })
            
            return content

        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            content['sentiment_analysis'] = {
                'error': str(e),
                'sentiment': 'unknown',
                'confidence': 0.0
            }
            return content

    def analyze_batch(self, contents: List[Dict]) -> List[Dict]:
        """
        Analyze sentiment for a batch of content
        
        Args:
            contents (List[Dict]): List of content items to analyze
            
        Returns:
            List[Dict]: Analyzed content items
        """
        analyzed_contents = []
        for content in contents:
            analyzed_content = self.analyze_content(content)
            analyzed_contents.append(analyzed_content)
        return analyzed_contents

    def get_aggregate_sentiment(self, contents: List[Dict]) -> Dict:
        """
        Calculate aggregate sentiment metrics from a list of analyzed content
        
        Args:
            contents (List[Dict]): List of analyzed content items
            
        Returns:
            Dict: Aggregate metrics including overall sentiment distribution and key risks
        """
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}
        total_confidence = 0
        all_risks = []
        all_phrases = []
        
        for content in contents:
            analysis = content.get('sentiment_analysis', {})
            sentiment = analysis.get('sentiment', 'unknown')
            sentiment_counts[sentiment] += 1
            
            if sentiment != 'unknown':
                total_confidence += analysis.get('confidence', 0)
            
            all_risks.extend(analysis.get('risks', []))
            all_phrases.extend(analysis.get('key_phrases', []))
        
        total_known = sum(sentiment_counts.values()) - sentiment_counts['unknown']
        avg_confidence = total_confidence / total_known if total_known > 0 else 0
        
        return {
            'sentiment_distribution': sentiment_counts,
            'average_confidence': avg_confidence,
            'common_risks': list(set(all_risks)),
            'trending_phrases': list(set(all_phrases)),
            'total_analyzed': len(contents),
            'timestamp': time.time()
        }

    def get_sentiment_trend(self, current: Dict, previous: Optional[Dict] = None) -> Dict:
        """
        Compare current sentiment with previous results to identify trends
        
        Args:
            current (Dict): Current aggregate sentiment metrics
            previous (Dict): Previous aggregate sentiment metrics
            
        Returns:
            Dict: Trend analysis including changes and alerts
        """
        if not previous:
            return {
                'changes': 'First analysis - no trend data available',
                'alerts': []
            }
        
        curr_dist = current['sentiment_distribution']
        prev_dist = previous['sentiment_distribution']
        
        # Calculate changes
        changes = {
            sentiment: curr_dist[sentiment] - prev_dist[sentiment]
            for sentiment in curr_dist.keys()
        }
        
        # Generate alerts
        alerts = []
        if changes['negative'] > 0:
            alerts.append(f"Negative sentiment increased by {changes['negative']}")
        if curr_dist['negative'] > curr_dist['positive']:
            alerts.append("Negative sentiment exceeds positive sentiment")
        
        return {
            'changes': changes,
            'alerts': alerts,
            'timestamp': time.time()
        }
