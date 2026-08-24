# Fluxogramas Mermaid — Agente de Manutenção Predial

> Cole os blocos abaixo no Obsidian dentro de blocos ` ```mermaid ` para renderizar.

---

## 1. Fluxo Geral do Agente (Triagem e Encaminhamento)

```mermaid
flowchart TD
    A[Solicitação recebida] --> B{Canal de entrada}
    B --> |E-mail| C[Camada de Orquestração]
    B --> |Chat Teams| C
    B --> |Formulário Web| C
    
    C --> D[Agente Conversacional]
    D --> E{Dados completos?}
    
    E --> |Não| F[Coleta dados faltantes via diálogo]
    F --> E
    
    E --> |Sim| G[Classificação automática]
    G --> H{Confiança ≥ 80%?}
    
    H --> |Não| I[🧑 Escalar para triagem humana]
    H --> |Sim| J{Qual prioridade?}
    
    J --> |Crítica| K[⚠️ Escalar equipe de segurança + Notificar gestor]
    J --> |Alta| L[Criar chamado + Notificar técnico de plantão]
    J --> |Normal / Baixa| M[Criar chamado + Fila padrão]
    
    L --> N[Registrar no CMMS via API]
    M --> N
    K --> N
    
    N --> O[Confirmar ao solicitante: nº + previsão]
    O --> P[Acompanhamento de status]
    P --> Q{Chamado concluído?}
    
    Q --> |Não| P
    Q --> |Sim| R[Pesquisa de satisfação automática]
    R --> S[Atualizar indicadores no BI]
```

---

## 2. Fluxo RAG (Retrieval-Augmented Generation)

```mermaid
flowchart TD
    A[Usuário descreve o problema] --> B[Gerar embedding da descrição]
    B --> C[Busca vetorial na base de conhecimento]
    
    C --> D[Procedimentos de Manutenção]
    C --> E[Orientações de Segurança]
    C --> F[Catálogo de Ocorrências]
    
    D --> G[Top-K trechos relevantes]
    E --> G
    F --> G
    
    G --> H[Montar prompt com contexto recuperado]
    H --> I[LLM gera resposta fundamentada]
    I --> J{Encontrou informação suficiente?}
    
    J --> |Sim| K[Resposta com citação da fonte + Classificação]
    J --> |Não| L[Informar necessidade de apoio humano]
```

---

## 3. Arquitetura Geral do Sistema

```mermaid
flowchart TD
    subgraph Canais["📨 Canais de Entrada"]
        CH1[E-mail]
        CH2[Chat Teams]
        CH3[Formulário Web]
    end

    subgraph Orquestração["⚙️ Camada de Orquestração"]
        OQ[Power Automate / n8n]
    end

    subgraph Agente["🤖 Agente Conversacional"]
        AG1[Classificação de Ocorrência]
        AG2[Coleta de Dados]
        AG3[Consulta RAG]
        AG4[Geração de Resposta]
    end

    subgraph Backends["🗄️ Sistemas Integrados"]
        BV[(Base Vetorial - Embeddings)]
        CMMS[(CMMS - Chamados)]
        NT[Notificações - Teams/E-mail]
    end

    subgraph Governança["🔒 Governança e Segurança"]
        RBAC[Controle de Acesso - RBAC]
        LOG[Logs de Auditoria]
        CRYPT[Criptografia TLS + AES-256]
    end

    subgraph BI["📊 Painel de Indicadores"]
        KPI1[Tempo de Abertura]
        KPI2[TMA]
        KPI3[Reaberturas]
        KPI4[Satisfação]
    end

    CH1 --> OQ
    CH2 --> OQ
    CH3 --> OQ
    OQ --> Agente
    AG3 --> BV
    AG4 --> CMMS
    AG4 --> NT
    CMMS --> BI
    Agente --> Governança
```

---

## 4. Fluxo de Participação Humana (Escalação)

```mermaid
flowchart TD
    A[Agente processa solicitação] --> B{Tipo de situação}
    
    B --> |Emergência / Risco| C[🚨 Escalar imediatamente]
    C --> C1[Equipe de Segurança / Brigada]
    
    B --> |Custo acima do limite| D[💰 Solicitar aprovação]
    D --> D1[Gestor de Facilities]
    
    B --> |Classificação ambígua| E[❓ Transferir para humano]
    E --> E1[Atendente de Triagem]
    
    B --> |Reclamação recorrente 3+| F[🔄 Alertar coordenador]
    F --> F1[Investigação de Causa-Raiz]
    
    B --> |Fora do escopo| G[🏗️ Redirecionar]
    G --> G1[Setor de Projetos / Engenharia]
    
    B --> |Situação normal| H[✅ Continuar fluxo automático]
```

---

## 5. Fluxo de Integração com CMMS

```mermaid
sequenceDiagram
    participant U as Solicitante
    participant AG as Agente
    participant API as API CMMS
    participant TEC as Equipe Técnica

    U->>AG: Descreve o problema
    AG->>U: Solicita dados faltantes
    U->>AG: Complementa informações
    AG->>AG: Classifica ocorrência + Define prioridade
    AG->>API: POST /ordens-servico (dados estruturados)
    API-->>AG: Retorna nº do chamado
    AG->>U: Confirma abertura (nº + previsão SLA)
    API->>TEC: Webhook - Novo chamado atribuído
    TEC->>API: PUT /ordens-servico/{id} (status: em andamento)
    API-->>AG: Webhook - Status atualizado
    AG->>U: Notifica: "Seu chamado está em atendimento"
    TEC->>API: PUT /ordens-servico/{id} (status: concluído)
    API-->>AG: Webhook - Chamado concluído
    AG->>U: Pesquisa de satisfação
    U->>AG: Avaliação (nota + comentário)
```

---

## Como usar no Obsidian

1. Certifique-se de que o plugin **Mermaid** está ativo (já vem nativo no Obsidian).
2. Copie qualquer bloco acima (incluindo ` ```mermaid ` e ` ``` `).
3. Cole em uma nota `.md` no Obsidian.
4. Alterne para o modo de leitura (Preview) para ver o diagrama renderizado.
