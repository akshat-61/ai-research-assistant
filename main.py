from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, workspaces, documents, notes, tags, chat

app = FastAPI(
    title="AI Research Assistant",
    description="Backend for the AI Research Assistant project.",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(workspaces.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(tags.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to AI Research Assistant API"}
