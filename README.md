# formaliza-ai-agente

API para geração automática de Estudos Técnicos Preliminares (ETP) usando Google Vertex AI (Gemini 1.5 Pro).

## 🎯 Sobre o Projeto

Sistema que automatiza a criação de Estudos Técnicos Preliminares para compras públicas, combinando:
- **Lei 14.133/2021** (Lei de Licitações)
- **Templates institucionais** da Prefeitura
- **IA Generativa** (Gemini 1.5 Pro via Vertex AI)

## 🚀 Tecnologias

- **Python 3.11+**
- **FastAPI** (API REST)
- **Google Vertex AI SDK** (Gemini 1.5 Pro)
- **Pydantic** (Validação de dados)
- **python-dotenv** (Variáveis de ambiente)

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Conta Google Cloud com Vertex AI habilitado (ou modo mock para testes)
- Credenciais do Google Cloud configuradas

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Formaliza-ai/formaliza-ai-agente.git
cd formaliza-ai-agente
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto:

```env
# Modo Mock (para testes sem usar créditos)
MOCK_AI=True

# Configuração Vertex AI (quando estiver pronto)
# MOCK_AI=False
# GOOGLE_CLOUD_PROJECT_ID=seu-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
# VERTEX_AI_MODEL=gemini-2.0-flash-001
```

## 🏃 Como Executar

Inicie o servidor:

```bash
python main.py
```

A API estará disponível em:
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 📡 Endpoints

### POST `/api/v1/etp/generate`

Gera um ETP completo baseado nos dados fornecidos.

**Request Body:**
```json
{
  "objeto": "Notebooks para Laboratório",
  "quantidade": 50,
  "especificacao_bruta": "i5 ou similar, 16gb ram, ssd 512, windows pro. Garantia 2 anos.",
  "justificativa_uso": "Aulas de programação e pesquisa para alunos do fundamental.",
  "origem_recurso": "FUNDEB"
}
```

**Response:**
```json
{
  "etp_content": "...",
  "success": true,
  "message": "ETP gerado com sucesso"
}
```

## 🧪 Testes

Execute o script de teste:

```bash
python test_etp.py
```

## 📁 Estrutura do Projeto

```
formaliza-ai-agente/
├── app/
│   ├── api/          # Endpoints FastAPI
│   ├── core/         # Configurações e utilitários
│   ├── schemas/      # Modelos Pydantic
│   └── services/     # Lógica de negócio (AI Service)
├── data/             # Arquivos de contexto (Lei + Templates)
├── docs/             # Documentação
├── main.py           # Entry point
└── requirements.txt  # Dependências
```

## 🔒 Segurança

- Nunca commite arquivos `.env` com credenciais
- Use variáveis de ambiente para configurações sensíveis
- Em produção, configure CORS adequadamente

## 📝 Licença

Este projeto é privado e pertence à FormalizaAI.

## 🤝 Contribuindo

Para contribuições, abra uma issue ou pull request.

