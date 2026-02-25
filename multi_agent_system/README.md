# Multi Agent System com LangChain

Projeto completo em Python para orquestrar um **time de 5 agentes autônomos colaborativos** com LangChain.

## ✅ Agentes implementados

1. **Agente de Pesquisa** (`research_agent.py`)
2. **Agente de Análise de Dados** (`data_analysis_agent.py`)
3. **Agente de Planejamento Estratégico** (`planning_agent.py`)
4. **Agente de Crítica e Validação** (`critic_agent.py`)
5. **Agente Coordenador / Orquestrador** (`coordinator_agent.py`)

## Arquitetura

```text
multi_agent_system/
│
├── agents/
│   ├── messages.py
│   ├── research_agent.py
│   ├── data_analysis_agent.py
│   ├── planning_agent.py
│   ├── critic_agent.py
│   └── coordinator_agent.py
│
├── tools/
│   ├── web_tools.py
│   ├── github_tools.py
│   └── data_tools.py
│
├── memory/
│   └── shared_memory.py
│
├── utils/
│   ├── logger.py
│   └── llm_factory.py
│
├── config.py
├── main.py
└── requirements.txt
```

## Principais características

- Arquitetura modular e escalável
- Ferramentas (tools) com `langchain_core.tools.tool`
- Memória compartilhada thread-safe entre agentes
- Mensagens estruturadas com Pydantic
- Logging detalhado por agente
- Execução assíncrona no orquestrador
- Retry + timeout por estágio
- Fácil troca de modelo via variáveis de ambiente

## Fluxo de execução

1. Usuário envia a consulta.
2. Coordenador chama o **Agente de Pesquisa**.
3. Resultado passa ao **Agente de Análise de Dados**.
4. Saída vai para **Planejamento Estratégico**.
5. **Crítico** valida consistência e lacunas.
6. Coordenador consolida saída final em JSON.

## Setup

```bash
cd multi_agent_system
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração de modelo

Variáveis suportadas:

- `MODEL_PROVIDER` (default: `openai`)
- `MODEL_NAME` (default: `gpt-4o-mini`)
- `MODEL_TEMPERATURE` (default: `0.2`)
- `AGENT_MAX_RETRIES` (default: `2`)
- `AGENT_TIMEOUT_SECONDS` (default: `45`)
- `LOG_LEVEL` (default: `INFO`)

Exemplo com OpenAI:

```bash
export OPENAI_API_KEY="sua_chave"
export MODEL_PROVIDER="openai"
export MODEL_NAME="gpt-4o-mini"
```

## Execução via CLI

```bash
python -m multi_agent_system.main "Analise o ecossistema LangChain e proponha um plano de adoção para uma startup B2B"
```

## Exemplo de saída (resumido)

```json
{
  "query": "Analise o ecossistema LangChain...",
  "research": {"summary": "...", "sources": []},
  "analysis": {"metrics": {}, "insights": []},
  "planning": {"priorities": [], "roadmap": []},
  "critique": {"consistency_score": 0.86, "recommendations": []},
  "status": "completed"
}
```

## Expansão futura

- Incluir execução híbrida sequencial/grafo (LangGraph)
- Adicionar roteamento dinâmico por tipo de consulta
- Persistir memória em Redis/Postgres
- Incluir testes automatizados por agente
- Adicionar novas tools de domínio (financeiro, jurídico etc.)
