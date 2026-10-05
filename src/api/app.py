# ==========================================
# DATALENS AI - FASTAPI APPLICATION V2
# ==========================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.database.connection import initialize_database


# ==========================================
# APPLICATION SETTINGS
# ==========================================

APPLICATION_NAME = "DataLens AI API"
APPLICATION_VERSION = "1.1.0"

ALLOWED_ORIGINS = [
    # Local development
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    # Production frontend
    "https://data-lens-ai-mocha.vercel.app",
]


# ==========================================
# APPLICATION LIFESPAN
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize application resources
    when the FastAPI server starts.
    """

    print("\n================================")
    print("STARTING DATALENS AI API")
    print("================================")

    initialize_database()

    print("✓ Database initialized.")
    print(f"✓ API Version: {APPLICATION_VERSION}")

    yield

    print("\n================================")
    print("STOPPING DATALENS AI API")
    print("================================")


# ==========================================
# CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title=APPLICATION_NAME,
    description=(
        "Intelligent Data Science & "
        "Business Analytics Platform"
    ),
    version=APPLICATION_VERSION,
    lifespan=lifespan,
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# API ROUTES
# ==========================================

app.include_router(
    router,
    prefix="/api",
    tags=["DataLens AI"],
)


# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get("/")
def root():
    """
    Basic API information endpoint.
    """

    return {
        "application": "DataLens AI",
        "status": "running",
        "version": APPLICATION_VERSION,
        "message": "DataLens AI API is running.",
        "documentation": "/docs",
        "health": "/api/health",
    }