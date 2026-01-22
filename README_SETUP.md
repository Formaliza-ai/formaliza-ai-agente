# Setup Rápido - Gerador de ETP

## 1. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Para testar sem usar créditos da Vertex AI
MOCK_AI=True

# Quando estiver pronto para usar Vertex AI real:
# MOCK_AI=False
# GOOGLE_CLOUD_PROJECT_ID=seu-project-id
# GOOGLE_CLOUD_LOCATION=us-central1
# VERTEX_AI_MODEL=gemini-1.5-pro
```

## 2. Iniciar o Servidor

```bash
python3 main.py
```

## 3. Testar a API

### Opção A: Usando o script Python
```bash
python3 test_etp.py
```

### Opção B: Usando curl (no WSL/Linux)
```bash
curl -X POST http://localhost:8000/api/v1/etp/generate \
  -H "Content-Type: application/json" \
  -d '{
    "objeto": "Notebooks para Laboratório",
    "quantidade": 50,
    "especificacao_bruta": "i5 ou similar, 16gb ram, ssd 512, windows pro. Garantia 2 anos.",
    "justificativa_uso": "Aulas de programação e pesquisa para alunos do fundamental.",
    "origem_recurso": "FUNDEB"
  }'
```

## 4. Verificar Logs

O servidor mostrará no console:
- Se está usando MOCK_AI ou Vertex AI real
- Erros de inicialização
- Status das requisições

