"""FastAPI application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import etp
from app.core.config import MOCK_AI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Gerador de ETP - FormalizaAI",
    description="API para geração automática de Estudos Técnicos Preliminares usando Vertex AI (Gemini 1.5 Pro)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do seu frontend  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(etp.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Gerador de ETP - FormalizaAI",
        "status": "running",
        "mock_mode": MOCK_AI
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting FastAPI application...")
    logger.info(f"Mock AI mode: {MOCK_AI}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

