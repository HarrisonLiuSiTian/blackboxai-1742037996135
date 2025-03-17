import openai
from typing import Dict, List, Optional
from config import AgentConfig, EnvConfig
import logging
from datetime import datetime

class AssistantAgent:
    def __init__(self, domain: str):
        """
        Initialize the assistant agent for a specific domain.
        
        Args:
            domain (str): The domain of expertise ("HR", "AI", or "Mathematics")
        """
        self.domain = domain
        self.config = AgentConfig.get_domain_config(domain)
        self.system_message = AgentConfig.get_system_message(domain)
        self.conversation_history: List[Dict] = []
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging for the agent."""
        logging.basicConfig(
            level=getattr(logging, EnvConfig.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"{self.domain}Assistant")

    def _maintain_conversation_history(self, user_message: str, assistant_response: str):
        """
        Maintain conversation history within the context window.
        
        Args:
            user_message (str): The user's message
            assistant_response (str): The assistant's response
        """
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response
        })
        
        # Keep only the recent conversations based on context window
        max_history = self.config.get("context_window", 5)
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]

    def _prepare_messages(self, user_query: str) -> List[Dict]:
        """
        Prepare the messages for the OpenAI API, including system message and conversation history.
        
        Args:
            user_query (str): The current user query
            
        Returns:
            List[Dict]: List of messages for the API
        """
        messages = [{"role": "system", "content": self.system_message}]
        
        # Add relevant conversation history
        for conv in self.conversation_history:
            messages.extend([
                {"role": "user", "content": conv["user_message"]},
                {"role": "assistant", "content": conv["assistant_response"]}
            ])
            
        # Add current query
        messages.append({"role": "user", "content": user_query})
        return messages

    def _format_response(self, response_text: str, domain_specific: bool = True) -> str:
        """
        Format the response based on the domain and add any necessary context or formatting.
        
        Args:
            response_text (str): The raw response text
            domain_specific (bool): Whether to add domain-specific formatting
            
        Returns:
            str: Formatted response
        """
        if not domain_specific:
            return response_text

        if self.domain == "Mathematics":
            # Add LaTeX formatting for mathematical expressions
            response_text = response_text.replace('$$', '$')  # Ensure consistent math delimiters
            
        elif self.domain == "HR":
            # Add HR policy disclaimer if needed
            if any(keyword in response_text.lower() for keyword in ['policy', 'regulation', 'law']):
                response_text += "\n\nNote: This advice is general in nature. Please consult with legal professionals for specific situations."
                
        elif self.domain == "AI":
            # Add technical implementation note if needed
            if any(keyword in response_text.lower() for keyword in ['implement', 'deploy', 'build']):
                response_text += "\n\nNote: Implementation details may vary based on your specific technical environment and requirements."

        return response_text

    async def get_response(self, user_query: str) -> Dict:
        """
        Get a response from the assistant for the given query.
        
        Args:
            user_query (str): The user's query
            
        Returns:
            Dict: Response containing the answer and metadata
        """
        try:
            messages = self._prepare_messages(user_query)
            
            response = await openai.ChatCompletion.acreate(
                model=self.config.get("model", "gpt-3.5-turbo"),
                messages=messages,
                temperature=self.config.get("temperature", 0.7),
                max_tokens=self.config.get("max_tokens", 1000)
            )
            
            response_text = response.choices[0].message['content']
            formatted_response = self._format_response(response_text)
            
            # Update conversation history
            self._maintain_conversation_history(user_query, formatted_response)
            
            return {
                "status": "success",
                "response": formatted_response,
                "metadata": {
                    "domain": self.domain,
                    "timestamp": datetime.now().isoformat(),
                    "model": self.config.get("model"),
                    "tokens_used": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting response: {str(e)}")
            return {
                "status": "error",
                "response": f"An error occurred: {str(e)}",
                "metadata": {
                    "domain": self.domain,
                    "timestamp": datetime.now().isoformat(),
                    "error_type": type(e).__name__
                }
            }

    def get_domain_capabilities(self) -> List[str]:
        """
        Get the list of capabilities for the current domain.
        
        Returns:
            List[str]: List of domain capabilities
        """
        return self.config.get("capabilities", [])

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
