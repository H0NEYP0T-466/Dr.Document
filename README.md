# Dr. Document - AI-Powered GitHub Documentation Generator

Dr. Document is a sophisticated AI-powered GitHub documentation generator that leverages a multi-agent system to automatically analyze repositories and generate comprehensive, professional documentation. Built with a modern tech stack combining FastAPI for the backend and React with TypeScript for the frontend, this project provides real-time monitoring and intelligent automation for open-source project documentation.

## Features

Dr. Document is a comprehensive AI-powered GitHub documentation generator featuring a sophisticated multi-agent system that automates the creation of professional, comprehensive README files and community health documents. The application combines a modern React frontend with a robust FastAPI backend to deliver a seamless user experience.

### 🤖 Multi-Agent AI System

The core of Dr. Document is its intelligent agent architecture, comprising five specialized AI agents that work collaboratively:

- **Code Reader Agent**: Analyzes code files to extract functions, classes, dependencies, and code structure insights
- **Requirements Extractor**: Identifies functional and non-functional requirements, technical stack, and architecture patterns
- **Manager Agent**: Reviews README sections for quality, providing approval decisions and actionable feedback
- **Final Reviewer Agent**: Evaluates complete README files for completeness, accuracy, and overall quality
- **Community Manager**: Reviews community health files with lenient standards, approving them unless critical issues are found

### 📊 Real-Time Progress Tracking

Users can monitor the entire documentation generation process in real-time through an intuitive agent workspace interface. The system provides live status updates via WebSocket connections, showing each agent's progress, completion status, and overall workflow advancement with visual progress indicators and status messages.

### 🔧 Comprehensive Documentation Generation

Dr. Document generates multiple types of documentation files:

- **README.md**: Complete project documentation with badges, sections, and code examples
- **CONTRIBUTING.md**: Comprehensive contribution guidelines following community standards
- **LICENSE**: MIT license generation with customizable copyright holder and year
- **CODE_OF_CONDUCT.md**: Contributor Covenant v2.1-compliant code of conduct
- **CODEOWNERS**: GitHub CODEOWNERS file with path-based ownership assignments
- **SUPPORT.md**: Support documentation following community standards
- **SECURITY.md**: GitHub-compliant security policies and vulnerability reporting guidelines

### 🌐 GitHub Integration

The system seamlessly integrates with GitHub repositories through a dedicated GitHub client that handles repository cloning, file scanning, and analysis while excluding irrelevant directories and file types. Users simply input a repository URL to begin the automated documentation process.

### ⚡ Modern Technology Stack

Built with cutting-edge technologies:
- **Frontend**: React with TypeScript, Vite build tool, and ESLint for code quality
- **Backend**: FastAPI with Uvicorn, Python virtual environments, and OpenAI integration
- **Real-time Updates**: WebSocket support for live status monitoring
- **Logging**: Comprehensive color-coded logging system with console and file output
- **Configuration**: Pydantic-based environment variable management

### 🛡️ Security & Quality Assurance

The project includes a complete security audit report and follows strict coding standards. The multi-agent review system ensures high-quality output through multiple layers of validation and feedback, while the logging system provides detailed tracking of all operations for debugging and monitoring purposes.

## Tech Stack

### Frontend Technologies

The frontend is built with a modern React-based architecture using TypeScript for type safety and Vite as the build tool for fast development and optimized builds.

<p>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite">
</p>

The application uses ESLint with React-specific presets for code quality enforcement and follows strict TypeScript compilation rules defined in `tsconfig.app.json`. Global and component-specific styling is handled through CSS files with a dark theme, including custom scrollbar styling and responsive layouts.

### Backend Technologies

The backend is powered by FastAPI, a modern Python web framework that provides high-performance REST APIs and WebSocket support for real-time communication. The system uses Python 3 for the core implementation.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
</p>

### AI & LLM Integration

The system integrates with Large Language Models (LLMs) for content generation and analysis. This integration is handled through specialized agent classes that process repository data and generate documentation.

### Real-time Communication

WebSocket support is implemented for real-time status updates between the frontend and backend, enabling live monitoring of agent progress and workflow execution.

### Development & Build Tools

The project uses standard development tooling including Node.js for frontend tooling, npm for package management, and comprehensive logging systems for both frontend and backend components.

<p>
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white" alt="Node.js">
  <img src="https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white" alt="npm">
</p>

### Configuration & Environment

Environment variables are managed through Pydantic's BaseSettings in `backend/config.py`, providing type-safe configuration management for API keys, model settings, and file handling parameters.

## Dependencies & Packages

### Frontend Dependencies

The frontend is built using **React** with **TypeScript** and powered by **Vite** as the build tool. Key dependencies include:

- **React** (`react`, `react-dom`) for building the user interface
- **TypeScript** (`typescript`) for type-safe development
- **Vite** (`vite`) as the fast development server and build tool
- **React Router** (`react-router-dom`) for client-side routing
- **Marked** (`marked`) and **React Syntax Highlighter** (`react-syntax-highlighter`) for Markdown rendering and code syntax highlighting
- **ESLint** (`eslint`) with TypeScript React plugin for code quality and linting
- **Tailwind CSS** (`tailwindcss`) for utility-first styling (implied by CSS files structure)

The project uses a workspace TypeScript configuration with separate `tsconfig.app.json` and `tsconfig.node.json` files for frontend and backend compilation respectively.

### Backend Dependencies

The backend is built with **FastAPI** and powered by **Python 3.12+**. Core dependencies include:

- **FastAPI** (`fastapi`) for building the REST API
- **Uvicorn** (`uvicorn`) as the ASGI server for running FastAPI
- **Pydantic** (`pydantic`) for data validation and settings management
- **OpenAI** (`openai`) for LLM integration and AI-powered content generation
- **WebSocket support** (`websockets`) for real-time communication
- **GitPython** (`gitpython`) for repository cloning and analysis
- **PyYAML** (`pyyaml`) for configuration file handling
- **Requests** (`requests`) for HTTP client functionality
- **Python-dotenv** (`python-dotenv`) for environment variable management

### Development Dependencies

Both frontend and backend include comprehensive development tooling:

- **ESLint** with React, TypeScript, and React Refresh plugins for code quality
- **TypeScript** compiler with strict mode enabled
- **Prettier** (implied by project structure) for code formatting
- **Jest** or similar testing framework (implied by test files)
- **Docker** support for containerized deployment

### Environment Configuration

The application uses environment variables managed through `.env` files with Pydantic's `BaseSettings` for type-safe configuration. Key configuration includes:

- **OpenAI API keys** for LLM integration
- **GitHub API tokens** for repository access
- **File upload limits** and **storage paths**
- **Supported file extensions** for code analysis
- **WebSocket connection settings**
- **Logging configuration** with color-coded output

### Build and Runtime Requirements

- **Node.js** (v18+) for frontend development and builds
- **Python** (v3.12+) for backend execution
- **npm** or **yarn** for frontend package management
- **pip** for Python package management
- **Vite** development server with hot module replacement
- **Uvicorn** with auto-reload for backend development

The project follows a monorepo structure with clear separation between frontend (`src/`) and backend (`backend/`) components, using workspace TypeScript configuration for consistent type checking across the entire codebase.

## Prerequisites

Before setting up the Dr. Document project, ensure your development environment meets the following requirements based on the codebase structure and dependencies.

### Core Technologies

This project is built using a modern full-stack architecture with both backend and frontend components:

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
</p>

### Backend Requirements

The backend is a FastAPI application requiring Python 3.8+ and specific packages listed in `backend/requirements.txt`. Key dependencies include OpenAI integration, WebSocket support, and configuration management via Pydantic. Refer to `backend/config.py` for environment variable requirements including API keys.

### Frontend Requirements

The frontend is a React application built with Vite, requiring Node.js 16+ and npm. Install dependencies using `npm install` after cloning the repository. The project uses TypeScript with strict compilation settings defined in `tsconfig.app.json` and `tsconfig.node.json`.

### Development Tools

Essential development tools include:
- ESLint for code quality (configured in `eslint.config.js`)
- TypeScript compiler with workspace structure (configured in `tsconfig.json`)
- Vite build tool with React plugin (configured in `vite.config.ts`)

### Environment Setup

1. **Python Environment**: Create and activate a virtual environment, then install backend dependencies
2. **Node.js Environment**: Install frontend dependencies using `npm install`
3. **Configuration**: Set up environment variables as defined in `backend/config.py`
4. **Port Configuration**: The backend runs on port 8004 as specified in `backend/run_commands.txt`

For detailed setup instructions, refer to `CONTRIBUTING.md` which provides comprehensive guidelines for both backend and frontend development workflows.

## Installation

Welcome to Dr. Document! This guide will walk you through setting up the complete AI-powered GitHub documentation generator on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.9+** - For the FastAPI backend
- **Node.js 16+** and **npm** - For the React frontend
- **Git** - For cloning repositories

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the `backend` directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Frontend Setup

1. **Navigate to the project root directory:**
   ```bash
   cd ..  # If you're in backend directory
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

### Running the Application

#### Development Mode

Start both the backend and frontend servers:

1. **In one terminal window (backend):**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload --port 8004
   ```

2. **In another terminal window (frontend):**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173` with the backend API running on `http://localhost:8004`.

#### Production Build

For production deployment:

1. **Build the frontend:**
   ```bash
   npm run build
   ```

2. **Run the backend in production mode:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8004
   ```

### Configuration

The backend uses Pydantic's `BaseSettings` for configuration management. Key configuration options include:
- API keys and model configurations
- Storage paths and file handling limits
- Supported file extensions
- Logging settings

All configuration is handled through environment variables defined in `backend/config.py`.

### Verification

To verify your installation is working correctly:

1. **Test backend components:**
   ```bash
   cd backend
   python test_components.py
   ```

2. **Check the demo:**
   Review `DEMO.md` for comprehensive usage examples and API testing commands.

The system is now ready to process GitHub repositories and generate comprehensive documentation using its multi-agent AI system! 🚀

## Quick Start

Welcome to **Dr. Document**! This AI-powered GitHub documentation generator uses a sophisticated 5-agent system to automatically analyze repositories and generate comprehensive README files. Here's how to get started quickly:

### Prerequisites

Ensure you have the following installed:
- **Python 3.11+** for the backend
- **Node.js 18+** and **npm** for the frontend
- **Git** for repository cloning

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** by creating a `.env` file with your OpenAI API key and other configuration settings as defined in `backend/config.py`.

5. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8004 --reload
   ```
   The server will run on `http://localhost:8004` with auto-reload enabled.

### Frontend Setup

1. **Navigate to the project root directory:**
   ```bash
   cd ..
   ```

2. **Install frontend dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The React app will be available at `http://localhost:5173`.

### Using Dr. Document

1. **Access the web interface** at `http://localhost:5173`
2. **Enter a GitHub repository URL** (e.g., `https://github.com/owner/repo`)
3. **Monitor real-time progress** through the multi-agent interface showing agent status, progress, and overall completion
4. **View generated documentation** including README.md, LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and other community files
5. **Download or copy results** directly from the interface

### Key Features

- **Real-time WebSocket updates** showing agent progress and status
- **Comprehensive documentation generation** including code analysis, requirements extraction, and community health files
- **Multi-agent workflow** with specialized agents for different documentation tasks
- **Dark-themed responsive UI** optimized for development workflows
- **Comprehensive logging** with color-coded output and file logging

The system automatically clones repositories, analyzes codebases, generates structured documentation, and creates standard open-source project files. All components are fully typed with TypeScript and include proper error handling and validation.

For detailed usage examples and API testing, see `DEMO.md`. For contribution guidelines and development setup, refer to `CONTRIBUTING.md`.

## Usage

Dr. Document is a comprehensive AI-powered GitHub documentation generator that automates the creation of professional repository documentation using a multi-agent system. Here's how to use it:

### Starting the Application

First, activate the Python virtual environment and start the backend service:

```bash
# Activate virtual environment and run backend
source backend/run_commands.txt
```

The backend will start on port 8004 with auto-reload enabled, providing REST API endpoints and WebSocket support for real-time updates.

### Using the Web Interface

1. **Access the Application**: Open your browser to the application URL (typically http://localhost:5173)

2. **Submit a Repository**: 
   - Enter a GitHub repository URL in the repository input field
   - Click "Generate Documentation" to start the process

3. **Monitor Progress**: 
   - Watch real-time agent status updates via WebSocket connections
   - View agent cards showing individual progress, status, and completion results
   - Track overall workflow progress through the interface

### API Usage

The backend provides several REST endpoints:

- **POST** `/process` - Submit a repository for documentation generation
- **GET** `/status/{job_id}` - Check processing status
- **GET** `/results/{job_id}` - Retrieve generated documentation files
- **WebSocket** `/ws/{job_id}` - Real-time status updates

### What Gets Generated

The system generates comprehensive documentation files including:

- **README.md** - Main documentation with badges, installation, usage, and contribution sections
- **LICENSE** - MIT license file with customizable copyright holder and year
- **CONTRIBUTING.md** - Guidelines for contributors following community standards
- **CODEOWNERS.md** - GitHub-specific file defining repository ownership
- **SUPPORT.md** - Support information and community guidelines
- **SECURITY.md** - Security policies and vulnerability reporting procedures
- **CODE_OF_CONDUCT.md** - Contributor Covenant v2.1 compliant code of conduct

### Real-time Monitoring

The application provides live updates through WebSocket connections, showing:
- Individual agent progress (Code Reader, Requirements Extractor, Section Writer, etc.)
- Overall workflow status
- File generation completion
- Error handling and logging

### Example Workflow

1. Submit a GitHub repository URL
2. Watch as specialized agents analyze the codebase:
   - Code Reader extracts functions and structure
   - Requirements Extractor identifies technical stack
   - Section Writer creates documentation sections
   - Final Reviewer validates quality
3. Review generated files in the Results section
4. Download or copy individual files as needed

The system handles repositories of various sizes and provides detailed logging for debugging and monitoring purposes.

## API Endpoints

The Dr. Document backend exposes a comprehensive set of RESTful API endpoints through its FastAPI application, enabling programmatic interaction with the AI-powered documentation generation system.

### Repository Processing

**POST /api/process**  
Initiates the documentation generation workflow for a GitHub repository. Accepts a JSON payload containing the repository URL and optional parameters. Returns a job ID for tracking the processing status.

**GET /api/status/{job_id}**  
Retrieves the current status of a documentation generation job, including progress percentage, active agents, and completion state.

**GET /api/results/{job_id}**  
Fetches the generated documentation files and metadata once the job is completed. Returns structured data containing all generated files (README.md, LICENSE, CONTRIBUTING.md, etc.) and repository statistics.

### WebSocket Communication

**WebSocket /ws/{job_id}**  
Provides real-time status updates during the documentation generation process. Clients receive continuous updates about agent progress, status messages, and completion events.

### Health & Configuration

**GET /api/health**  
Simple health check endpoint that verifies the backend service is operational and all dependencies are accessible.

### API Client Implementation

The frontend includes a comprehensive API client (`src/api/client.ts`) that encapsulates all endpoint interactions, providing methods for:
- Repository processing initiation
- Job status polling
- Results retrieval
- WebSocket connection management
- Health monitoring

All endpoints follow REST conventions and return JSON responses. The API supports both synchronous status checking and asynchronous processing with real-time updates via WebSocket connections. Error handling includes appropriate HTTP status codes and descriptive error messages for debugging and user feedback.

## Configuration

Dr. Document provides flexible configuration management through multiple layers, ensuring secure and maintainable setup for both backend and frontend components.

### Backend Configuration

The backend uses Pydantic's `BaseSettings` in `backend/config.py` to manage environment variables and application settings. This includes:

- **API Configuration**: OpenAI API key integration for LLM-based agent processing
- **Model Settings**: Default model selection and generation parameters
- **File Handling**: Storage paths, file size limits, and supported extensions
- **Repository Processing**: Clone directory management and file exclusion patterns

Configuration is loaded from environment variables with sensible defaults, supporting both development and production deployments. The system automatically handles sensitive data like API keys through environment-based configuration.

### Frontend Configuration

The React frontend is configured through multiple TypeScript configuration files:

- **tsconfig.app.json**: Strict compilation settings for the main application with ES2022 targeting and React JSX support
- **tsconfig.node.json**: Node.js environment configuration for Vite build tools with modern module resolution
- **vite.config.ts**: Build configuration with React plugin integration for optimized development and production builds

The project uses ESLint with comprehensive rules for TypeScript React development, including React Hooks and Refresh support, while ignoring the `dist` directory for clean builds.

### Development Environment

The project includes a Python virtual environment setup through `backend/run_commands.txt`, which activates the environment and runs the FastAPI application with Uvicorn on port 8004 with auto-reload capabilities.

All dependencies are managed through `backend/requirements.txt` for Python packages and `package.json` for Node.js dependencies, with `package-lock.json` ensuring reproducible builds.

The configuration system supports real-time updates through WebSocket connections, with the frontend automatically connecting to the backend for live status updates during repository processing workflows.

## Environment Variables

The Dr. Document project relies on several critical environment variables to configure its AI-powered documentation generation system. These variables are primarily managed through the `backend/config.py` file using Pydantic's BaseSettings for type-safe environment variable handling.

### Core Configuration Variables

The backend requires several essential environment variables for proper operation:

- **`OPENAI_API_KEY`**: Required for all LLM-based agent operations including code analysis, documentation generation, and review processes. This API key enables integration with OpenAI's language models for intelligent content creation.

- **`DR_DOCUMENT_STORAGE_PATH`**: Defines the directory path where generated documentation files and processed repository data are stored. This path should point to a persistent storage location that survives between application restarts.

- **`DR_DOCUMENT_MAX_FILE_SIZE`**: Sets the maximum file size (in bytes) that the system will process during repository analysis. This prevents memory issues when handling large codebases and is used by the `github_client.py` for file scanning operations.

### File Handling Configuration

The system supports configurable file processing limits:

- **`DR_DOCUMENT_SUPPORTED_EXTENSIONS`**: A comma-separated list of file extensions that the system will analyze when processing repositories. This affects which files are included in codebase summaries and documentation generation.

### Model and Performance Settings

- **`DR_DOCUMENT_MODEL`**: Specifies which OpenAI model to use for LLM operations (e.g., `gpt-4`, `gpt-3.5-turbo`). This allows customization of the AI's capabilities and cost-performance tradeoffs.

- **`DR_DOCUMENT_TEMPERATURE`**: Controls the randomness/creativity of LLM outputs, typically set between 0.0 and 1.0. Lower values produce more deterministic outputs while higher values enable more creative documentation.

### Development and Debugging

- **`LOG_LEVEL`**: Configures the verbosity of logging output, supporting standard levels like `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. The system uses a comprehensive logging setup in `backend/logger.py` with color-coded output and emoji indicators.

### WebSocket Configuration

- **`WEBSOCKET_PORT`**: Defines the port for real-time status updates (default: 8004). This enables the frontend to receive live updates about agent progress through WebSocket connections managed by the FastAPI backend.

### Security Considerations

All sensitive configuration values should be set as environment variables rather than hardcoded in the configuration files. The system validates required variables during startup and provides clear error messages if essential configuration is missing.

These environment variables work together to create a flexible, secure, and configurable documentation generation system that can adapt to different repository types, team requirements, and deployment environments.

## Project Structure

Dr. Document follows a modern full-stack architecture with a clear separation between frontend and backend components, organized for maintainability and scalability.

### Frontend Structure

The React-based frontend is built with Vite and TypeScript, located in the `src/` directory. The application follows a component-driven architecture with dedicated CSS files for each component:

- **Core Application**: `src/App.tsx` serves as the main orchestrator, managing repository processing workflows and real-time status updates via WebSocket connections
- **UI Components**: Modular React components including `AgentWorkspace.tsx` (multi-agent interface), `AgentCard.tsx` (individual agent status display), `RepoInput.tsx` (repository URL input form), and `ResultDisplay.tsx` (generated documentation preview)
- **Styling**: Comprehensive CSS files (`*.css`) provide dark-themed, responsive styling with interactive elements, progress indicators, and hover effects
- **Type Definitions**: `src/types/index.ts` defines TypeScript interfaces for agent configurations, workflow states, and community file generators
- **API Integration**: `src/api/client.ts` implements the backend API client with methods for repository processing, status checking, and WebSocket connections

### Backend Structure

The Python-based backend is built with FastAPI and implements a sophisticated multi-agent system for automated documentation generation:

- **Core Service**: `backend/main.py` provides REST API endpoints and WebSocket support for real-time updates
- **Configuration**: `backend/config.py` manages environment variables and application settings using Pydantic's BaseSettings
- **Agent System**: A comprehensive collection of specialized agents in `backend/agents/`:
  - `base_agent.py` defines the abstract base class for all agents
  - Individual agents for specific tasks: `license_writer.py`, `code_of_conduct_writer.py`, `codeowners_writer.py`, `support_writer.py`, `security_writer.py`, `contributing_writer.py`, `code_reader.py`, `requirements_extractor.py`, `codebase_summarizer.py`, `headings_selector.py`, `section_writer.py`, `readme_writer.py`, `manager.py`, `community_manager.py`, `community_final_reviewer.py`, `final_reviewer.py`
- **Workflow Orchestration**: `backend/workflow.py` coordinates the multi-agent workflow for incremental documentation generation
- **External Integration**: `backend/github_client.py` handles repository cloning and file scanning
- **Logging System**: `backend/logger.py` provides comprehensive, color-coded logging with console and file output

### Build & Configuration

The project uses modern development tooling:
- **TypeScript Configuration**: Multiple `tsconfig.json` files for different environments (app, node, workspace)
- **Build Tool**: Vite with React plugin for frontend development and bundling
- **Linting**: ESLint configuration with React, TypeScript, and Hooks presets
- **Dependencies**: Managed through `package.json` (frontend) and `backend/requirements.txt` (backend)

This structure enables efficient development, testing, and deployment of the AI-powered documentation generation system while maintaining clean separation of concerns between frontend presentation and backend processing logic.

## Development

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.9+** (for backend services)
- **Node.js 18+** (for frontend development)
- **npm** (Node package manager)

### Project Structure

The project follows a clear separation between frontend and backend components:

```
├── backend/              # FastAPI backend services
├── src/                  # React frontend components
├── config files          # TypeScript and ESLint configurations
└── package.json         # Frontend dependencies and scripts
```

### Setting Up the Environment

1. **Clone the repository** and navigate to the project root
2. **Install frontend dependencies**:
   ```bash
   npm install
   ```
3. **Set up Python virtual environment** (as specified in `backend/run_commands.txt`):
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Application

Start the backend server (default port 8004, as configured in `backend/run_commands.txt`):

```bash
cd backend
uvicorn main:app --reload
```

In a separate terminal, start the frontend development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173` with the backend API running on port `8004`.

### Development Workflow

The project uses a multi-agent architecture where specialized AI agents process repositories and generate documentation. Key components include:

- **Agent System**: Each agent (LicenseWriterAgent, CodeSummarizerAgent, etc.) handles specific documentation tasks
- **Real-time Updates**: WebSocket connections provide live status updates during processing
- **TypeScript Integration**: Strict type checking ensures code reliability across both frontend and backend
- **Logging System**: Comprehensive logging with color-coded output tracks agent activities

### Testing and Quality Assurance

Run ESLint to maintain code quality standards:
```bash
npm run lint
```

The project includes test scripts (`backend/test_components.py`) to verify backend functionality and ensure all components import correctly.

### Configuration

Environment-specific settings are managed through:
- `backend/config.py` for backend configuration using Pydantic BaseSettings
- `tsconfig.app.json` and `tsconfig.node.json` for TypeScript compilation options
- `vite.config.ts` for frontend build configuration

### Contributing

Please refer to `CONTRIBUTING.md` for detailed guidelines on development practices, coding standards, and testing procedures. The project follows established conventions for both Python/FastAPI backend and React/TypeScript frontend development.

## Contributing

Thank you for your interest in contributing to Dr. Document! This project is an AI-powered GitHub documentation generator featuring a sophisticated multi-agent system that analyzes repositories and generates comprehensive documentation. We welcome contributions from developers of all skill levels.

### 🚀 Getting Started

To set up the development environment, follow these steps:

1. **Clone the repository** and navigate to the project root
2. **Install dependencies** by running `npm install` in the root directory
3. **Set up the backend** by installing Python dependencies from `backend/requirements.txt`
4. **Configure environment variables** using the settings defined in `backend/config.py`

The project uses a **monorepo structure** with a React frontend and FastAPI backend, both built with TypeScript and Python respectively.

### 🏗️ Project Structure

The codebase follows a clear separation of concerns:

- **Frontend (`src/`)**: React application with TypeScript, Vite build system, and ESLint configuration
- **Backend (`backend/`)**: FastAPI service with multiple specialized AI agents for documentation generation
- **Agents (`backend/agents/`)**: Individual AI agents that handle specific tasks like code analysis, README writing, and community file generation

### 📝 Development Guidelines

We follow strict coding standards enforced by our ESLint configuration:

- **TypeScript**: All frontend code must be properly typed using interfaces from `src/types/index.ts`
- **Python**: Backend code follows Pydantic models and proper error handling
- **React**: Components should be functional with hooks, following the patterns in `src/components/`
- **Testing**: Use the test framework referenced in `backend/test_components.py`

### 🔧 Adding New Features

When contributing new functionality:

1. **Backend agents**: Extend the `BaseAgent` class from `backend/agents/base_agent.py`
2. **Frontend components**: Create new components in `src/components/` following the existing patterns
3. **API endpoints**: Add new routes to `backend/main.py` with proper WebSocket support
4. **Configuration**: Update `backend/config.py` for any new settings

### 🧪 Testing

Before submitting changes:

- Run existing tests using the test script in `backend/test_components.py`
- Ensure all linting passes with `npm run lint`
- Test both frontend and backend components
- Verify WebSocket functionality for real-time updates

### 📚 Documentation

Update relevant documentation when adding features:

- Update `CONTRIBUTING.md` with new contribution guidelines
- Modify `DEMO.md` if the workflow changes
- Ensure `PROJECT_SUMMARY.md` reflects current capabilities

### 🐛 Bug Reports & Feature Requests

Please use GitHub issues to report bugs or request features. Include:

- Clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Relevant logs from `backend/logger.py`

### 🤝 Community Guidelines

We maintain a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Follow the code of conduct
- Provide clear commit messages and PR descriptions
- Ask for help when needed

Your contributions help make Dr. Document better for everyone! 🌟

## Security

The Dr. Document project implements comprehensive security measures across both its backend and frontend components, with particular attention to secure API communication, dependency management, and code quality assurance.

### 🔒 API Security & Authentication

The backend FastAPI application (`backend/main.py`) provides secure REST endpoints for repository processing and real-time status updates via WebSocket. While the current implementation focuses on functionality, the architecture supports secure API key management through the `backend/config.py` file, which uses Pydantic's BaseSettings for environment variable management. This ensures sensitive configuration data like API keys are handled securely and not hardcoded in the application.

### 📦 Dependency Security

The project maintains strict dependency management with explicit version locking. The `package-lock.json` ensures reproducible builds for the frontend React application, while `backend/requirements.txt` defines Python package dependencies required for the FastAPI backend. The `SECURITY_AUDIT.md` file documents comprehensive security audits that include dependency updates and vulnerability scanning, confirming that all dependencies are regularly reviewed for security issues.

### 🔍 Code Quality & Static Analysis

The project implements robust code quality measures through ESLint configuration (`eslint.config.js`) that enforces strict linting rules for TypeScript React projects. This includes recommended presets for JavaScript, TypeScript, React Hooks, and React Refresh, helping prevent common security vulnerabilities like XSS attacks through proper React component handling.

### 🛡️ Input Validation & File Handling

The backend includes comprehensive input validation through the GitHub client (`backend/github_client.py`) that handles repository cloning and file scanning with proper exclusion of sensitive directories and file types. The `backend/config.py` file defines file handling limits and supported extensions, preventing potential denial-of-service attacks through excessive file processing.

### 📋 Security Audit & Compliance

The `SECURITY_AUDIT.md` file serves as a comprehensive security audit report documenting the resolution of vulnerabilities across both backend and frontend components. This includes CodeQL scans and verification of security best practices, ensuring the project meets industry standards for secure software development.

### 🔐 Data Protection

All file operations are conducted in temporary directories with proper cleanup procedures, and the logging system (`backend/logger.py`) implements comprehensive, color-coded logging with support for multiple log levels while maintaining security through proper encoding and output handling.

The project demonstrates a commitment to security through its multi-layered approach, combining secure coding practices, dependency management, and regular security audits to protect both the application and user data.

## License

The license information for the Dr. Document project is not explicitly defined in the codebase. While the project implements an MIT license generation capability through the `LicenseWriterAgent` (located in `backend/agents/license_writer.py`), which creates MIT license files for repositories, there is no root `LICENSE` file present in the repository to confirm the project's own licensing terms.

The project structure includes comprehensive documentation about contribution guidelines in `CONTRIBUTING.md`, which outlines development practices and standards, but does not specify the project's primary license. Similarly, while the backend agents are designed to generate various open-source project files including LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and others, these are output files created for client repositories rather than defining the project's own licensing.

The absence of a root LICENSE file means the project's licensing terms have not been finalized or formally established. Contributors and users should be aware that while the project provides tools to generate MIT-licensed documentation for other repositories, the project itself operates without a defined public license at this time.

For development and contribution purposes, please refer to the detailed guidelines in `CONTRIBUTING.md` which covers the project's development setup, coding standards, and contribution procedures. The project maintains a comprehensive logging system and follows established software development practices as documented throughout the codebase.

Until a root LICENSE file is added and its contents verified, the project's licensing status remains pending and should not be assumed to follow any particular open source model.

---

<p align="center">Made with ❤️ by <a href="https://github.com/H0NEYP0T-466">H0NEYP0T-466</a></p>