import os
from typing import Dict, List

class AgentConfig:
    # Domain-specific configurations
    DOMAIN_CONFIGS: Dict[str, Dict] = {
        "HR": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 1000,
            "capabilities": [
                "Recruitment & Talent Acquisition",
                "Employee Relations",
                "Performance Management",
                "HR Policies & Compliance",
                "Training & Development"
            ],
            "context_window": 5  # Number of previous exchanges to maintain context
        },
        "AI": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.8,
            "max_tokens": 1200,
            "capabilities": [
                "Machine Learning & Deep Learning",
                "Natural Language Processing",
                "Computer Vision",
                "AI Implementation Strategies",
                "AI Ethics & Best Practices"
            ],
            "context_window": 4
        },
        "Mathematics": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.5,  # Lower temperature for more precise math responses
            "max_tokens": 1000,
            "capabilities": [
                "Pure Mathematics",
                "Applied Mathematics",
                "Statistical Analysis",
                "Mathematical Modeling",
                "Problem Solving"
            ],
            "context_window": 3
        }
    }

    # System messages for each domain
    SYSTEM_MESSAGES: Dict[str, str] = {
        "HR": """You are an expert HR consultant with deep knowledge in:
            - Talent acquisition and recruitment strategies
            - Employee engagement and retention
            - Performance evaluation and management
            - HR policy development and compliance
            - Training program development
            Provide detailed, practical advice while considering industry best practices and regulations.""",
        
        "AI": """You are an AI technology expert specializing in:
            - Machine learning model development and deployment
            - Natural language processing applications
            - Computer vision solutions
            - AI system architecture and implementation
            - Ethical AI considerations
            Provide technical guidance while considering practical implementation challenges.""",
        
        "Mathematics": """You are a mathematics expert proficient in:
            - Advanced mathematical concepts and proofs
            - Statistical analysis and probability
            - Mathematical modeling and optimization
            - Numerical methods and algorithms
            - Problem-solving strategies
            Provide clear, step-by-step explanations and solutions."""
    }

    @staticmethod
    def get_domain_config(domain: str) -> Dict:
        """Retrieve configuration for a specific domain."""
        return AgentConfig.DOMAIN_CONFIGS.get(domain, {})

    @staticmethod
    def get_system_message(domain: str) -> str:
        """Retrieve system message for a specific domain."""
        return AgentConfig.SYSTEM_MESSAGES.get(domain, "")

    @staticmethod
    def get_capabilities(domain: str) -> List[str]:
        """Retrieve capabilities for a specific domain."""
        config = AgentConfig.get_domain_config(domain)
        return config.get("capabilities", [])

# Environment variables
class EnvConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Application settings
class AppConfig:
    APP_NAME = "AI Personal Assistant"
    VERSION = "1.0.0"
    DESCRIPTION = "Specialized assistant for HR, AI Applications, and Mathematics"
    SUPPORTED_DOMAINS = ["HR", "AI", "Mathematics"]
    MAX_QUERY_LENGTH = 1000
    DEFAULT_DOMAIN = "HR"
