#!/usr/bin/env python3
"""Script simples para testar a API de geração de ETP."""

import json
import sys

try:
    import requests
except ImportError:
    print("ERRO: Biblioteca 'requests' não encontrada.")
    print("Instale com: pip install requests")
    sys.exit(1)

url = "http://localhost:8000/api/v1/etp/generate"

payload = {
    "objeto": "Notebooks para Laboratório",
    "quantidade": 50,
    "especificacao_bruta": "i5 ou similar, 16gb ram, ssd 512, windows pro. Garantia 2 anos.",
    "justificativa_uso": "Aulas de programação e pesquisa para alunos do fundamental.",
    "origem_recurso": "FUNDEB"
}

print("=" * 70)
print("TESTE DA API - Geração de ETP (Caso: Notebooks)")
print("=" * 70)
print(f"\nURL: {url}")
print(f"\nPayload:")
print(json.dumps(payload, indent=2, ensure_ascii=False))
print("\n" + "=" * 70)
print("Enviando requisição...\n")

try:
    response = requests.post(url, json=payload, timeout=30)
    
    print(f"Status: {response.status_code}")
    print("=" * 70)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCESSO!")
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        print("\n" + "=" * 70)
        print("CONTEÚDO DO ETP GERADO:")
        print("=" * 70)
        print(data.get('etp_content', ''))
    else:
        print(f"\n❌ ERRO {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2, ensure_ascii=False))
        except:
            print(response.text)
            
except requests.exceptions.ConnectionError:
    print("❌ ERRO: Não foi possível conectar ao servidor.")
    print("\nCertifique-se de que o servidor está rodando:")
    print("  python3 main.py")
    print("\nE que está acessível em: http://localhost:8000")
except requests.exceptions.Timeout:
    print("❌ ERRO: Timeout na requisição (pode estar aguardando resposta da Vertex AI)")
except Exception as e:
    print(f"❌ ERRO: {type(e).__name__}: {str(e)}")

