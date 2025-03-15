# Company Sentiment Monitoring Agent

An intelligent agent built with OpenAI Agents SDK that monitors company sentiment across multiple Chinese and international platforms.

## Features

- Multi-platform monitoring:
  - Toutiao (今日头条)
  - Baidu (百度)
  - Google
  - Douyin (抖音)
  - Xiaohongshu (小红书)
- Real-time sentiment analysis using OpenAI
- Automated monitoring with configurable intervals
- Trend analysis and alert system
- Comprehensive logging system
- Data persistence and historical analysis
- Asynchronous processing for improved performance

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet access to monitored platforms
- (Optional) Proxy configuration for accessing blocked sites

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd monitoring_agent_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Copy `config.json.example` to `config.json`
   - Update the configuration with your settings:
     - Add your OpenAI API key
     - Set company name and search keywords
     - Configure polling interval
     - (Optional) Add proxy settings

## Configuration

The `config.json` file contains all necessary settings:

```json
{
    "companyName": "Your Company",
    "searchKeywords": ["keyword1", "keyword2"],
    "websites": {
        "toutiao": "https://www.toutiao.com",
        "baidu": "https://www.baidu.com",
        "google": "https://www.google.com",
        "douyin": "https://www.douyin.com",
        "xiaohongshu": "https://www.xiaohongshu.com"
    },
    "pollingInterval": 30,
    "openai_api_key": "your-api-key-here",
    "proxy": {
        "http": "",
        "https": ""
    }
}
```

## Usage

1. Start the monitoring agent:
```bash
python monitor_agent.py
```

Optional arguments:
- `--config`: Specify a custom config file path (default: config.json)

2. Monitor the logs:
- Check `logs/monitor_YYYYMMDD.log` for detailed logging
- Review `data/results_YYYYMMDD_HHMMSS.json` for analysis results

## Project Structure

```
monitoring_agent_project/
├── config.json           # Configuration file
├── monitor_agent.py      # Main entry point
├── agent_handler.py      # Core agent logic
├── analysis.py          # Sentiment analysis
├── scrapers.py          # Web scraping
├── logger.py            # Logging setup
├── requirements.txt     # Dependencies
├── logs/                # Log files
└── data/                # Analysis results
```

## Error Handling

The agent implements comprehensive error handling:
- Automatic retries for failed requests
- Rate limiting protection
- Error logging and reporting
- Graceful degradation when services are unavailable

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 guidelines. Format code using:
```bash
black .
flake8 .
isort .
```

## Security Considerations

- API keys are stored in configuration files
- Proxy support for accessing restricted sites
- Rate limiting to prevent API abuse
- Error handling to prevent data leaks
- Secure storage of monitoring results

## Limitations

- Some platforms may have anti-scraping measures
- API rate limits may affect monitoring frequency
- Proxy configuration may be required for some sites
- Sentiment analysis accuracy depends on OpenAI model

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:
1. Check the documentation
2. Review existing issues
3. Create a new issue with:
   - Detailed description
   - Error messages
   - Configuration (without sensitive data)
   - Steps to reproduce
