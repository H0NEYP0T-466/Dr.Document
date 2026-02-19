# Contributing to Dr. Document

Thank you for your interest in contributing to Dr. Document! This guide will help you get started.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Git
- LongCat API key (get one from [LongCat](https://longcat.chat))

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/H0NEYP0T-466/Dr.Document.git
   cd Dr.Document
   ```

2. **Backend Setup**:
   ```bash
   ./start-backend.sh
   ```
   
   Or manually:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your LONGCAT_API_KEY
   python3 main.py
   ```

3. **Frontend Setup** (in a new terminal):
   ```bash
   ./start-frontend.sh
   ```
   
   Or manually:
   ```bash
   npm install
   npm run dev
   ```

## 📁 Project Structure

```
Dr.Document/
├── backend/               # Python FastAPI backend
│   ├── agents/           # AI agent implementations
│   │   ├── base_agent.py
│   │   ├── code_reader.py
│   │   ├── requirements_extractor.py
│   │   ├── manager.py
│   │   ├── readme_writer.py
│   │   └── final_reviewer.py
│   ├── config.py         # Configuration management
│   ├── logger.py         # Comprehensive logging system
│   ├── github_client.py  # GitHub integration
│   ├── workflow.py       # Workflow orchestration
│   └── main.py          # FastAPI application
├── src/                  # React frontend
│   ├── api/             # API client
│   ├── components/      # React components
│   ├── types/           # TypeScript types
│   └── App.tsx          # Main application
└── public/              # Static assets
```

## 🎨 Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Comprehensive docstrings for all classes and methods
- Use the logger for ALL operations:
  ```python
  logger.info("Operation description", emoji='START')
  logger.success("Operation completed")
  logger.error("Error occurred", exc_info=True)
  ```

### TypeScript (Frontend)

- Use TypeScript strict mode
- Prefer functional components with hooks
- Use `type` keyword for type-only imports
- Keep components focused and reusable

### Logging Requirements

**Every operation MUST be logged!** This is a core requirement of Dr. Document.

```python
# Log workflow steps
logger.workflow_step("Step Name", "Details")

# Log LLM interactions
logger.llm_input(model, input_data)
logger.llm_call(model, call_details)
logger.llm_output(model, output_data)

# Log agent operations
logger.agent_start(agent_name, task)
logger.agent_complete(agent_name, result)
logger.agent_failed(agent_name, error)

# Log file operations
logger.file_process(filename, action)
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Frontend Tests

```bash
npm test
```

### Manual Testing

1. Start both backend and frontend
2. Enter a test repository URL (e.g., a small public repo)
3. Watch the agent workspace for real-time updates
4. Verify the generated README
5. Check backend logs for comprehensive logging

## 🔧 Development Tips

### Backend Development

- Use `uvicorn main:app --reload` for auto-reload during development
- Check logs in `backend/dr_document.log`
- Test individual agents in isolation:
  ```python
  from backend.agents.code_reader import CodeReaderAgent
  agent = CodeReaderAgent()
  result = agent.run({'file_path': 'test.py', 'file_content': '...'})
  ```

### Frontend Development

- Use React DevTools for debugging
- Check browser console for errors
- Test WebSocket connections in Network tab
- Verify responsive design at different screen sizes

### Adding New Agents

1. Create new agent class inheriting from `BaseAgent`
2. Implement the `process` method
3. Add comprehensive logging
4. Update workflow orchestration
5. Add agent to frontend types
6. Update UI to display the new agent

### Modifying LLM Calls

- Always log inputs, calls, and outputs
- Use appropriate models:
  - `LongCat-Flash-Lite` for simple tasks (most common)
  - `LongCat-Flash-Chat` for content generation
  - `LongCat-Flash-Thinking` for complex decisions
- Handle errors gracefully
- Consider token limits

## 📝 Submitting Changes

### Commit Messages

Use clear, descriptive commit messages:

```
Add feature X to improve Y

- Detail 1
- Detail 2
- Detail 3
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Update documentation
7. Commit your changes
8. Push to your fork
9. Open a Pull Request

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Comprehensive logging added for all operations
- [ ] Tests added/updated (if applicable)
- [ ] Documentation updated
- [ ] No console errors
- [ ] Backend builds without errors
- [ ] Frontend builds without errors
- [ ] Tested manually

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Environment details (OS, Python version, Node version)
7. Backend logs from `backend/dr_document.log`

## 💡 Feature Requests

We welcome feature requests! Please include:

1. Clear description of the feature
2. Use case and benefits
3. Potential implementation approach
4. Any relevant examples

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on what's best for the community

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [LongCat API Documentation](https://longcat.chat)

## ❓ Questions?

If you have questions, feel free to:

- Open an issue for discussion
- Check existing issues and PRs
- Review the main README.md

Thank you for contributing to Dr. Document! 🎉
