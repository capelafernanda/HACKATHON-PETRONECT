# PETRONECT INTELIGENTE

## Transformando comportamento em oportunidades de negócio

Protótipo desenvolvido para o Hackathon Conexão Ancestral / Petronect.

O projeto demonstra como dados de acesso e navegação dos fornecedores podem ser transformados em informações para apoiar decisões de reengajamento.

## Problema

O portal consegue acompanhar o volume de acessos, mas o desafio é entender melhor:

- quem está acessando;
- o que o fornecedor está buscando;
- quais oportunidades despertam interesse;
- quando uma proposta é abandonada;
- quais fornecedores precisam de reengajamento.

## Solução

O protótipo analisa uma base simulada de acessos e identifica padrões de comportamento.

O fluxo principal é:

**Dados de acesso → Análise de comportamento → Score de engajamento → Diagnóstico → Ação recomendada**

O sistema classifica os fornecedores em:

- Engajado
- Em risco
- Inativo

A partir do comportamento identificado, também recomenda ações de reengajamento, como:

- enviar novas oportunidades;
- incentivar a retomada de uma proposta;
- atualizar recomendações;
- enviar uma comunicação de retorno.

## Dashboard

O dashboard permite visualizar:

- total de acessos;
- propostas iniciadas, abandonadas e enviadas;
- telas mais acessadas;
- principais buscas;
- acessos por estado;
- nível de engajamento;
- fornecedores em atenção;
- ação recomendada para cada fornecedor.

Também é possível selecionar um fornecedor e visualizar um diagnóstico individual, além de simular uma comunicação personalizada.

## Tecnologias

- Python
- Pandas
- Streamlit
- Git / GitHub

## Estrutura do projeto

`gerar_dados.py`  
Gera a base simulada de acessos dos fornecedores.

`analisar_dados.py`  
Analisa os dados, calcula o score de engajamento e define o status e a ação recomendada.

`dashboard.py`  
Apresenta os dados e análises em um dashboard interativo.

`dados_fornecedores.csv`  
Base simulada de acessos.

`resumo_fornecedores.csv`  
Resumo dos fornecedores com indicadores de comportamento, score, status e ação recomendada.

## Como executar

Instale as dependências:

```bash
pip install pandas streamlit