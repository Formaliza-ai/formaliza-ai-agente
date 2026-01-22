"""ETP generation endpoints."""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status

from app.schemas.etp import ETPGenerateRequest, ETPGenerateResponse, ErrorResponse
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/etp", tags=["ETP"])

# Initialize AI service (singleton pattern)
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


@router.post(
    "/generate",
    response_model=ETPGenerateResponse,
    status_code=status.HTTP_200_OK,
    responses={
        503: {"model": ErrorResponse, "description": "Service unavailable (AI error)"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def generate_etp(request: ETPGenerateRequest) -> ETPGenerateResponse:
    """
    Generate ETP (Estudo Técnico Preliminar) using AI.
    
    Args:
        request: ETP generation request with object details
        
    Returns:
        Generated ETP content
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        ai_service = get_ai_service()
        etp_content = ai_service.generate_etp(request)
        
        return ETPGenerateResponse(
            etp_content=etp_content,
            success=True,
            message="ETP gerado com sucesso"
        )
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"ETP generation failed: {error_msg}")
        
        # Return 503 for AI service errors (Vertex AI failures, safety filters)
        if "Vertex AI" in error_msg or "safety" in error_msg.lower() or "blocked" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "error": "AI service unavailable",
                    "detail": error_msg
                }
            )
        
        # Return 500 for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "detail": error_msg
            }
        )

