# AI Research Assistant - Progress Tracker

## Things Done

### Phase 1: Backend Foundations

#### Step 1.1: Project Setup & Package Management
- [x] Initialized project using `uv`.
- [x] Configured `pyproject.toml` with core dependencies (FastAPI, SQLAlchemy 2.0, Alembic, asyncpg, aiosqlite, etc.).
- [x] Set up the entry point in `main.py`.

#### Step 1.2: Infrastructure Setup
- [x] Created local secrets file (`.env`) for DB credentials and LLM Configuration.
- [x] Configured `core/config.py` using Pydantic BaseSettings for strong typing of environment variables.
- [x] Configured LLM Variables: `LLM_BASE_URL` (10.10.8.200), `MODEL_NAME` (gemma-4-26b-a4b-qat), `TEMPERATURE` (0.0).

#### Step 1.3: Database Modeling
- [x] Set up SQLAlchemy 2.0 declarative base (`models/base.py`).
- [x] Created Models: `User`, `Workspace`, `Document`, `Note`, `Tag` with all relationships and foreign keys.
- [x] Configured Many-to-Many association table (`note_tags`).
- [x] Centralized imports in `models/__init__.py`.

#### Step 1.4: Database Engine & Migrations
- [x] Created Async DB Engine and session maker in `core/database.py`.
- [x] Initialized Alembic (`alembic init -t async`).
- [x] Configured `alembic/env.py` to pull metadata and DB URL from application settings.
- [x] Successfully generated first migration: `alembic revision --autogenerate -m "initial_schema"`.
- [x] Applied migration to create local database: `alembic upgrade head`.

#### Step 1.5: Pydantic Schemas (Data Validation)
- [x] Created Base, Create, Update, and Response schemas for User, Workspace, Document, Note, and Tag.
- [x] Enabled `from_attributes=True` for Response schemas.

#### Step 1.6: Security & Authentication Layer
- [x] Implemented password hashing (bcrypt) and JWT functions in `core/security.py`.
- [x] Created `get_current_user` OAuth2 dependency in `api/deps.py`.

#### Step 1.7: API Routing & Controllers
- [x] Built Auth router (`/auth/register`, `/auth/login`, `/auth/me`).
- [x] Built Workspaces CRUD router.
- [x] Built sub-routers for Documents, Notes, and Tags linked to a workspace.
- [x] Rewrote `main.py` to instantiate FastAPI and include all routers.

#### Step 1.8: Unit & Integration Testing
- [x] Set up `pytest` with `pytest-asyncio` and `httpx`.
- [x] Configured `conftest.py` for async in-memory SQLite database (`sqlite+aiosqlite:///:memory:`).
- [x] Wrote tests for user registration, duplicate prevention, and JWT login.
- [x] Wrote tests for Workspace creation and retrieval using auth headers.
- [x] Downgraded `bcrypt` to `4.0.1` to resolve passlib 72-byte string hash bug during testing.
- [x] Tests pass successfully.

## Challenges & Solutions

### 1. Database Migration Blocker (Docker/Podman Issue)
**Problem:** We initially attempted to use PostgreSQL via Docker for local development. However, the local container environment (Podman masquerading as Docker) failed to start the `docker-compose.yml` stack due to a daemon connection error (`Not supported URL scheme http+docker`). This blocked Alembic from connecting to the database, which is required to auto-generate the initial SQL schemas from our Python models.

**Solution:** Rather than spending time fighting the local container daemon configuration, we pivoted to using **SQLite** for local development. 
- Installed the async SQLite driver (`uv add aiosqlite`).
- Updated the `DATABASE_URL` in `.env` and `core/config.py` to point to a local file (`sqlite+aiosqlite:///./ai_research.db`).
- This completely removed the dependency on external servers or Docker, allowing Alembic to successfully generate the migration and build the database file locally.
