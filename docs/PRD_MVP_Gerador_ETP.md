# Product Requirements Document (PRD) - Gerador de ETP GovTech
**Versão:** 0.1 (MVP Local)
**Objetivo:** Automatizar a criação do "Estudo Técnico Preliminar" (ETP) para compras públicas.

## 1. O Problema
Servidores públicos gastam horas escrevendo justificativas técnicas e jurídicas. Eles sabem *o que* comprar (ex: Notebooks), mas não sabem *como* escrever isso no formato exigido pela Lei 14.133/2021 e nos padrões da prefeitura.

## 2. A Solução
Uma API que recebe uma especificação simples (linguagem natural) e gera um documento ETP completo, profissional e juridicamente embasado, mimetizando o estilo de documentos anteriores de sucesso.

## 3. User Story (Caso de Teste: Notebooks)
**Como:** Secretário de Educação.
**Quero:** Enviar o pedido: "Preciso de 50 notebooks i5, 16GB RAM para os laboratórios, verba do FUNDEB".
**Para:** Receber um texto estruturado contendo:
    1. Objeto Formalizado.
    2. Justificativa Pedagógica e Legal (Citando Art. 40 da Lei 14.133).
    3. Especificação Técnica Refinada (convertendo "i5" para "Processador 6 núcleos...").
    4. Matriz de Riscos.
    5. Valor Estimado.

## 4. Requisitos Funcionais
- **Input:** JSON com `objeto`, `quantidade`, `detalhes_tecnicos`, `dotacao_orcamentaria`.
- **Processamento:** O backend deve combinar o Input + Lei + Template e enviar ao Gemini 1.5 Pro.
- **Output:** JSON com o texto do documento formatado em Markdown/HTML, pronto para exportação.