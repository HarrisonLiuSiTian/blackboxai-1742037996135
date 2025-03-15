import time
import json
from typing import Dict, List, Optional
import asyncio
from datetime import datetime
import os

from logger import get_logger
from scrapers import create_scrapers
from analysis import SentimentAnalyzer

logger = get_logger()

class MonitoringAgent:
    def __init__(self, config_path: str = "config.json"):
        """Initialize the monitoring agent with configuration"""
        self.config = self._load_config(config_path)
        self.scrapers = create_scrapers(self.config)
        self.analyzer = SentimentAnalyzer(self.config)
        self.last_results = None
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise

    async def _scrape_website(self, source: str, scraper, keyword: str) -> List[Dict]:
        """Scrape a single website asynchronously"""
        try:
            logger.info(f"Starting scraping for {source} with keyword: {keyword}")
            results = await asyncio.get_event_loop().run_in_executor(
                None, scraper.search, keyword
            )
            logger.info(f"Found {len(results)} results from {source}")
            return results
        except Exception as e:
            logger.error(f"Error scraping {source}: {str(e)}")
            return []

    async def gather_data(self) -> List[Dict]:
        """Gather data from all sources asynchronously"""
        all_results = []
        tasks = []

        for keyword in self.config['searchKeywords']:
            for source, scraper in self.scrapers.items():
                task = self._scrape_website(source, scraper, keyword)
                tasks.append(task)

        # Gather all results
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                all_results.extend(result)
            else:
                logger.error(f"Error in scraping task: {str(result)}")

        return all_results

    def analyze_data(self, results: List[Dict]) -> Dict:
        """Analyze gathered data"""
        try:
            # Perform sentiment analysis on all results
            analyzed_results = self.analyzer.analyze_batch(results)
            
            # Get aggregate metrics
            aggregate_metrics = self.analyzer.get_aggregate_sentiment(analyzed_results)
            
            # Get trend analysis
            trend_analysis = self.analyzer.get_sentiment_trend(
                aggregate_metrics,
                self.last_results
            )
            
            # Update last results for future trend analysis
            self.last_results = aggregate_metrics
            
            return {
                'results': analyzed_results,
                'aggregate_metrics': aggregate_metrics,
                'trend_analysis': trend_analysis,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            return {
                'error': str(e),
                'timestamp': time.time()
            }

    def save_results(self, analysis_results: Dict):
        """Save analysis results to file"""
        try:
            timestamp = datetime.fromtimestamp(analysis_results['timestamp'])
            filename = f"results_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to {filepath}")
            
            # Keep only the last 100 result files
            self._cleanup_old_results()
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

    def _cleanup_old_results(self, keep_last: int = 100):
        """Clean up old result files, keeping only the specified number of most recent files"""
        try:
            files = sorted([
                os.path.join(self.data_dir, f)
                for f in os.listdir(self.data_dir)
                if f.startswith('results_') and f.endswith('.json')
            ])
            
            if len(files) > keep_last:
                for file in files[:-keep_last]:
                    os.remove(file)
                logger.info(f"Cleaned up {len(files) - keep_last} old result files")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    def get_latest_results(self) -> Optional[Dict]:
        """Get the most recent analysis results"""
        try:
            files = sorted([
                f for f in os.listdir(self.data_dir)
                if f.startswith('results_') and f.endswith('.json')
            ])
            
            if not files:
                return None
            
            latest_file = os.path.join(self.data_dir, files[-1])
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading latest results: {str(e)}")
            return None

    async def monitor_cycle(self):
        """Run one complete monitoring cycle"""
        try:
            # Gather data from all sources
            results = await self.gather_data()
            
            if not results:
                logger.warning("No results gathered in this cycle")
                return
            
            # Analyze gathered data
            analysis_results = self.analyze_data(results)
            
            # Save results
            self.save_results(analysis_results)
            
            # Check for alerts
            if analysis_results.get('trend_analysis', {}).get('alerts'):
                logger.warning(
                    "Alerts detected: " + 
                    str(analysis_results['trend_analysis']['alerts'])
                )
            
            return analysis_results
        except Exception as e:
            logger.error(f"Error in monitoring cycle: {str(e)}")
            return None

    async def run(self):
        """Run the monitoring agent continuously"""
        logger.info("Starting monitoring agent")
        while True:
            try:
                await self.monitor_cycle()
                # Wait for the configured interval
                await asyncio.sleep(self.config['pollingInterval'] * 60)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                # Wait a short time before retrying
                await asyncio.sleep(60)

    def start(self):
        """Start the monitoring agent"""
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.run())
        except KeyboardInterrupt:
            logger.info("Monitoring agent stopped by user")
        except Exception as e:
            logger.error(f"Monitoring agent stopped due to error: {str(e)}")
        finally:
            loop.close()
