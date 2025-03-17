# AI Personal Assistant

A specialized AI assistant built with OpenAI's GPT and Streamlit, focusing on three domains:
- Human Resources (HR)
- Artificial Intelligence (AI)
- Mathematics

## Features

- Domain-specific expertise in HR, AI, and Mathematics
- Interactive web interface built with Streamlit
- Conversation history tracking
- Contextual responses based on conversation history
- Domain-specific response formatting
- Metadata tracking for each interaction

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hr_ai_math_assistant
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Select a domain (HR, AI, or Mathematics)

4. Enter your question in the text area

5. Click "Get Answer" to receive a response

## Domain Capabilities

### Human Resources (HR)
- Recruitment & Talent Acquisition
- Employee Relations
- Performance Management
- HR Policies & Compliance
- Training & Development

### Artificial Intelligence (AI)
- Machine Learning & Deep Learning
- Natural Language Processing
- Computer Vision
- AI Implementation Strategies
- AI Ethics & Best Practices

### Mathematics
- Pure Mathematics
- Applied Mathematics
- Statistical Analysis
- Mathematical Modeling
- Problem Solving

## Project Structure

```
hr_ai_math_assistant/
├── app.py              # Main Streamlit application
├── agent_handler.py    # Agent logic and OpenAI integration
├── config.py          # Configuration settings
├── requirements.txt   # Python dependencies
└── README.md         # Project documentation
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `DEBUG_MODE`: Enable debug mode (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR, etc.)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this project for any purpose.
