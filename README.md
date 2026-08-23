# 🏢 PrediALL Facilidades
## Agente de Manutenção Predial com IA

Aplicação para abertura, triagem e acompanhamento de chamados de manutenção predial com agente conversacional integrado.

### Stack Tecnológica (100% Gratuita)
| Componente | Tecnologia | Custo |
|-----------|-----------|-------|
| Frontend/Interface | Streamlit | Grátis (Streamlit Cloud) |
| Banco de Dados | Supabase (PostgreSQL) | Grátis (500MB) |
| Agente IA (LLM) | Google Gemini API | Grátis (15 req/min) |
| RAG / Embeddings | ChromaDB + Sentence Transformers | Grátis (local) |
| Notificações | Telegram Bot | Grátis |
| Deploy | Streamlit Cloud | Grátis |

### Arquitetura
```
[Streamlit - Interface Web]
        │
        ▼
[Python Backend]
        │
   ┌────┼──────────────────┐
   ▼    ▼                  ▼
[Gemini API]    [Supabase]    [Telegram Bot]
(Classificação   (PostgreSQL    (Notificações)
 + Chat IA)      Chamados)
        │
        ▼
[ChromaDB - RAG]
(Procedimentos, Normas, Catálogo)
```

### Como Rodar Localmente
```bash
# 1. Clonar o projeto
git clone <repo-url>
cd PrediALL-Facilidades

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves (Supabase, Gemini, Telegram)

# 4. Inicializar banco de dados
python setup_database.py

# 5. Carregar base de conhecimento (RAG)
python setup_knowledge_base.py

# 6. Rodar a aplicação
streamlit run app.py
```

### Estrutura do Projeto
```
📁 PrediALL Facilidades/
├── app.py                      ← Entrada principal Streamlit
├── requirements.txt            ← Dependências Python
├── .env.example                ← Template de variáveis de ambiente
├── setup_database.py           ← Script para criar tabelas no Supabase
├── setup_knowledge_base.py     ← Script para indexar documentos no ChromaDB
├── 📁 pages/
│   ├── 1_💬_Chat_Agente.py     ← Interface de chat com IA
│   ├── 2_📋_Novo_Chamado.py    ← Formulário estruturado
│   ├── 3_📊_Meus_Chamados.py   ← Lista e status dos chamados
│   └── 4_📈_Painel_Gestor.py   ← Dashboard KPIs
├── 📁 services/
│   ├── ai_agent.py             ← Lógica do agente (Gemini + prompts)
│   ├── database.py             ← Operações Supabase
│   ├── rag.py                  ← Busca vetorial (ChromaDB)
│   └── notifications.py       ← Telegram Bot
├── 📁 knowledge_base/
│   ├── procedimentos.md        ← Documentos para RAG
│   └── catalogo_ocorrencias.md ← Catálogo de problemas
└── 📁 docs/
    ├── guia-implementacao.md
    └── seguranca-e-governanca.md
```

### Deploy no Streamlit Cloud
1. Suba o código no GitHub
2. Acesse share.streamlit.io
3. Conecte o repositório
4. Configure os Secrets (chaves API)
5. Deploy automático!
