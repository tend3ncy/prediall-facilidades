# Guia de Implementação — Stack Gratuita

## Streamlit + Supabase + Google Gemini + ChromaDB

---

## Fase 1: Configurar Ambiente (30 min)

### 1.1 Criar ambiente Python
```bash
# Criar pasta do projeto (já feito)
cd "PrediALL Facilidades"

# Criar virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 1.2 Criar projeto no Supabase (grátis)
1. Acesse https://supabase.com → Sign Up (GitHub login)
2. Clique "New Project"
3. Escolha região (South America - São Paulo)
4. Anote a senha do banco
5. Aguarde provisionamento (~2 min)

### 1.3 Obter API Key do Google Gemini (grátis)
1. Acesse https://aistudio.google.com/apikey
2. Clique "Create API Key"
3. Copie a chave gerada

### 1.4 Criar Bot no Telegram (opcional, grátis)
1. No Telegram, procure @BotFather
2. Envie `/newbot`
3. Defina nome e username
4. Copie o token gerado
5. Crie um grupo e adicione o bot
6. Descubra o chat_id via https://api.telegram.org/bot{TOKEN}/getUpdates

### 1.5 Configurar .env
```bash
cp .env.example .env
# Edite .env com as chaves obtidas acima
```

---

## Fase 2: Configurar Banco de Dados (10 min)

### 2.1 Executar SQL no Supabase
1. No dashboard do Supabase, vá em "SQL Editor"
2. Execute o script:
```bash
python setup_database.py
# Copie o SQL exibido e cole no Supabase SQL Editor
```
3. Clique "Run" no Supabase

### 2.2 Verificar
- Vá em "Table Editor" no Supabase
- Confirme que a tabela `chamados` foi criada
- Os dados de exemplo devem aparecer (5 chamados)

---

## Fase 3: Configurar Base de Conhecimento / RAG (5 min)

```bash
python setup_knowledge_base.py
```

Isso indexa 11 documentos no ChromaDB (procedimentos, normas, catálogo).
A pasta `chroma_data/` será criada automaticamente.

---

## Fase 4: Rodar a Aplicação (1 min)

```bash
streamlit run app.py
```

Acesse: http://localhost:8501

### Testar o fluxo completo:
1. Faça login (qualquer nome/email)
2. Abra o Chat com Agente IA
3. Diga: "O ar-condicionado da sala 405 está vazando"
4. O agente vai perguntar a urgência e coletar dados
5. Confirme e o chamado será criado no Supabase
6. Verifique em "Meus Chamados"

---

## Fase 5: Deploy no Streamlit Cloud (10 min)

### 5.1 Subir código no GitHub
```bash
git init
git add .
git commit -m "feat: PrediALL Facilidades - MVP completo"
git remote add origin https://github.com/seu-usuario/prediall-facilidades.git
git push -u origin main
```

### 5.2 Deploy
1. Acesse https://share.streamlit.io
2. Faça login com GitHub
3. Clique "New app"
4. Selecione o repositório
5. Branch: main
6. Main file: app.py
7. Em "Advanced settings" → Secrets, adicione:
```toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJ..."
GEMINI_API_KEY = "AIza..."
TELEGRAM_BOT_TOKEN = "123456:ABC..."
TELEGRAM_CHAT_ID = "-100..."
```
8. Clique "Deploy"

### 5.3 Pronto!
Sua URL será: https://seu-app.streamlit.app

---

## Custos Reais

| Serviço | Free Tier | Limite |
|---------|-----------|--------|
| Streamlit Cloud | ✅ Grátis | 1 app público |
| Supabase | ✅ Grátis | 500MB banco, 1GB storage, 50k rows |
| Google Gemini | ✅ Grátis | 15 req/min, 1M tokens/dia |
| ChromaDB | ✅ Grátis | Local (sem limite) |
| Telegram Bot | ✅ Grátis | Sem limite |
| **TOTAL** | **R$ 0,00** | Suficiente para MVP e uso moderado |

### Quando precisaria pagar?
- Supabase: > 500MB de dados ou > 50k chamados → US$ 25/mês
- Gemini: > 1M tokens/dia ou precisa de GPT-4 quality → US$ 0-20/mês
- Streamlit: App privado ou mais recursos → US$ 0 (Community) ou empresarial

---

## Cronograma Real

| Etapa | Tempo | Pré-requisito |
|-------|-------|---------------|
| Setup ambiente | 30 min | Python instalado |
| Config Supabase | 10 min | Conta criada |
| Config RAG | 5 min | - |
| Testar local | 15 min | - |
| Deploy | 10 min | GitHub |
| **Total** | **~1 hora** | |
