"""AI Service for ETP generation using Vertex AI (Gemini 1.5 Pro)."""

import logging
from typing import Optional

from vertexai.preview.generative_models import GenerativeModel
import vertexai

from app.core.config import (
    PROJECT_ID,
    LOCATION,
    MODEL_NAME,
    MOCK_AI,
    load_context_files
)
from app.schemas.etp import ETPGenerateRequest

logger = logging.getLogger(__name__)


class AIService:
    """Service for generating ETPs using Vertex AI with Sandwich Prompting strategy."""
    
    def __init__(self):
        """Initialize AI service and load context files."""
        self.lei_content: Optional[str] = None
        self.template_content: Optional[str] = None
        self.model: Optional[GenerativeModel] = None
        
        # Load context files at initialization
        try:
            self.lei_content, self.template_content = load_context_files()
            logger.info("Context files loaded successfully")
        except FileNotFoundError as e:
            logger.error(f"Failed to load context files: {e}")
            raise
        
        # Initialize Vertex AI if not in mock mode
        if not MOCK_AI:
            if not PROJECT_ID:
                logger.warning("GOOGLE_CLOUD_PROJECT_ID not set. Vertex AI will not be available.")
                logger.warning("Set MOCK_AI=True in .env to use mock responses for testing.")
                self.model = None
            else:
                try:
                    logger.info(f"Initializing Vertex AI with project: {PROJECT_ID}, location: {LOCATION}")
                    vertexai.init(project=PROJECT_ID, location=LOCATION)
                    self.model = GenerativeModel("gemini-2.0-flash-001")
                    logger.info(f"Vertex AI initialized successfully with model: gemini-2.0-flash-001")
                except Exception as e:
                    logger.error(f"Failed to initialize Vertex AI: {e}")
                    logger.warning("Falling back to None. Set MOCK_AI=True to use mock responses.")
                    self.model = None
    
    def _build_sandwich_prompt(self, request: ETPGenerateRequest) -> str:
        """
        Build prompt using Sandwich Prompting strategy.
        
        Strategy:
        1. SYSTEM ROLE & LEGAL GROUNDING (Lei 14.133)
        2. STYLE REFERENCE (Template ETP Torres)
        3. USER TASK (Request details)
        
        Args:
            request: ETP generation request
            
        Returns:
            Complete prompt string
        """
        # PARTE 1: SYSTEM ROLE & LEGAL GROUNDING
        system_prompt = f"""Você é um Auditor de Licitações Especialista. Use EXCLUSIVAMENTE a Lei 14.133/2021 fornecida abaixo para justificar suas decisões.

{self.lei_content}

---

"""
        
        # PARTE 2: STYLE REFERENCE (Few-Shot)
        style_reference = f"""Você deve escrever seguindo estritamente o tom de voz, cabeçalhos e estrutura do exemplo abaixo (Prefeitura de Torres). Não invente seções novas.

{self.template_content}

---

"""
        
        # PARTE 3: USER TASK
        user_task = f"""Agora, gere um NOVO ETP para o seguinte pedido:

OBJETO: {request.objeto}
QUANTIDADE: {request.quantidade}
ESPECIFICAÇÃO BRUTA: {request.especificacao_bruta}
JUSTIFICATIVA DE USO: {request.justificativa_uso}
ORIGEM DO RECURSO: {request.origem_recurso}

Gere o ETP completo seguindo a estrutura do template fornecido, adaptando os campos conforme os dados acima. Mantenha o tom formal e técnico da Prefeitura de Torres."""

        # Combine all parts
        full_prompt = system_prompt + style_reference + user_task
        
        return full_prompt
    
    def generate_etp(self, request: ETPGenerateRequest) -> str:
        """
        Generate ETP content using Vertex AI.
        
        Args:
            request: ETP generation request
            
        Returns:
            Generated ETP content as string
            
        Raises:
            Exception: If generation fails or is blocked by safety filters
        """
        # Mock mode for development/testing
        if MOCK_AI:
            logger.info("Using MOCK_AI mode - returning placeholder response")
            return self._get_mock_response(request)
        
        # Verify model is initialized
        if self.model is None:
            raise Exception("Vertex AI model not initialized. Check GOOGLE_CLOUD_PROJECT_ID and credentials.")
        
        try:
            # Build prompt using Sandwich strategy
            prompt = self._build_sandwich_prompt(request)
            
            # Generate response using Vertex AI
            logger.info(f"Iniciando chamada Vertex AI para o projeto {PROJECT_ID} com modelo gemini-2.0-flash-001")
            logger.debug(f"Prompt length: {len(prompt)} characters")
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 8192,
                    "temperature": 0.7,
                }
            )
            
            # Extract text from response
            if hasattr(response, 'text') and response.text:
                etp_content = response.text
                logger.info("ETP generated successfully")
                return etp_content
            else:
                raise Exception("Vertex AI returned empty response")
                
        except Exception as e:
            error_msg = str(e)
            error_lower = error_msg.lower()
            
            # Check for 404 errors (model not found) and try fallback
            if "404" in error_msg or "not found" in error_lower:
                logger.warning(f"Model gemini-2.0-flash-001 not available (404). Attempting fallback to gemini-2.0-flash-lite-001...")
                try:
                    # Try fallback model (lighter version, more widely available)
                    fallback_model = GenerativeModel("gemini-2.0-flash-lite-001")
                    logger.info(f"Iniciando chamada Vertex AI para o projeto {PROJECT_ID} com modelo fallback gemini-2.0-flash-lite-001")
                    
                    response = fallback_model.generate_content(
                        prompt,
                        generation_config={
                            "max_output_tokens": 8192,
                            "temperature": 0.7,
                        }
                    )
                    
                    if hasattr(response, 'text') and response.text:
                        etp_content = response.text
                        logger.info("ETP generated successfully using fallback model gemini-2.0-flash-lite-001")
                        return etp_content
                    else:
                        raise Exception("Fallback model returned empty response")
                        
                except Exception as fallback_error:
                    logger.error(f"Fallback model also failed: {str(fallback_error)}")
                    raise Exception(f"Both primary (gemini-2.0-flash-001) and fallback (gemini-2.0-flash-lite-001) models failed. Last error: {str(fallback_error)}")
            
            # Check for safety filter blocks
            if "safety" in error_lower or "blocked" in error_lower:
                raise Exception(f"Content blocked by safety filters: {error_msg}")
            
            # Check for authentication/credential errors
            if "credentials" in error_lower or "authentication" in error_lower or "permission" in error_lower:
                raise Exception(f"Authentication error: {error_msg}. Check GOOGLE_APPLICATION_CREDENTIALS or gcloud auth.")
            
            # Re-raise other errors
            raise Exception(f"Vertex AI generation failed: {error_msg}")
    
    def _get_mock_response(self, request: ETPGenerateRequest) -> str:
        """
        Generate mock ETP response for development/testing.
        
        Args:
            request: ETP generation request
            
        Returns:
            Mock ETP content
        """
        return f"""PREFEITURA DE TORRES - SECRETARIA DE EDUCAÇÃO - Cuidando da gente
ESTUDO TÉCNICO PRELIMINAR

1. OBJETO
O presente documento visa planejar o FORNECIMENTO FUTURO E PARCELADO DE {request.objeto.upper()} PARA A REDE MUNICIPAL DE ENSINO.

2. INFORMAÇÕES BÁSICAS
Responsáveis: Secretário de Educação
Objetivo: Demonstrar viabilidade técnica e econômica para subsidiar a tomada de decisão.

3. ESPECIFICAÇÃO TÉCNICA

| Item | Unidade | Quantidade | Descritivo Técnico Detalhado |
|------|---------|------------|------------------------------|
| {request.objeto} | Unidade | {request.quantidade} | {request.especificacao_bruta} |

4. FUNDAMENTAÇÃO LEGAL
Fundamenta-se na Lei 14.133/2021, especialmente nos Artigos 18, 40 e 42, que estabelecem a obrigatoriedade do planejamento de contratações e do estudo técnico preliminar.

5. MATRIZ DE RISCOS

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Entrega fora do prazo | Média | Alto | Multas e fiscalização |
| Especificações inadequadas | Baixa | Médio | Revisão técnica prévia |

6. JUSTIFICATIVA
{request.justificativa_uso}

7. ORIGEM DO RECURSO
{request.origem_recurso}

Data: [Data atual]
Assinatura Digital: [Secretário de Educação]
"""

