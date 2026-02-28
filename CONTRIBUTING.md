# Contributing to H0NEYP0T-466/Dr.Document

🎉 Welcome to **Dr. Document**! Thank you for your interest in contributing to this AI-powered GitHub documentation generator. We're excited to have you join our community of developers working to automate high-quality repository documentation.

Dr. Document is a sophisticated multi-agent system that analyzes codebases and generates comprehensive documentation, including README files, community health files, and more. Your contributions help make open-source projects more discoverable, maintainable, and welcoming to new contributors.

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **Git** (for version control)
- **OpenAI API key** (for LLM functionality)

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Dr.Document.git
   cd Dr.Document
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Frontend**
   ```bash
   npm install
   ```

4. **Configure Environment**
   Create a `.env` file in the `backend` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   LOG_LEVEL=INFO
   ```

5. **Run the Application**
   - Start backend (in one terminal):
     ```bash
     cd backend
     python -m uvicorn main:app --reload --port 8004
     ```
   - Start frontend (in another terminal):
     ```bash
     npm run dev
     ```

---

## 🐛 Reporting Bugs

We appreciate bug reports! To help us resolve issues quickly, please follow these guidelines:

### Before Submitting
- ✅ Search existing issues to avoid duplicates
- ✅ Check the [DEMO.md](DEMO.md) for known limitations
- ✅ Verify your issue isn't related to API keys or environment setup

### Bug Report Template
When creating a new issue, please include:

```markdown
**Description**
A clear and concise description of the bug.

**Steps to Reproduce**
1. Go to...
2. Click on...
3. See error

**Expected Behavior**
What should have happened?

**Actual Behavior**
What actually happened?

**Environment**
- OS: [e.g., macOS 14, Windows 11]
- Python Version: [e.g., 3.11.5]
- Node Version: [e.g., 18.17.0]
- Browser: [e.g., Chrome 120]

**Logs**
Relevant log output (from both frontend console and backend logs)

**Screenshots**
If applicable, add screenshots to help explain the problem.

**Additional Context**
Any other information that might help us understand the issue.
```

---

## 💡 Suggesting Features & Enhancements

We love new ideas! Here's how to propose improvements:

### Feature Request Guidelines
- ✅ Check existing issues/PRs to avoid duplicates
- ✅ Consider whether it aligns with Dr. Document's core mission
- ✅ Provide clear use cases and benefits

### How to Submit
1. Open a new issue with the **"Feature Request"** label
2. Use this template:
   ```markdown
   **Feature Description**
   Clear description of the proposed feature

   **Use Case**
   Why is this needed? Who would benefit?

   **Proposed Implementation**
   (Optional) Any ideas on how it could work

   **Alternatives Considered**
   What other approaches were considered?

   **Additional Context**
   Screenshots, mockups, or related issues
   ```

---

## 🔄 Pull Request Process

We follow GitHub's standard fork-and-pull model. Here's our workflow:

### 1. Fork & Branch
```bash
# Create your feature branch
git checkout -b feat/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Branch Naming Convention
Use one of these prefixes:
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Build process or auxiliary tool changes

### 3. Make Your Changes
- Follow our [Code Style Guidelines](#-code-style-and-quality-expectations)
- Add tests for new functionality
- Update documentation as needed

### 4. Commit Messages
Use conventional commits:
```bash
git commit -m "feat: add new agent for license generation"
git commit -m "fix: resolve websocket connection timeout"
git commit -m "docs: update contributing guidelines"
```

### 5. Push & Create PR
```bash
git push origin feat/your-feature-name
```

### 6. PR Requirements
Your pull request must include:
- ✅ **Clear description** of changes
- ✅ **Related issue reference** (if applicable)
- ✅ **Testing instructions** (how to verify your changes)
- ✅ **Screenshots** (for UI changes)
- ✅ **Breaking changes** clearly documented

Example PR description:
```markdown
## Summary
This PR adds support for generating LICENSE files using the MIT license template.

## Related Issue
Fixes #123

## Changes
- Added `LicenseWriterAgent` class in `backend/agents/license_writer.py`
- Updated workflow to include license generation step
- Added tests in `test_components.py`

## Testing
1. Set up environment with OpenAI API key
2. Run: `python test_components.py`
3. Verify license file is generated correctly

## Screenshots
[Before/After screenshots if applicable]
```

---

## 📝 Code Style and Quality Expectations

We maintain high code quality standards for both frontend and backend components.

### Backend (Python)
- **Style**: Follow [PEP 8](https://pep8.org/) with [Black](https://black.readthedocs.io/) formatting
- **Type Hints**: Required for all function parameters and return values
- **Documentation**: Google-style docstrings for all classes and methods
- **Logging**: Use the existing logger system (`backend/logger.py`)

Example:
```python
class CodeReaderAgent(BaseAgent):
    """Analyzes code files and extracts structural information."""
    
    def process(self, code_content: str, file_path: str) -> dict:
        """Process code content and return analysis results.
        
        Args:
            code_content: The source code to analyze
            file_path: Path to the file being analyzed
            
        Returns:
            Dictionary containing analysis results
        """
        # Implementation here
        pass
```

### Frontend (TypeScript/React)
- **Style**: Use Prettier with ESL