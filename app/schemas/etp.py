"""ETP generation request and response schemas."""

from pydantic import BaseModel, Field


class ETPGenerateRequest(BaseModel):
    """Request schema for ETP generation."""
    
    objeto: str = Field(..., description="Objeto da contratação (ex: Notebooks para Laboratório)")
    quantidade: int = Field(..., gt=0, description="Quantidade de itens")
    especificacao_bruta: str = Field(..., description="Especificação técnica bruta do item")
    justificativa_uso: str = Field(..., description="Justificativa do uso/necessidade")
    origem_recurso: str = Field(..., description="Origem do recurso (ex: FUNDEB)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "objeto": "Notebooks para Laboratório",
                "quantidade": 50,
                "especificacao_bruta": "i5 ou similar, 16gb ram, ssd 512, windows pro. Garantia 2 anos.",
                "justificativa_uso": "Aulas de programação e pesquisa para alunos do fundamental.",
                "origem_recurso": "FUNDEB"
            }
        }


class ETPGenerateResponse(BaseModel):
    """Response schema for ETP generation."""
    
    etp_content: str = Field(..., description="Conteúdo completo do ETP gerado")
    success: bool = Field(..., description="Indica se a geração foi bem-sucedida")
    message: str = Field(default="ETP gerado com sucesso", description="Mensagem de status")


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Mensagem de erro")
    detail: str = Field(default="", description="Detalhes adicionais do erro")

