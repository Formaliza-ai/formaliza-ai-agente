# Technical Specification

## 1. Arquitetura de Prompting (The "Sandwich" Strategy)
O `AIService` deve montar o prompt dinamicamente seguindo esta ordem:

**[PARTE 1: SYSTEM ROLE & LEGAL GROUNDING]**
"Você é um Auditor de Licitações Especialista. Use EXCLUSIVAMENTE a Lei 14.133/2021 fornecida abaixo para justificar suas decisões.
[CONTEÚDO DO ARQUIVO lei_14133.txt]"

**[PARTE 2: STYLE REFERENCE (Few-Shot)]**
"Você deve escrever seguindo estritamente o tom de voz, cabeçalhos e estrutura do exemplo abaixo (Prefeitura de Torres). Não invente seções novas.
[CONTEÚDO DO ARQUIVO template_etp_torres.txt]"

**[PARTE 3: USER TASK]**
"Agora, gere um NOVO ETP para o seguinte pedido:
Objeto: {request.objeto}
Specs: {request.specs}
..."

## 2. Definição da API (FastAPI)

### `POST /api/v1/etp/generate`
**Request Body:**
```json
{
  "objeto": "Notebooks para Laboratório",
  "quantidade": 50,
  "especificacao_bruta": "i5 ou similar, 16gb ram, ssd 512, windows pro. Garantia 2 anos.",
  "justificativa_uso": "Aulas de programação e pesquisa para alunos do fundamental.",
  "origem_recurso": "FUNDEB"
}