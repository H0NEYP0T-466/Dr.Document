# 🏥 Dr. Document - AI-Powered GitHub Documentation Generator

An intelligent documentation system that uses multi-agent AI to automatically analyze GitHub repositories and generate comprehensive README files.

## ✨ Features

- 🤖 **Multi-Agent AI System**: 5 specialized AI agents working together
- 📊 **Real-time Progress**: Watch agents work in a beautiful office interface
- 🎨 **Modern Dark UI**: Sleek, professional interface
- 📝 **Comprehensive Analysis**: Deep code analysis and requirement extraction
- ✅ **Quality Control**: Manager approval and final review systems
- 🚀 **LongCat Integration**: Efficient token usage with Flash-Lite models
- 📥 **Export Options**: Copy or download generated README files

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **Multi-Agent Workflow**:
  1. **Code Reader** 👀 - Analyzes code structure, functions, and dependencies
  2. **Requirements Extractor** 📋 - Extracts functional and non-functional requirements
  3. **Manager/Overseer** 👔 - Reviews quality and provides feedback
  4. **README Writer** ✍️ - Generates comprehensive documentation
  5. **Final Reviewer** 🔍 - Validates completeness and accuracy

- **Comprehensive Logging**: Color-coded logs for every operation
- **LLM Integration**: LongCat models with optimized token usage
- **GitHub Integration**: Direct repository cloning and analysis
- **WebSocket Support**: Real-time status updates

### Frontend (React + TypeScript)
- Modern, responsive UI with dark theme
- Real-time agent status visualization
- Live progress tracking
- Markdown preview with syntax highlighting
- Copy and download functionality

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- LongCat API Key

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your LONGCAT_API_KEY
   ```

5. **Run the backend**:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env if you need to change the API URL
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## 🔧 Configuration

### Backend Configuration (backend/.env)

```env
# LongCat API Configuration
LONGCAT_API_KEY=your_longcat_api_key_here

# Optional GitHub Token for private repositories
GITHUB_TOKEN=your_github_token_here
```

### Frontend Configuration (.env)

```env
# Backend API URL
VITE_API_URL=http://localhost:8000
```

## 📖 Usage

1. **Open the application** in your browser
2. **Enter a GitHub repository URL** (e.g., `https://github.com/user/repo`)
3. **Click "Generate Documentation"**
4. **Watch the agents work** in real-time
5. **Review the generated README** and export it

## 🤖 AI Models Used

- **LongCat-Flash-Lite**: Primary model for code analysis and extraction (50M tokens available)
- **LongCat-Flash-Chat**: Content generation and README writing
- **LongCat-Flash-Thinking**: Complex decision-making and reviews

## 📁 Project Structure

```
Dr.Document/
├── backend/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── code_reader.py
│   │   ├── requirements_extractor.py
│   │   ├── manager.py
│   │   ├── readme_writer.py
│   │   └── final_reviewer.py
│   ├── config.py
│   ├── logger.py
│   ├── github_client.py
│   ├── workflow.py
│   ├── main.py
│   └── requirements.txt
├── src/
│   ├── api/
│   │   └── client.ts
│   ├── components/
│   │   ├── RepoInput.tsx
│   │   ├── AgentCard.tsx
│   │   ├── AgentWorkspace.tsx
│   │   └── ResultDisplay.tsx
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
└── package.json
```

## 🔌 API Endpoints

- `POST /api/process-repo` - Start repository processing
- `GET /api/status/{job_id}` - Get job status
- `GET /api/result/{job_id}` - Get completed result
- `WS /ws/{job_id}` - WebSocket for real-time updates
- `GET /health` - Health check

## 🎨 Features in Detail

### Comprehensive Logging
Every operation is logged with:
- 🔵 INFO: General operations
- 🟡 WARNING: Non-critical issues
- 🔴 ERROR: Critical failures
- 🟢 SUCCESS: Completed operations
- 🟣 LLM: AI model interactions

### Quality Control
- Manager reviews analysis quality before README generation
- Final reviewer validates completeness and accuracy
- Iterative refinement with feedback loops

### Real-time Updates
- WebSocket connections for live progress
- Agent status visualization
- Progress bars and status indicators

## 🛠️ Development

### Backend Development

```bash
# Run with auto-reload
cd backend
uvicorn main:app --reload

# View logs
tail -f backend/dr_document.log
```

### Frontend Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Linting

```bash
# Frontend linting
npm run lint
```

## 📝 License

This project is part of the Dr. Document system.

## 🙏 Acknowledgments

- LongCat AI for providing the AI models
- React and FastAPI communities
- Open source contributors

## 🔮 Future Enhancements

- [ ] Support for multiple documentation formats
- [ ] Custom agent configurations
- [ ] Advanced quality metrics
- [ ] Repository comparison features
- [ ] Batch processing capabilities
- [ ] Enhanced code pattern detection
- [ ] Integration with CI/CD pipelines
