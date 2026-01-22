"""Configuration management using environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Google Cloud / Vertex AI Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-east1")
MODEL_NAME = os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash-001")

# Development / Testing
MOCK_AI = os.getenv("MOCK_AI", "False").lower() == "true"

# File paths for context injection
LEI_14133_PATH = DATA_DIR / "lei_14133_artigos_chave.txt"
TEMPLATE_ETP_PATH = DATA_DIR / "template_etp_torres.txt"


def load_context_files() -> tuple[str, str]:
    """
    Load context files for RAG injection.
    
    Returns:
        Tuple containing (lei_content, template_content)
        
    Raises:
        FileNotFoundError: If context files are missing
    """
    if not LEI_14133_PATH.exists():
        raise FileNotFoundError(f"Context file not found: {LEI_14133_PATH}")
    if not TEMPLATE_ETP_PATH.exists():
        raise FileNotFoundError(f"Context file not found: {TEMPLATE_ETP_PATH}")
    
    lei_content = LEI_14133_PATH.read_text(encoding="utf-8")
    template_content = TEMPLATE_ETP_PATH.read_text(encoding="utf-8")
    
    return lei_content, template_content

