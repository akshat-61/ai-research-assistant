# AI Research Assistant - Progress Tracker

## Things Done

### Phase 1: Backend Foundations

#### Step 1.1: Project Setup & Package Management
- [x] Initialized project using `uv`.
- [x] Configured `pyproject.toml` with core dependencies (FastAPI, SQLAlchemy 2.0, Alembic, asyncpg, etc.).
- [x] Set up the entry point in `main.py`.

#### Step 1.3: Database Modeling
- [x] Set up SQLAlchemy 2.0 declarative base (`models/base.py`).
- [x] Created `User` model (Authentication data) in `models/user.py`.
- [x] Created `Workspace` model (Project container) in `models/workspace.py`.
- [x] Created `Document` model (File tracking) in `models/document.py`.
- [x] Created `Note` and `Tag` models with a Many-to-Many association table (`note_tags`) in `models/note.py` and `models/tag.py`.
- [x] Centralized imports in `models/__init__.py`.
- [x] Defined all relationships with `cascade="all, delete-orphan"` where appropriate.

## Configuration Details Noted
- **LLM_BASE_URL**: `http://10.10.8.200:5000/v1`
- **MODEL_NAME**: `google/gemma-4-26b-a4b-qat`
- **TEMPERATURE**: `0`
