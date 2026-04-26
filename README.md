# AI Chatbot

A simple AI chatbot application built with Streamlit, LangChain, and OpenAI's GPT-4o model. This app provides an interactive chat interface where users can converse with an AI assistant that maintains conversation history.

## Features

- Interactive chat interface using Streamlit
- Conversation memory with chat history
- Powered by OpenAI's GPT-4o model
- Sidebar with options to clear chat history
- Responsive design with centered layout

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-chatbot
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Create a `.env` file in the `src/ai_chatbot/` directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Activate the Poetry shell:
   ```bash
   poetry shell
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run src/ai_chatbot/app.py
   ```

3. Open your browser to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Start chatting with the AI assistant!

## Configuration (configurable in `constants.py`)

- **Model**: GPT-4o 
- **Temperature**: 0.7 (controls response randomness)
- **System Prompt**: "You are a helpful AI assistant." (customizable)

## Testing

Run the unit tests using Poetry:
```bash
PYTHONPATH=src/ai_chatbot poetry run pytest
```

## Project Structure

```
ai-chatbot/
├── src/
│   └── ai_chatbot/
│       ├── __init__.py
│       ├── constants.py
│       └── app.py          # Main application file
├── tests/
│   ├── __init__.py
│   └── test_app.py         # Unit tests
├── pyproject.toml          # Poetry configuration
├── README.md               # This file
└── .env                    # Environment variables (create this)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests to ensure everything works
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 