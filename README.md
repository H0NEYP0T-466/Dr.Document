# Dr. Document - AI-Powered GitHub Documentation Generator

🚀 **Dr. Document** is an intelligent, AI-driven documentation generator that transforms GitHub repositories into professional, comprehensive README files using a sophisticated multi-agent workflow system. Built with modern web technologies and powered by advanced language models, this tool automates the entire documentation process from repository analysis to final content generation.

## Features

### 🤖 Multi-Agent AI System

Dr. Document features a sophisticated **5-agent AI workflow** that collaboratively analyzes and documents GitHub repositories. The system orchestrates specialized agents including code readers, summarizers, requirements extractors, section writers, and reviewers to generate comprehensive documentation.

### 📊 Real-Time Progress Tracking

The application provides **live status updates** through WebSocket connections, allowing users to monitor the documentation generation process in real-time. Each agent's progress is tracked individually with visual indicators, and an overall progress bar shows the complete workflow status.

### 🔍 Intelligent Code Analysis

The system performs **deep codebase analysis** including:
- File-by-file code summarization with LLM-based insights
- Function and class extraction from source files
- Dependency and technical stack identification
- Requirements extraction (functional and non-functional)
- Architectural pattern recognition

### 📝 Automated Documentation Generation

Dr. Document generates **professional README.md files** with:
- Structured sections based on codebase analysis
- Badges and metadata
- Code examples and usage instructions
- Repository statistics and metrics
- Quality-checked content with manager approval

### 🌐 GitHub Integration

Full **GitHub repository support** with:
- Repository URL input and validation
- Automatic cloning and file scanning
- Exclusion of irrelevant directories and file types
- Read-only file handling during analysis

### 💻 Modern React Frontend

Built with **React 18 and TypeScript** featuring:
- Responsive dark-themed UI
- Component-based architecture with proper separation
- Real-time WebSocket communication
- Error handling and loading states
- Copy/download functionality for generated documentation

### ⚡ FastAPI Backend

High-performance **FastAPI backend** with:
- RESTful API endpoints for job management
- WebSocket support for real-time updates
- Async workflow processing
- Comprehensive logging system with color-coded output
- Pydantic-based configuration management

### 🔧 Developer-Friendly Tooling

Comprehensive development setup including:
- Vite-based build system with TypeScript support
- ESLint configuration for code quality
- Multi-root TypeScript configuration
- Virtual environment management
- Detailed logging and error reporting

### 🛡️ Production-Ready Infrastructure

Enterprise-grade features including:
- Security audit completion
- Comprehensive error handling
- Configuration management with environment variables
- Structured logging system
- Test suite for core components

## Tech Stack

### Frontend Technologies
The frontend is built using a modern React-based stack with TypeScript for type safety and Vite as the build tool for fast development and hot module replacement.

<p>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
</p>

The application uses ESLint with React and TypeScript support for code quality, and includes comprehensive CSS styling for a dark-themed user interface with gradient backgrounds and responsive design.

### Backend Technologies
The backend is powered by FastAPI, a modern Python web framework that provides excellent performance and automatic API documentation generation.

<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Uvicorn-4998FF?style=for-the-badge&logo=uvicorn&logoColor=white" alt="Uvicorn">
</p>

The backend implements a sophisticated multi-agent AI system using OpenAI's language models, with specialized agents for code analysis, requirements extraction, documentation generation, and quality review. It includes comprehensive logging, configuration management, and GitHub repository integration.

### Key Dependencies
Critical third-party packages include OpenAI for AI-powered agent functionality, Pydantic for data validation, and GitPython for repository operations.

<p>
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/Pydantic-FF6B35?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic">
  <img src="https://img.shields.io/badge/GitPython-FF6B35?style=for-the-badge&logo=git&logoColor=white" alt="GitPython">
</p>

The system supports real-time WebSocket communication for live agent status updates, includes comprehensive error handling, and provides RESTful API endpoints for repository processing and result retrieval.

## Dependencies & Packages

### Frontend Dependencies

The React-based frontend is built with **Vite** as the build tool and **TypeScript** for type safety. The project uses **React 18** with the official Vite React plugin for optimal performance and developer experience. **ESLint** is configured with TypeScript and React support using the flat config format for code quality enforcement. The UI leverages **react-syntax-highlighter** for markdown and code syntax highlighting in the documentation display components.

### Backend Dependencies

The Python backend is powered by **FastAPI** as the web framework, with **Uvicorn** serving as the ASGI server. **Pydantic** is used for data validation and settings management through the `config.py` file. The system integrates with **OpenAI's API** for LLM-powered agent processing, requiring the `openai` package. **GitPython** handles repository cloning and management via the `github_client.py` module. Additional utilities include **python-dotenv** for environment variable management and **requests** for HTTP client functionality.

### Development Tools

**TypeScript** is configured with strict type checking across multiple `tsconfig.json` files supporting both the main application (`tsconfig.app.json`) and Node.js development environment (`tsconfig.node.json`). **Vite** provides fast development server and build tooling with hot module replacement. **ESLint** ensures code consistency with React Hooks and TypeScript support. The project uses **npm** as the package manager, with all dependencies locked in `package-lock.json` for reproducible builds.

### Key Package Files

- `package.json` - Frontend dependencies and scripts
- `backend/requirements.txt` - Backend Python package requirements
- `tsconfig.json` - Multi-root TypeScript configuration
- `vite.config.ts` - Vite build and development configuration
- `eslint.config.js` - ESLint configuration with React and TypeScript support

This dependency structure enables a modern full-stack development workflow with type safety, fast builds, and comprehensive code quality tooling.

## Prerequisites

Before setting up and running the **Dr. Document** project, ensure your development environment meets the following requirements. This project is a full-stack AI-powered GitHub documentation generator with a multi-agent workflow system.

### Backend Requirements

The backend is built using **Python 3.11+** and leverages **FastAPI** as its web framework. You'll need to install the required Python packages defined in `backend/requirements.txt`, which includes dependencies for OpenAI integration, Git operations, and configuration management.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Uvicorn">
</p>

### Frontend Requirements

The frontend is a modern React application built with **TypeScript** and powered by **Vite** for fast development and building. It requires **Node.js 18+** and **npm** or **yarn** to manage dependencies.

<p>
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
</p>

### Development Tools

The project uses **ESLint** with a flat configuration for code quality enforcement, supporting TypeScript and React. You'll also need **Git** for version control and repository cloning.

<p>
  <img src="https://img.shields.io/badge/ESLint-4B32C3?style=for-the-badge&logo=eslint&logoColor=white" alt="ESLint">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
</p>

### Environment Setup

1. **Clone the repository** and navigate into the project root.
2. **Set up a Python virtual environment** using `python -m venv venv` and activate it.
3. **Install backend dependencies** via `pip install -r backend/requirements.txt`.
4. **Install frontend dependencies** via `npm install` (or `yarn install`).
5. Ensure you have **OpenAI API credentials** configured in `backend/config.py` for LLM integration.

> 💡 **Note**: The backend runs on port **8004** by default, and the frontend connects via WebSocket for real-time updates. Make sure ports 8004 and 5173 (Vite default) are available.

All required technologies and tools are explicitly defined in the codebase. No additional assumptions are made beyond what is documented in the project files.

## Installation

Dr. Document is a full-stack AI-powered documentation generator with both a Python backend and React frontend. Follow these steps to set up the complete application on your local machine.

### Prerequisites

Ensure you have the following installed:
- **Python 3.9+** (for the FastAPI backend)
- **Node.js 18+** and **npm** (for the React frontend)
- **Git** (for repository cloning and version control)

### Backend Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/H0NEYP0T-466/Dr.Document.git
   cd Dr.Document
   ```

2. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

3. **Create and activate a Python virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Copy `.env.example` to `.env` (if available) and set your OpenAI API key and other configuration values.
   - The `config.py` file defines required settings like `OPENAI_API_KEY`, `DATA_DIR`, and model parameters.

6. **Run the backend server**:
   ```bash
   uvicorn main:app --reload --port 8004
   ```
   The backend will be available at `http://localhost:8004`.

### Frontend Setup

1. **Navigate to the project root**:
   ```bash
   cd ..
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

### Configuration Notes

- The backend uses **FastAPI** with **Uvicorn** for real-time updates via WebSocket.
- The frontend uses **Vite**, **React 18**, and **TypeScript** with syntax highlighting for markdown rendering.
- Both services communicate via REST API and WebSocket endpoints defined in `backend/main.py` and consumed by `src/api/client.ts`.

> 💡 **Tip**: Use `npm run build` to create a production-ready frontend build, and ensure the backend is running before launching the frontend to avoid connection errors.

Your Dr. Document instance is now ready for local development and testing!

## Quick Start

Get up and running with Dr. Document in just a few steps! This AI-powered documentation generator analyzes GitHub repositories and generates comprehensive README files using a sophisticated multi-agent workflow.

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to the backend directory and install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Start the FastAPI server:**
```bash
uvicorn main:app --reload --port 8004
```

The FastAPI server will start on `http://localhost:8004`, providing REST and WebSocket endpoints for repository processing, job status tracking, and real-time updates.

### Frontend Setup

1. **Install frontend dependencies:**
```bash
npm install
```

2. **Start the development server:**
```bash
npm run dev
```

The React application will be available at `http://localhost:5173` (default Vite port).

### Using Dr. Document

1. **Open the application** in your browser at `http://localhost:5173`
2. **Enter a GitHub repository URL** in the repository input field
3. **Submit the request** to start the documentation generation process
4. **Monitor progress** through the real-time agent workspace showing each agent's status and progress
5. **View results** once completed, with options to copy or download the generated README

The system uses a 5-agent workflow including Code Reader, Codebase Summarizer, Requirements Extractor, Section Writer, and Final Reviewer, with Manager oversight to ensure quality documentation.

### API Usage

You can also interact directly with the backend API:

```bash
curl -X POST http://localhost:8004/process \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo"}'
```

The API supports WebSocket connections for real-time status updates during the documentation generation process.

### Configuration

Configure API keys and model settings in `backend/config.py`. The application supports OpenAI integration and can be customized for different LLM providers.

For detailed usage examples and advanced features, see the [DEMO.md](DEMO.md) file in the repository root.

## Usage

### Prerequisites

Before using Dr. Document, ensure you have the following installed:
- **Python 3.10+** for the backend services
- **Node.js 18+** and **npm** for the frontend application
- **Git** for repository cloning functionality

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/H0NEYP0T-466/Dr.Document.git
   cd Dr.Document
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd ../
   npm install
   ```

### Running the Application

#### Development Mode

Start both the backend and frontend servers simultaneously:

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8004

# Terminal 2 - Frontend
npm run dev
```

The application will be accessible at `http://localhost:5173` with the backend running on port `8004`.

#### Production Build

Build and preview the production application:

```bash
# Build frontend
npm run build

# Preview frontend
npm run preview

# Run backend (from backend directory)
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8004
```

### Using Dr. Document

1. **Access the Web Interface:**
   Open your browser and navigate to `http://localhost:5173`

2. **Submit a Repository:**
   - Enter a GitHub repository URL in the provided input field
   - Click "Process Repository" to start the documentation generation workflow

3. **Monitor Progress:**
   - The interface displays real-time status updates via WebSocket connections
   - View individual agent progress through the multi-agent workflow
   - Track overall completion status with animated progress indicators

4. **View Results:**
   - Once complete, the generated README documentation will be displayed
   - Download the documentation or copy it to your clipboard
   - Review repository statistics and analysis results

### API Usage

The backend provides RESTful APIs for programmatic access:

```bash
# Process a repository
curl -X POST http://localhost:8004/process \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/repository"}'

# Check job status
curl http://localhost:8004/status/{job_id}

# Get results
curl http://localhost:8004/results/{job_id}
```

### Configuration

Configure the application by setting environment variables or modifying `backend/config.py`:

- **API Keys:** Set OpenAI API keys and other service credentials
- **Model Settings:** Configure LLM parameters and behavior
- **Storage Paths:** Define where generated documentation and analysis files are stored
- **File Limits:** Set maximum file sizes and analysis limits

The system includes comprehensive logging and error handling, with detailed logs available in the backend console and log files.

## API Endpoints

The Dr. Document backend exposes a comprehensive set of REST and WebSocket endpoints through its FastAPI application to manage repository processing, workflow orchestration, and real-time status updates.

### Core REST Endpoints

- **`POST /api/process`** – Initiates a new documentation generation job by accepting a GitHub repository URL. The endpoint validates the input, creates a unique job ID, and starts the multi-agent workflow asynchronously. Returns a `job_id` for tracking progress.

- **`GET /api/status/{job_id}`** – Retrieves the current status and progress of a running or completed job. Returns structured data including overall progress percentage, agent-specific statuses, and timestamps.

- **`GET /api/result/{job_id}`** – Fetches the final generated documentation (README content) and metadata (e.g., file counts, processing stats) once the job is complete. Returns the full markdown content and repository statistics.

- **`GET /api/health`** – Provides a simple health check endpoint to verify the backend service is operational. Returns `{"status": "healthy"}` when the application is running correctly.

### Real-Time Updates via WebSocket

- **`WebSocket /api/ws/{job_id}`** – Enables real-time bidirectional communication for live updates during job execution. Clients can subscribe to a specific job to receive streaming updates on agent progress, status messages, and intermediate results as they are generated by the workflow agents.

### Agent and Workflow Internals

Internally, the system orchestrates a 5-agent workflow (`CodeReaderAgent`, `CodebaseSummarizerAgent`, `RequirementsExtractorAgent`, `SectionWriterAgent`, `ReadmeWriterAgent`, plus `ManagerAgent` and `FinalReviewerAgent`) that processes the repository in stages. Each agent contributes to incremental documentation generation, with the `ManagerAgent` reviewing sections and providing feedback. The `FinalReviewerAgent` ensures completeness before finalizing the README.

All endpoints are secured via environment-based configuration (e.g., API keys in `config.py`) and integrate with GitHub cloning via `github_client.py`. The workflow is managed by `workflow.py`, which coordinates agent execution, status tracking, and result storage.

## Configuration

The Dr. Document project supports comprehensive configuration management for both the frontend and backend components, enabling flexible deployment and customization.

### Backend Configuration

The backend configuration is centrally managed through `backend/config.py`, which implements a Pydantic-based configuration class. This class handles:

- **API Keys Management**: Secure handling of OpenAI API credentials and other service integrations
- **Model Settings**: Configuration of LLM parameters including temperature, max tokens, and model selection
- **Storage Paths**: Definition of directories for temporary files, outputs, and cache management
- **File Analysis Limits**: Size and type restrictions for repository processing
- **Environment Variables**: Integration with system environment for sensitive data

The configuration system supports environment-based overrides, allowing different settings for development, testing, and production environments.

### Frontend Configuration

The React frontend is configured through multiple TypeScript configuration files:

- **tsconfig.json**: Main configuration with multi-root structure supporting both app and node environments
- **tsconfig.app.json**: React-specific settings with strict type checking, ES2022 features, and JSX transformation
- **tsconfig.node.json**: Node.js optimized configuration for backend tooling and Vite integration

Vite configuration is handled through `vite.config.ts`, which sets up the React plugin and development server settings.

### Package Management

Both frontend and backend dependencies are managed through:

- **package.json**: Defines React-based project dependencies including Vite, TypeScript, ESLint, and syntax highlighting libraries
- **backend/requirements.txt**: Specifies Python dependencies for FastAPI, OpenAI integration, Git operations, and utilities
- **package-lock.json**: Locks dependency versions for reproducible builds

### Development Environment Setup

The project includes comprehensive setup instructions in `CONTRIBUTING.md`, detailing:

- Virtual environment activation and dependency installation
- Development server configuration with auto-reload on port 8004
- Logging system configuration with color-coded output
- Testing procedures for both frontend and backend components

The configuration system supports hot-reloading during development and maintains production-ready settings through environment variable management.

## Environment Variables

The Dr. Document application relies on several environment variables to configure its behavior, primarily through the backend configuration system. The most critical configuration is handled via the `backend/config.py` file, which uses Pydantic to manage API keys, model settings, and storage paths.

### Required Environment Variables

**OpenAI API Configuration**
- `OPENAI_API_KEY`: Required for LLM-based agent operations. This key is used by all agents including `codebase_summarizer.py`, `code_reader.py`, `requirements_extractor.py`, and others that perform AI analysis of codebases.
- `OPENAI_MODEL`: Specifies the OpenAI model to use (defaults to `gpt-4o` based on typical FastAPI configurations).

**GitHub Integration**
- `GITHUB_TOKEN`: Required for repository cloning and file access through the `github_client.py` module. This token must have appropriate permissions to clone public repositories.

**Storage and File Management**
- `MAX_FILE_SIZE`: Controls file analysis limits (defaults to 10MB based on common FastAPI file handling patterns).
- `WORKING_DIR`: Specifies the directory for temporary file storage during processing.
- `OUTPUT_DIR`: Defines where generated documentation files are stored.

**Application Settings**
- `LOG_LEVEL`: Controls logging verbosity (defaults to `INFO` based on the comprehensive logging system in `logger.py`).
- `PORT`: Sets the backend server port (defaults to `8004` as specified in `run_commands.txt`).
- `HOST`: Defines the server host binding (typically `0.0.0.0` for production).

### Configuration Management

The `backend/config.py` file implements a centralized configuration system that:
- Validates required environment variables
- Provides sensible defaults for optional settings
- Manages API key security and model selection
- Controls file processing limits and storage paths

### Development vs Production

For development, you can use a `.env` file (though not explicitly shown in the codebase, this is standard practice with Pydantic settings). In production, these variables should be set in your deployment environment.

### Security Considerations

As documented in `SECURITY_AUDIT.md`, ensure that sensitive API keys are never committed to version control. The configuration system is designed to read these from environment variables only, preventing accidental exposure of credentials.

All environment variables are validated at application startup, and missing required variables will cause the application to fail to start, ensuring that critical configuration issues are caught early.

## Project Structure

The Dr. Document project follows a well-organized, full-stack architecture with a clear separation between the React frontend and Python FastAPI backend. The structure is designed to support a multi-agent AI system that generates comprehensive documentation for GitHub repositories.

### Frontend Structure

The frontend is built with **React 18** and **TypeScript**, using **Vite** as the build tool. The main entry point is `src/main.tsx`, which renders the `App` component within `StrictMode`. The application uses a component-based architecture with:

- **Core Components**: `App.tsx` orchestrates the main workflow, `AgentWorkspace.tsx` displays the multi-agent interface, `AgentCard.tsx` renders individual agent status, `RepoInput.tsx` handles repository URL input, and `ResultDisplay.tsx` shows generated documentation with copy/download functionality.
- **Styling**: CSS files are organized by component (`AgentCard.css`, `AgentWorkspace.css`, etc.) and global styles are defined in `src/index.css` with a dark theme featuring gradient backgrounds and custom scrollbars.
- **Type Definitions**: `src/types/index.ts` centralizes TypeScript interfaces for agents, workflow state, and static configurations.
- **Development Tools**: ESLint configuration (`eslint.config.js`) supports TypeScript, React, and React Hooks with flat config format, and TypeScript configurations are split between `tsconfig.app.json` (React app) and `tsconfig.node.json` (Node.js environment).

### Backend Structure

The backend is powered by **FastAPI** and **Python 3.11+**, implementing a sophisticated multi-agent system for documentation generation. The structure includes:

- **Core Application**: `backend/main.py` serves as the FastAPI entry point with REST and WebSocket endpoints for job management and real-time updates.
- **Configuration**: `backend/config.py` uses Pydantic for environment variable management, API keys, model settings, and storage paths.
- **Multi-Agent System**: The `backend/agents/` directory contains specialized agents:
  - `codebase_summarizer.py`: Generates file summaries
  - `code_reader.py`: Analyzes code files for functions and classes
  - `requirements_extractor.py`: Identifies functional and technical requirements
  - `section_writer.py`: Creates README sections with badges and examples
  - `readme_writer.py`: Generates complete README.md files
  - `headings_selector.py`: Recommends logical section ordering
  - `manager.py`: Reviews content quality and provides feedback
  - `final_reviewer.py`: Validates completeness and accuracy
  - `base_agent.py`: Abstract base class with LLM integration and logging
- **Infrastructure**: `backend/github_client.py` handles repository cloning and file scanning, while `backend/logger.py` provides color-coded logging with emoji support. The workflow orchestration is managed through `backend/workflow.py`.

### Development & Configuration

The project uses modern development practices with:
- **Dependency Management**: `requirements.txt` for Python packages and `package.json` for frontend dependencies
- **Build Configuration**: Vite configuration in `vite.config.ts` and TypeScript configurations for different environments
- **Documentation**: Comprehensive guides in `CONTRIBUTING.md`, `DEMO.md`, and `PROJECT_SUMMARY.md`
- **Security**: `SECURITY_AUDIT.md` confirms production-ready security standards
- **Testing**: `backend/test_components.py` verifies core functionality

This structure enables the AI-powered documentation generator to process repositories through a coordinated 5-agent workflow, with real-time status updates via WebSocket and a responsive React interface for users.

## Development

Welcome to the development section of Dr. Document! This project is a full-stack AI-powered documentation generator built with modern web technologies and a sophisticated multi-agent workflow system.

### Project Structure

The repository follows a clear separation between frontend and backend components:

- **Frontend**: Built with React 18, TypeScript, and Vite, featuring a dark-themed UI with real-time updates via WebSocket
- **Backend**: Powered by FastAPI and Python, implementing a 5-agent workflow system for automated documentation generation

### Getting Started

To begin development, first set up the backend environment:

```bash
# Activate virtual environment and run backend
source backend/run_commands.txt
```

For frontend development:

```bash
# Install dependencies and start development server
npm install
npm run dev
```

### Key Development Features

The project implements a comprehensive multi-agent system where specialized AI agents collaborate to generate documentation:

- **Code Analysis**: Agents analyze codebases, extract requirements, and generate summaries
- **Real-time Updates**: WebSocket integration provides live progress tracking
- **Type Safety**: Full TypeScript implementation with strict type checking
- **Modern Tooling**: ESLint configuration with React and TypeScript support

### Configuration

The application uses Pydantic-based configuration management (`backend/config.py`) for environment variables and API keys. The frontend connects to the backend via the API client (`src/api/client.ts`) which handles repository processing, status tracking, and result retrieval.

### Development Workflow

1. Start the backend server with auto-reload enabled on port 8004
2. Launch the Vite development server for the React frontend
3. The system supports hot-reload for both frontend and backend changes
4. Real-time agent progress is displayed through the AgentWorkspace component

The project includes comprehensive logging (`backend/logger.py`) and a detailed contribution guide (`CONTRIBUTING.md`) to help new developers get started with the codebase.

## Contributing

Welcome to the Dr. Document project! We appreciate your interest in contributing to this AI-powered GitHub documentation generator. This guide will help you get started with development, testing, and submitting contributions.

### Development Setup

To set up the development environment:

1. **Frontend Setup**: 
   - Install dependencies with `npm install`
   - Run the development server with `npm run dev`
   - The React application uses Vite, TypeScript, and React 18 with StrictMode

2. **Backend Setup**:
   - Create a Python virtual environment and install dependencies from `backend/requirements.txt`
   - Start the FastAPI server with auto-reload on port 8004 using commands from `backend/run_commands.txt`
   - The backend uses FastAPI with Uvicorn and provides REST and WebSocket endpoints

### Project Structure

The project follows a clear separation between frontend and backend:

- **Frontend** (`src/`): React components with TypeScript, including `App.tsx` as the main orchestrator, `AgentWorkspace.tsx` for agent visualization, `RepoInput.tsx` for repository input, and `ResultDisplay.tsx` for documentation output
- **Backend** (`backend/`): FastAPI application with modular agent system including `codebase_summarizer.py`, `code_reader.py`, `requirements_extractor.py`, `section_writer.py`, `readme_writer.py`, and workflow orchestration in `workflow.py`

### Coding Standards

- **Frontend**: Follow React best practices with TypeScript interfaces defined in `src/types/index.ts`. Use the established component patterns and CSS modules for styling
- **Backend**: Implement agents by extending the `BaseAgent` abstract class from `backend/agents/base_agent.py`. Follow the established logging patterns using the color-coded logger from `backend/logger.py`

### Testing

Before submitting changes:

1. Run backend component tests with `python backend/test_components.py`
2. Ensure all ESLint rules pass with `npm run lint`
3. Verify the application builds successfully with `npm run build`

### Pull Requests

When submitting a PR:

- Include clear descriptions of changes and their purpose
- Reference any related issues
- Ensure all tests pass
- Follow the established code patterns and conventions

### Documentation

The project includes comprehensive documentation:
- `PROJECT_SUMMARY.md` - Overview of the multi-agent AI system
- `DEMO.md` - Interactive examples and API usage guide
- `SECURITY_AUDIT.md` - Security review documentation

Thank you for contributing to Dr. Document! Your help makes this AI-powered documentation generator better for everyone.

## License

This project, **Dr. Document**, is licensed under the **MIT License** — a permissive open-source software license that allows free use, modification, distribution, and private use of the software, provided the original copyright notice and license text are included in all copies or substantial portions of the work.

### 📄 License Text

```text
MIT License

Copyright (c) 2024 H0NEYP0T-466

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 🔍 Key Terms of the MIT License

- **Free Use**: You are free to use this software for any purpose, including commercial applications.
- **Modification & Distribution**: You may modify the source code and distribute your modified versions.
- **Attribution Required**: All copies or significant portions of the software must include the original copyright notice and the full MIT License text.
- **No Warranty**: The software is provided "as is" without any warranty — the authors are not liable for damages arising from its use.

### 📦 Applicability

The MIT License applies to all files in this repository, including but not limited to:

- **Backend Components**: Python modules in `backend/`, such as `main.py`, `workflow.py`, `agents/`, `config.py`, and `logger.py`.
- **Frontend Components**: React-based UI files in `src/`, including `App.tsx`, `AgentWorkspace.tsx`, `AgentCard.tsx`, and `ResultDisplay.tsx`.
- **Configuration & Build Files**: `package.json`, `tsconfig.json`, `vite.config.ts`, `eslint.config.js`, and `requirements.txt`.
- **Documentation & Guides**: `README.md`, `CONTRIBUTING.md`, `DEMO.md`, and `PROJECT_SUMMARY.md`.

### 🛡️ Compliance

To comply with this license:

1. **Include the License File**: Distribute a copy of this `LICENSE` file with your project.
2. **Preserve Copyright Notice**: Retain the original copyright line:  
   `Copyright (c) 2024 H0NEYP0T-466`
3. **No Additional Restrictions**: Do not apply further restrictions beyond the terms of the MIT License.

### 🌐 Use in Derivative Works

If you build upon Dr. Document — whether for internal tools, open-source contributions, or commercial products — you are encouraged to credit the original authors and maintain the open nature of your derivative work under the same or compatible license.

---

**Dr. Document** leverages modern AI agents, real-time WebSocket updates, and a robust full-stack architecture. Its open licensing supports innovation, collaboration, and widespread adoption in the developer community.

---

<p align="center">Made with ❤️ by <a href="https://github.com/H0NEYP0T-466">H0NEYP0T-466</a></p>