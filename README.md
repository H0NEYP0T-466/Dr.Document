# H0NEYP0T-466/Dr.Document

# Dr. Document README Sections

Dr. Document is a sophisticated AI-powered GitHub documentation generator featuring a complete 5-agent workflow system that automatically analyzes repositories and generates comprehensive, professional README files. The project consists of a robust backend built with FastAPI and Python, and a modern React frontend with TypeScript, providing real-time progress tracking and interactive documentation generation.

## Key Highlights

Dr. Document is a sophisticated AI-powered GitHub documentation generator featuring a robust multi-agent workflow system that automates the creation of comprehensive README files for software repositories. The application is built with a modern full-stack architecture combining a React frontend with TypeScript and a Python FastAPI backend, providing both real-time user interaction and powerful AI-driven processing capabilities.

The system implements a **five-agent workflow architecture** that orchestrates specialized AI agents to analyze repositories and generate professional documentation. The workflow begins with the **Codebase Summarizer Agent**, which generates concise summaries for each file in the codebase, followed by the **Code Reader Agent** that extracts functions, classes, and dependencies from code files. The **Requirements Extractor Agent** identifies functional and non-functional requirements, while the **Headings Selector Agent** determines the most relevant documentation sections based on codebase analysis. Finally, the **Readme Writer Agent** synthesizes all collected information into a structured, well-formatted README.md file with proper badges and examples.

The backend is built on **FastAPI** with **Uvicorn** serving, providing asynchronous processing capabilities and WebSocket support for real-time progress tracking. The system integrates with **OpenAI's language models** through a standardized agent interface, enabling sophisticated natural language processing and code analysis. Configuration is managed through a **Pydantic-based system** that supports environment variables and type-safe settings for API keys, model parameters, and storage paths.

The frontend provides an intuitive interface built with **React and TypeScript**, featuring a dark theme with gradient backgrounds and smooth animations. Users can input GitHub repository URLs through a dedicated form component, and the system displays real-time progress updates via WebSocket connections. The interface includes comprehensive status indicators, progress bars, and a final results display with syntax-highlighted markdown preview and export functionality.

The application includes **comprehensive logging capabilities** with color-coded output, emoji support, and both console and file logging options. Security is addressed through a completed security audit that confirms all vulnerabilities have been resolved. The project follows strict development standards with ESLint configuration, TypeScript strict mode, and detailed contribution guidelines.

Key technical features include **WebSocket-based real-time updates**, **responsive design with modern CSS styling**, **dependency management through package.json and requirements.txt**, and **modular agent architecture** that can be easily extended or modified. The system supports file size limits, handles various code file types, and provides robust error handling throughout the documentation generation process.

## Features

### 🤖 AI-Powered Multi-Agent Documentation Generation
Dr. Document leverages a sophisticated **5-agent AI workflow** to automatically analyze and document GitHub repositories. The system orchestrates specialized agents including codebase summarizer, requirements extractor, section writer, headings selector, and final reviewer to generate comprehensive documentation.

### 🔄 Real-Time Progress Tracking
Built with **WebSocket support**, the application provides live updates during the documentation generation process. Users can monitor agent status, progress bars, and receive real-time notifications as each agent completes its tasks, creating an engaging and transparent workflow experience.

### 📊 Interactive Dashboard Interface
The frontend features a modern React-based dashboard with **AgentWorkspace** displaying a grid of agent cards showing individual progress, status indicators, and completion metrics. The interface uses gradient designs, hover effects, and responsive layouts for an intuitive user experience.

### 🔗 GitHub Repository Integration
Users can input GitHub repository URLs through a dedicated **RepoInput component** that validates URLs and initiates the documentation generation process. The backend includes a robust GitHub client that clones repositories and scans for relevant code files while excluding unnecessary directories.

### 📝 Comprehensive README Generation
The system generates professional **README.md files** with structured sections, badges, code examples, and detailed explanations. Each section is written by specialized agents and reviewed for quality, ensuring accurate and useful documentation that matches the codebase structure.

### 🛠️ Advanced Code Analysis
Multiple agents perform deep code analysis including **function extraction, class identification, dependency mapping, and architectural pattern recognition**. The code reader agent analyzes individual files while the requirements extractor identifies functional and technical requirements.

### ⚡ High-Performance Backend
Built with **FastAPI and Uvicorn**, the backend provides asynchronous processing with auto-reload capabilities on port 8004. The system handles multiple concurrent requests efficiently while maintaining real-time communication through WebSocket connections.

### 🔒 Secure Configuration Management
The application uses **Pydantic-based configuration** with environment variable support for managing API keys, model settings, and storage paths. A comprehensive security audit confirms all vulnerabilities have been resolved for production readiness.

### 📱 Responsive Design
The frontend is built with **Vite, React, and TypeScript** featuring dark themes, custom scrollbars, and modern CSS styling. The interface adapts seamlessly across devices with gradient backgrounds and smooth animations.

### 🔄 Workflow Orchestration
The **workflow.py** module coordinates the multi-agent process, managing repository cloning, agent execution, and result aggregation. Each agent follows a standardized interface while providing specialized functionality for comprehensive documentation generation.

## Tech Stack

### Backend Technologies

The backend is built with a modern Python stack featuring **FastAPI** as the web framework, providing high-performance API endpoints and automatic OpenAPI documentation. The application uses **Uvicorn** as the ASGI server to run the FastAPI application with WebSocket support and auto-reload capabilities. For AI integration, the backend leverages **OpenAI's GPT models** through their official Python SDK, enabling sophisticated natural language processing and code analysis capabilities.

The backend architecture follows a modular design with a comprehensive agent system built on an abstract `BaseAgent` class that provides standardized LLM integration, logging, and workflow management. Key agents include `CodebaseSummarizerAgent`, `HeadingsSelectorAgent`, `SectionWriterAgent`, `RequirementsExtractorAgent`, and specialized agents like `ManagerAgent` and `FinalReviewerAgent` that work together in a coordinated workflow to generate comprehensive documentation.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Uvicorn-438EE4?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Uvicorn">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
</p>

### Frontend Technologies

The frontend is a modern React application built with **TypeScript** for type safety and better developer experience. The project uses **Vite** as the build tool, configured through `vite.config.ts`, providing fast development server and optimized production builds. The UI components are built using React functional components with hooks for state management, featuring real-time updates through WebSocket connections to the backend.

The application implements a sophisticated multi-agent dashboard with components like `AgentWorkspace`, `AgentCard`, `RepoInput`, and `ResultDisplay` that provide interactive progress tracking and documentation preview capabilities. The styling is implemented with custom CSS featuring dark themes, gradient backgrounds, and smooth animations for a modern user experience.

<p>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white" alt="WebSocket">
</p>

### Development & Tooling

The project uses **ESLint** for code quality enforcement with React-specific rules and **TypeScript** configurations for both frontend (`tsconfig.app.json`) and backend (`tsconfig.node.json`) environments. The development workflow is supported by comprehensive configuration files including `package.json` for frontend dependencies, `requirements.txt` for Python packages, and various configuration files for TypeScript, ESLint, and Vite.

The project structure includes proper separation of concerns with distinct directories for backend agents, frontend components, API clients, and type definitions, all managed through a workspace-based TypeScript configuration system.

<p>
  <img src="https://img.shields.io/badge/ESLint-4B32C3?style=for-the-badge&logo=eslint&logoColor=white" alt="ESLint">
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown">
</p>

## Dependencies & Packages

Dr. Document is built using a modern full-stack architecture with carefully selected dependencies for both frontend and backend functionality. The project uses **Vite** as the build tool for the React-based frontend, with **TypeScript** providing strict type safety across all client-side code. For code quality assurance, the project leverages **ESLint** configured with React Hooks and React Refresh plugins, ensuring consistent coding standards and preventing common React anti-patterns.

The frontend relies on core React dependencies including `react`, `react-dom`, and `react-router-dom` for navigation. For rendering and displaying generated documentation, the application uses `react-markdown` and `react-syntax-highlighter` to provide rich markdown preview with syntax highlighting capabilities. The UI components are styled using standard CSS with custom styling for dark themes, gradient backgrounds, and interactive elements.

The backend is powered by **FastAPI**, a modern Python web framework that provides high-performance API endpoints and automatic OpenAPI documentation. **Uvicorn** serves as the ASGI server for running the FastAPI application with WebSocket support for real-time updates. The backend integrates with **OpenAI's GPT models** through the official `openai` Python client for AI-powered code analysis and documentation generation.

For configuration management, the project uses **Pydantic** to define structured configuration classes with environment variable support, ensuring type-safe settings management. **aiofiles** enables asynchronous file operations during repository cloning and processing, while **GitPython** provides comprehensive Git repository interaction capabilities. The logging system utilizes standard Python `logging` with custom formatting and color-coded output.

The multi-agent workflow system relies on several specialized agents including code summarization, requirements extraction, section writing, and final review capabilities. These agents are orchestrated through an asynchronous workflow system that coordinates the entire documentation generation process. The backend also includes WebSocket support for real-time progress tracking between the frontend and backend components.

All dependencies are carefully version-locked in `package-lock.json` and `requirements.txt` to ensure reproducible builds and consistent development environments across the team.

## Prerequisites

Before setting up and running the Dr. Document project, ensure your development environment meets the following requirements:

### Core Technologies

The project is built using a modern full-stack architecture with the following primary technologies:

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
</p>

### Backend Requirements

The backend requires Python 3.9+ and uses several key dependencies:

- **OpenAI API integration** for LLM-powered agent workflows
- **WebSocket support** for real-time progress tracking
- **GitHub repository cloning** capabilities
- **FastAPI framework** with Uvicorn server

Install backend dependencies using:
```bash
pip install -r backend/requirements.txt
```

It's strongly recommended to use a virtual environment before installing packages.

### Frontend Requirements

The frontend requires Node.js 16+ and uses:

- **React 18** with TypeScript support
- **Vite** as the build tool
- **ESLint** for code quality
- **Markdown rendering** and syntax highlighting

Install frontend dependencies using:
```bash
npm install
```

### API Keys & Authentication

The application requires the following credentials to function properly:

- **OpenAI API Key**: Required for all LLM-based agent operations including code analysis, summarization, and documentation generation
- **GitHub Personal Access Token**: Required for repository cloning operations to avoid rate limits and enable private repository access

These credentials should be configured in the backend's configuration system, typically through environment variables as defined in `backend/config.py`.

### Development Setup

The project consists of two separate applications that must be run independently:

1. **Backend Service**: FastAPI application running on port 8004 with auto-reload
2. **Frontend Application**: React application served by Vite development server

Both applications must be started separately after installing their respective dependencies.

## Installation

Follow these steps to set up and run the Dr. Document AI-powered GitHub documentation generator locally:

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.9+** (for backend services)
- **Node.js 18+** (for frontend development and build tools)
- **npm** or **yarn** (package manager for frontend dependencies)
- **Git** (to clone repositories and manage version control)

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

3. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   Create a `.env` file in the `backend` directory with the following content (adjust values as needed):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   LOG_LEVEL=INFO
   PORT=8004
   ```

6. **Start the FastAPI backend server**:
   ```bash
   uvicorn main:app --reload --port 8004
   ```
   The backend will be accessible at `http://localhost:8004`.

### Frontend Setup

1. **Navigate to the project root** (if still in `backend`):
   ```bash
   cd ..
   ```

2. **Install frontend dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`.

### Configuration Files

The project uses several configuration files:
- `backend/config.py`: Manages API keys, model settings, and storage paths via environment variables
- `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`: TypeScript configurations for frontend and backend
- `vite.config.ts`: Vite build configuration with React plugin
- `eslint.config.js`: ESLint rules for TypeScript and React with React Refresh support

### Running the Full Application

Once both services are running:
1. Open your browser to `http://localhost:5173`
2. Use the repository input form to submit a GitHub URL
3. Monitor real-time agent progress via WebSocket connections
4. View generated documentation in the result display panel

### Development Notes

- The backend uses **FastAPI** with **Uvicorn** for real-time WebSocket communication
- Frontend built with **React**, **TypeScript**, and **Vite**
- Multi-agent workflow includes: codebase summarizer, requirements extractor, headings selector, section writer, and final reviewer
- All components support hot-reload during development
- Comprehensive logging system with color-coded output for debugging

For detailed contribution guidelines and testing procedures, refer to `CONTRIBUTING.md`.

## Quick Start

Welcome to **Dr. Document** — an AI-powered GitHub documentation generator that automates the creation of comprehensive README files using a sophisticated 5-agent workflow system. This Quick Start guide will help you get the application running locally in just a few steps.

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **npm** (comes with Node.js)

### 1. Clone the Repository

```bash
git clone https://github.com/H0NEYP0T-466/Dr.Document.git
cd Dr.Document
```

### 2. Set Up the Backend

Navigate to the `backend` directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Configure your environment variables by creating a `.env` file (refer to `config.py` for required keys like `OPENAI_API_KEY`).

Start the FastAPI server with auto-reload:

```bash
python run_commands.txt
```

This launches the backend on **port 8004** with WebSocket support for real-time updates.

### 3. Set Up the Frontend

In a new terminal, navigate to the project root and install frontend dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (default Vite port).

### 4. Use the Application

1. Open your browser and go to `http://localhost:5173`
2. Enter a valid GitHub repository URL (e.g., `https://github.com/owner/repo`)
3. Submit the form to initiate the AI documentation generation process
4. Watch real-time progress updates via WebSocket as agents analyze the codebase
5. View the generated README with syntax-highlighted markdown preview
6. Download or copy the final documentation

The system uses a multi-agent workflow:
- **Code Reader** analyzes source files
- **Codebase Summarizer** creates file summaries
- **Requirements Extractor** identifies project needs
- **Section Writer** generates README content
- **Final Reviewer** validates output quality

All agent statuses and progress are displayed in real time through the responsive dashboard interface.

### Next Steps

For advanced usage, refer to:
- `DEMO.md` for detailed examples and API usage
- `CONTRIBUTING.md` for development setup and coding standards
- `PROJECT_SUMMARY.md` for architectural overview

The application features comprehensive logging, security audits, and supports LongCat AI integration for enhanced analysis capabilities.

## Usage

Dr. Document is an AI-powered GitHub documentation generator that automates the creation of comprehensive README files through a sophisticated multi-agent workflow. To begin using the application, start by setting up and running both the frontend and backend components.

First, ensure you have all dependencies installed by running:

```bash
npm install
```

Then launch the development environment with:

```bash
npm run dev
```

This will start both the Vite-powered React frontend and the FastAPI backend with auto-reload capabilities.

Once the application is running, you'll be presented with an intuitive interface featuring a repository input form where you can enter any GitHub repository URL. The system orchestrates seven AI agents in a sequential workflow that includes codebase summarization, requirements extraction, heading selection, section writing, manager review, final validation, and comprehensive documentation generation.

As the agents process the repository, you'll see real-time updates through WebSocket connections that display agent status, progress bars, and current operations. Each agent card shows its individual progress and status, while the overall workflow progress is tracked at the top of the interface.

The system automatically clones the repository, analyzes code files while excluding test directories and non-code files, and processes the codebase through specialized agents. You'll see live updates as agents generate summaries, extract requirements, select relevant documentation headings, and write structured content with badges and code examples.

Once processing completes, the ResultDisplay component presents the generated README with syntax-highlighted markdown preview, repository statistics, and action buttons for copying, downloading, or resetting the workflow. The interface supports full-screen markdown viewing with professional formatting and responsive design.

For advanced usage, you can interact with the backend API directly through the client module, which provides methods for job management, status checking, and real-time WebSocket connections. The comprehensive logging system provides detailed feedback throughout the documentation generation process, ensuring transparency in how each agent contributes to the final output.

## API Endpoints

The Dr. Document backend provides a comprehensive RESTful API built with FastAPI, enabling programmatic interaction with the multi-agent documentation generation system. All API endpoints are accessible under the `/api` prefix and support JSON request/response formats.

### Repository Processing

**`POST /api/process`**  
Initiates a new documentation generation job for a GitHub repository. Accepts a JSON payload with the `repo_url` field containing the full GitHub repository URL. Returns a job ID immediately upon successful submission, which can be used to track progress and retrieve results.

**`GET /api/status/{job_id}`**  
Retrieves the current status and progress of a documentation generation job. Returns detailed information including overall progress percentage, current agent stage, agent-specific status updates, and timestamps for job creation and completion.

### Results Retrieval

**`GET /api/result/{job_id}`**  
Fetches the generated documentation results for a completed job. Returns the full README content in Markdown format, repository statistics (stars, forks, etc.), and metadata about the generation process including agent execution times and final approval status.

### Health & Monitoring

**`GET /api/health`**  
Provides basic health check information for the backend service, returning the service status, version information, and timestamp of the last check.

### WebSocket Integration

**`GET /api/ws/{job_id}`**  
Establishes a WebSocket connection for real-time progress updates during documentation generation. Clients receive live status updates as each agent in the workflow completes its tasks, enabling real-time monitoring of the multi-agent process.

All endpoints include proper error handling and return standardized JSON responses with appropriate HTTP status codes. The API supports CORS for frontend integration and includes comprehensive logging for debugging and monitoring purposes.

## Configuration

The Dr. Document application is configured through multiple layers of settings that control both backend behavior and frontend functionality. The primary configuration system is implemented in `backend/config.py`, which uses Pydantic models to manage application parameters with environment variable support.

### Backend Configuration

The `Config` class in `backend/config.py` defines all backend settings including:
- **API Keys**: OpenAI integration requires `OPENAI_API_KEY` environment variable for LLM processing
- **Model Settings**: Configurable LLM model selection and temperature parameters for agent workflows
- **Storage Paths**: Directory configurations for temporary files, output storage, and cache management
- **File Analysis Limits**: Maximum file sizes and directory exclusions for repository scanning
- **WebSocket Settings**: Real-time update intervals and connection parameters
- **Security Settings**: Rate limiting and request validation thresholds

Environment variables are loaded automatically with sensible defaults, allowing deployment flexibility across development, testing, and production environments.

### Frontend Configuration

The React frontend uses Vite for build optimization with TypeScript support. Key configuration files include:

- **TypeScript Configuration**: 
  - `tsconfig.json` establishes workspace structure with separate configurations for app and Node.js environments
  - `tsconfig.app.json` enables strict type checking for React components with ES2022 features
  - `tsconfig.node.json` configures module resolution for Vite and Node.js compatibility

- **Build Configuration**: 
  - `vite.config.ts` sets up React plugin integration and development server settings
  - `package.json` defines build scripts and dependency management

### Environment Setup

The application requires a virtual environment for Python dependencies managed through `backend/requirements.txt`, which includes FastAPI, OpenAI integration, WebSocket support, and utility libraries. The `backend/run_commands.txt` file provides the standard commands for activating the environment and launching the Uvicorn server on port 8004 with auto-reload functionality.

All configuration values can be overridden through environment variables, making the application highly configurable for different deployment scenarios while maintaining sensible defaults for local development.

## Environment Variables

The Dr. Document application relies on several critical environment variables to configure its AI-powered backend functionality and ensure secure operation. These variables are primarily managed through the `backend/config.py` file, which uses Pydantic's `BaseSettings` to load and validate configuration from environment variables at runtime.

### Required API Keys

The application requires OpenAI API integration for its multi-agent workflow system. You must set the following environment variable:

- **`OPENAI_API_KEY`**: This is essential for all LLM-based agent operations including code analysis, documentation generation, and review processes. Without this key, the backend will fail to initialize and agent tasks cannot be executed.

### Application Configuration

Additional configuration parameters are controlled via environment variables:

- **`LOG_LEVEL`**: Controls the verbosity of logging output from the backend services. Accepts standard logging levels such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. This is used by the comprehensive logging system defined in `backend/logger.py`.

- **`MAX_FILE_SIZE_MB`**: Sets the maximum file size (in megabytes) that the GitHub client (`backend/github_client.py`) will process during repository analysis. This prevents processing of excessively large files and is used by the file scanning utilities.

- **`STORAGE_PATH`**: Defines the directory path where processed repositories and generated documentation are temporarily stored during workflow execution. This path is used by the repository cloning and file management components.

### Security and Operational Settings

- **`ALLOWED_ORIGINS`**: Configures CORS settings for the FastAPI backend running on port 8004. This should be set to the frontend origin (e.g., `http://localhost:5173`) to allow secure cross-origin requests from the React frontend.

All environment variables are validated at application startup through the configuration system in `backend/config.py`. Missing required variables will cause the application to fail initialization. The configuration supports both development and production environments, with sensible defaults provided for optional parameters.

For local development, create a `.env` file in the project root and set your environment variables accordingly. The backend will automatically load these values when started via the commands in `backend/run_commands.txt`.

## Project Structure

The Dr. Document project follows a well-organized monorepo structure with a clear separation between frontend and backend components, optimized for a modern full-stack AI-powered documentation generation system.

### Frontend (React + TypeScript + Vite)

The frontend is built using **React** with **TypeScript** and powered by **Vite** as the build tool. It resides in the `src/` directory and includes:

- **`src/main.tsx`**: Application entry point that initializes React with StrictMode and renders the main `App` component.
- **`src/App.tsx`**: Root component managing repository input, real-time agent status updates via WebSocket, and orchestrating UI state across interconnected components.
- **`src/components/`**: Contains all React components:
  - `AgentWorkspace.tsx`: Dashboard displaying agent progress and status in a grid layout.
  - `AgentCard.tsx`: Individual agent status card with progress bars and state indicators.
  - `RepoInput.tsx`: Form component for submitting GitHub repository URLs.
  - `ResultDisplay.tsx`: Final documentation output viewer with markdown preview, copy/download, and reset functionality.
- **`src/types/index.ts`**: Central TypeScript type definitions for agents, workflows, and application state.
- **`src/App.css` & `src/index.css`**: Global and component-specific styling with dark theme, gradients, and responsive design.
- **`src/components/*.css`**: Modular CSS files for each component, supporting hover effects and animations.

The frontend communicates with the backend via REST and WebSocket APIs, providing real-time updates during documentation generation.

### Backend (FastAPI + Python)

The backend is implemented using **FastAPI** and **Python**, located in the `backend/` directory:

- **`backend/main.py`**: Main FastAPI application entry point with WebSocket support, job management, and RESTful endpoints.
- **`backend/config.py`**: Pydantic-based configuration management with environment variables for API keys, models, and storage paths.
- **`backend/workflow.py`**: Orchestrates the 5-agent asynchronous documentation generation workflow.
- **`backend/agents/`**: Contains all AI agents:
  - `codebase_summarizer.py`: Generates file summaries.
  - `code_reader.py`: Analyzes code files for functions, classes, and dependencies.
  - `requirements_extractor.py`: Identifies functional and technical requirements.
  - `headings_selector.py`: Selects relevant README headings.
  - `section_writer.py`: Writes individual documentation sections.
  - `readme_writer.py`: Compiles final README content.
  - `manager.py`: Reviews and approves sections with feedback.
  - `final_reviewer.py`: Performs final validation of generated documentation.
- **`backend/github_client.py`**: Handles GitHub repository cloning and file scanning.
- **`backend/logger.py`**: Comprehensive logging system with color-coded output and file support.
- **`backend/agents/base_agent.py`**: Abstract base class providing LLM integration and standardized agent interface.
- **`backend/requirements.txt`**: Python dependencies including FastAPI, OpenAI, and WebSocket support.

### Configuration & Tooling

- **`package.json` & `package-lock.json`**: Frontend dependencies including Vite, React, TypeScript, ESLint, and Markdown rendering libraries.
- **`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`**: TypeScript configurations for frontend and Node.js environments.
- **`vite.config.ts`**: Vite build configuration with React plugin.
- **`eslint.config.js`**: ESLint setup with React Hooks and Refresh support.
- **`backend/run_commands.txt`**: Commands to activate virtual environment and run Uvicorn server on port 8004.

This structure enables modular development, clear separation of concerns, and scalable AI agent orchestration for automated GitHub documentation generation.

## Development

### Project Setup and Configuration

The Dr. Document project uses a modern full-stack architecture with a **FastAPI backend** and a **React/TypeScript frontend** built with Vite. To get started, ensure you have Python 3.9+ and Node.js installed.

#### Backend Setup
1. Navigate to the `backend` directory
2. Create and activate a virtual environment using the commands in `run_commands.txt`
3. Install dependencies with `pip install -r requirements.txt`
4. Configure environment variables by copying `.env.example` to `.env` (refer to `config.py` for required variables like `OPENAI_API_KEY`)

#### Frontend Setup
1. Install dependencies with `npm install`
2. The project uses TypeScript with strict type checking enabled in `tsconfig.app.json`
3. ESLint is configured with React Hooks and Refresh support via `eslint.config.js`

### Key Technologies

- **Backend**: FastAPI with WebSocket support, OpenAI integration, and Pydantic configuration
- **Frontend**: React with TypeScript, Vite build tool, and Markdown rendering
- **Agents**: Six specialized AI agents including `CodebaseSummarizerAgent`, `HeadingsSelectorAgent`, `SectionWriterAgent`, `ManagerAgent`, `FinalReviewerAgent`, and `RequirementsExtractorAgent`

### Development Workflow

The application features a **multi-agent documentation generation system** orchestrated through `workflow.py`. Each agent processes specific aspects of repository analysis:

```python
# Example agent workflow
workflow = [
    CodebaseSummarizerAgent,
    HeadingsSelectorAgent,
    SectionWriterAgent,
    ManagerAgent,
    FinalReviewerAgent,
    RequirementsExtractorAgent
]
```

Real-time progress tracking is implemented via WebSocket connections using the `api/client.ts` client, providing live updates on agent status and overall progress.

### Configuration Files

The project uses a workspace structure with separate TypeScript configurations:
- `tsconfig.app.json` for React application compilation
- `tsconfig.node.json` for Node.js/Vite tooling
- `vite.config.ts` for frontend build configuration

### Running the Application

Start the backend server:
```bash
uvicorn main:app --reload --port 8004
```

Start the frontend development server:
```bash
npm run dev
```

The frontend connects to the backend via WebSocket on port 8004, providing real-time updates during documentation generation workflows.

## Contributing

Welcome to the Dr. Document project! We're excited to have you contribute to our AI-powered GitHub documentation generator. This guide will help you get started with development, testing, and contributing to both the backend and frontend components.

### 🚀 Getting Started

**Prerequisites:**
- Python 3.8+ for backend development
- Node.js 16+ and npm for frontend development
- Git for version control

**Setup:**
1. Clone the repository and navigate to the project root
2. Backend setup:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Frontend setup:
   ```bash
   npm install
   ```

### 🏗️ Project Structure

The project follows a clear separation between frontend and backend:

- **Frontend** (`src/`): React + TypeScript application with Vite build tool
- **Backend** (`backend/`): FastAPI service with WebSocket support and multi-agent workflow
- **Configuration**: TypeScript configs in `tsconfig.*.json`, ESLint in `eslint.config.js`

### 🔧 Development Workflow

**Running the Application:**
- Start backend: `cd backend && uvicorn main:app --reload --port 8004`
- Start frontend: `npm run dev`
- Both services communicate via REST API and WebSocket connections

**Code Standards:**
- Follow TypeScript strict typing patterns in frontend
- Use Pydantic models for backend data validation
- Implement comprehensive logging using the custom logger system
- Write unit tests for new agent functionality

### 🤖 Contributing to Agents

The project features a sophisticated multi-agent system. When adding new agents:

1. **Extend BaseAgent**: All agents inherit from `base_agent.py`
2. **Follow the workflow**: New agents should integrate with the existing workflow orchestration
3. **Add proper logging**: Use the established logging patterns
4. **Test imports**: Verify your agent works with the existing test suite

### 🧪 Testing

**Backend Testing:**
- Run `python backend/test_components.py` to verify imports and basic functionality
- Test agent workflows using the existing test patterns
- Ensure all new code follows the established patterns

**Frontend Testing:**
- Use the existing ESLint configuration for code quality
- Follow React component patterns established in existing components
- Test WebSocket connections and real-time updates

### 📝 Documentation

When contributing:
- Update relevant documentation files
- Include examples in `DEMO.md` for new features
- Ensure `PROJECT_SUMMARY.md` reflects current capabilities
- Add security considerations to `SECURITY_AUDIT.md` for new features

### 🔒 Security Considerations

All contributions must maintain security standards:
- Follow the patterns established in `SECURITY_AUDIT.md`
- Validate all inputs using the existing validation patterns
- Implement proper error handling without exposing sensitive information

### 🎯 Pull Requests

Before submitting a PR:
1. Ensure all tests pass
2. Follow the established coding standards
3. Update documentation as needed
4. Include examples of how your changes work
5. Reference any related issues

Thank you for contributing to Dr. Document! Your efforts help make automated documentation generation more powerful and accessible.

## License

This project is licensed under the **MIT License**. The full license text is reproduced below:

```
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

### Key Terms of the MIT License

- **Permissive Use**: You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software without restriction, provided you include the original copyright and license notice in all copies or substantial portions of the software.
- **No Warranty**: The software is provided "as is", without warranty of any kind—express or implied—including but not limited to warranties of merchantability, fitness for a particular purpose, or non-infringement.
- **Attribution Required**: Any redistribution must retain the original copyright notice and the full MIT license text.

### Applicability

This license applies to all source files in the repository, including:

- **Backend Components**: FastAPI application (`backend/main.py`), agent classes (e.g., `codebase_summarizer.py`, `readme_writer.py`), workflow orchestration (`workflow.py`), and configuration (`config.py`).
- **Frontend Components**: React application (`src/App.tsx`, `src/components/AgentWorkspace.tsx`, etc.), TypeScript interfaces (`src/types/index.ts`), and styling files.
- **Configuration & Tooling**: `tsconfig.json`, `vite.config.ts`, `eslint.config.js`, `package.json`, and `requirements.txt`.
- **Documentation**: All markdown files such as `README.md`, `CONTRIBUTING.md`, `DEMO.md`, and `PROJECT_SUMMARY.md`.

### Third-Party Dependencies

The project relies on several open-source libraries, including:

- **Python**: FastAPI, Uvicorn, OpenAI SDK, Pydantic, and asyncio for backend functionality.
- **TypeScript/React**: React, Vite, TypeScript, ESLint, and syntax highlighting libraries for the frontend.
- **Other Utilities**: WebSocket support, logging, and file handling tools.

These dependencies are subject to their respective licenses (e.g., MIT, Apache-2.0, BSD). The project maintains compliance by including appropriate license notices in `package.json` and `requirements.txt`.

### Commercial and Modification Rights

You may use this software for commercial purposes. Modifications are permitted and encouraged, especially for internal or public distribution, as long as the license terms are preserved.

For questions about licensing, please open an issue or contact the maintainers via the repository’s issue tracker.

---

<p align="center">Made with ❤️ by <a href="https://github.com/H0NEYP0T-466">H0NEYP0T-466</a></p>