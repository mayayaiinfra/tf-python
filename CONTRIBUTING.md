# Contributing to THUNDERFIRE Python SDK

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone: `git clone https://github.com/YOUR_USERNAME/tf-python.git`
3. Install dev dependencies: `pip install -e .[dev]`
4. Create a branch: `git checkout -b feature/your-feature`
5. Make changes
6. Run tests: `pytest`
7. Commit and push
8. Open a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install with all extras
pip install -e .[all,dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=thunderfire --cov-report=html
```

## Code Style

- Use type hints
- Follow PEP 8
- Add docstrings (Google style)
- Run `ruff check` before committing

## Framework Integrations

When adding or modifying framework integrations:

- **LangChain**: Tools in `src/thunderfire/langchain/`
- **CrewAI**: Tools in `src/thunderfire/crewai/`
- **AutoGen**: Tools in `src/thunderfire/autogen/`
- **OpenAI**: Functions in `src/thunderfire/openai/`
- **MCP**: Server in `src/thunderfire/mcp/`

## Testing

- Add tests for new functionality
- Use `pytest-asyncio` for async tests
- Mock external API calls with `respx`

## Questions?

Open an issue or discussion on GitHub.
