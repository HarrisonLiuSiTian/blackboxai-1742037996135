import os
import sys
import argparse
from agent_handler import MonitoringAgent
from logger import get_logger
import json

logger = get_logger()

def validate_config(config_path: str) -> bool:
    """
    Validate the configuration file
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_fields = [
            'companyName',
            'searchKeywords',
            'websites',
            'pollingInterval',
            'openai_api_key'
        ]
        
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field in config: {field}")
                return False
        
        if not isinstance(config['searchKeywords'], list):
            logger.error("searchKeywords must be a list")
            return False
        
        if not isinstance(config['websites'], dict):
            logger.error("websites must be a dictionary")
            return False
        
        required_websites = [
            'toutiao', 'baidu', 'google', 'douyin', 'xiaohongshu'
        ]
        for site in required_websites:
            if site not in config['websites']:
                logger.error(f"Missing required website in config: {site}")
                return False
        
        if not isinstance(config['pollingInterval'], (int, float)):
            logger.error("pollingInterval must be a number")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Error validating config: {str(e)}")
        return False

def setup_directories():
    """
    Create necessary directories for the application
    """
    directories = ['logs', 'data']
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

def main():
    """
    Main entry point for the monitoring agent
    """
    parser = argparse.ArgumentParser(
        description='Start the company sentiment monitoring agent'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Path to configuration file'
    )
    args = parser.parse_args()

    try:
        # Ensure config file exists
        if not os.path.exists(args.config):
            logger.error(f"Configuration file not found: {args.config}")
            sys.exit(1)

        # Validate configuration
        if not validate_config(args.config):
            logger.error("Invalid configuration")
            sys.exit(1)

        # Setup required directories
        setup_directories()

        # Create and start the monitoring agent
        logger.info("Initializing monitoring agent...")
        agent = MonitoringAgent(args.config)
        
        logger.info(
            f"Starting monitoring for company: "
            f"{agent.config['companyName']}"
        )
        logger.info(
            f"Monitoring keywords: "
            f"{', '.join(agent.config['searchKeywords'])}"
        )
        logger.info(
            f"Polling interval: "
            f"{agent.config['pollingInterval']} minutes"
        )
        
        # Start the agent
        agent.start()

    except KeyboardInterrupt:
        logger.info("Monitoring agent stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
