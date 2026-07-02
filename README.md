# AI Research Assistant

A production-grade AI Research Assistant (similar to NotebookLM or Perplexity) that allows users to upload documents, extract knowledge, and interact with an Agentic AI powered by RAG (Retrieval-Augmented Generation).

## 🚀 Project Overview

This project is built following a comprehensive 6-phase master plan designed to create a scalable, secure, and intelligent system capable of autonomous multi-step reasoning. 

### Key Features (Planned)
- **Multi-Tenant Workspaces**: Users can create isolated workspaces for different research projects.
- **Intelligent RAG Pipeline**: Upload documents (PDFs, text) and extract vector embeddings for accurate, hallucination-free retrieval.
- **Agentic Workflows**: Powered by LangGraph, the AI acts as a multi-agent swarm (Planner, Retriever, Verifier, Writer) to execute complex research tasks.
- **Verifiable Citations**: Every claim made by the AI is backed by exact source citations from the uploaded documents.
- **High Performance**: Asynchronous Python backend (FastAPI), background task processing (Celery/Redis), and semantic caching.

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI (Async Python)
- **Database Layer**: SQLite (via aiosqlite for local dev) / PostgreSQL (Production)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Validation & Settings**: Pydantic & Pydantic-Settings
- **LLM**: Google Gemma-4-26b-a4b-qat (Temperature: 0.0)

## 📈 Current Progress (Phase 1)

We are currently executing **Phase 1: Backend Foundations (CRUD & Auth)**. 

### What has been built so far:
1. **Project Setup**: Initialized using `uv` with core dependencies configured in `pyproject.toml`.
2. **Infrastructure**: 
   - Configured `.env` secrets and LLM variables.
   - Built strong-typed environment validation via `core/config.py`.
3. **Database Architecture**:
   - Switched to an async SQLite database (`ai_research.db`) to streamline local development and bypass Docker/Podman daemon issues.
   - Designed normalized SQLAlchemy 2.0 models with cascading relationships:
     - `User` (Authentication)
     - `Workspace` (Project Containers)
     - `Document` (File Tracking)
     - `Note` & `Tag` (User-generated insights with Many-to-Many associations)
4. **Migrations**: 
   - Initialized Alembic for async migrations.
   - Successfully generated and applied the `initial_schema` migration. The local database is live!

## 🚧 Next Steps

The immediate next goals are to build the API layer:
1. **Pydantic Schemas**: Create strict data validation models for incoming and outgoing API traffic (hiding sensitive data like passwords).
2. **FastAPI Routers**: Build the API endpoints for Authentication (JWT) and Workspaces (CRUD operations protected by auth dependencies).
3. **Transition to Phase 2**: Implement the file upload endpoints to begin parsing documents for the AI.

## 💻 Local Development

To run the project locally (Note: API is currently under construction):

```bash
# 1. Install dependencies using uv
uv sync

# 2. Run database migrations (already up to date if db exists)
uv run alembic upgrade head

# 3. Start the FastAPI development server (Coming Soon!)
uv run uvicorn main:app --reload
```
