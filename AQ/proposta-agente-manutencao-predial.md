# AGENTE DE MANUTENÇÃO PREDIAL E FACILIDADES

## Proposta Conceitual — Bootcamp Low Code (Tema 2, Fases 4 e 5)

---

## 1. Definição do Problema

Uma empresa corporativa recebe diariamente solicitações relacionadas a iluminação, ar-condicionado, mobiliário, reserva de salas, limpeza e pequenos reparos. Esses pedidos chegam por múltiplos canais (e-mail, chat, telefone, formulários) e frequentemente estão incompletos — faltam dados como localização exata, tipo de problema ou grau de urgência. Isso gera retrabalho, atrasos no atendimento e insatisfação dos ocupantes do prédio.

### Principais Usuários

| Perfil | Descrição |
|--------|-----------|
| Colaboradores | Funcionários que reportam problemas ou solicitam serviços |
| Equipe de Facilities | Técnicos e coordenadores que executam e gerenciam os chamados |
| Gestores prediais | Responsáveis por indicadores, custos e contratos de manutenção |

---

## 2. Objetivo do Agente

Atuar como ponto único de entrada para solicitações de manutenção predial, garantindo que cada chamado seja registrado com informações completas, classificado corretamente e encaminhado à equipe adequada — reduzindo tempo de triagem e aumentando a taxa de resolução no primeiro atendimento.

---

## 3. Capacidades do Agente (mínimo 4)

1. **Identificação do tipo de ocorrência** — Classifica automaticamente a solicitação em categorias (elétrica, climatização, mobiliário, limpeza, infraestrutura, reserva de sala) com base na descrição do usuário.

2. **Coleta estruturada de informações** — Conduz um diálogo guiado para obter dados obrigatórios que estejam faltando (unidade, andar, sala, urgência, descrição detalhada, foto se aplicável).

3. **Consulta a procedimentos e base de conhecimento** — Recupera instruções relevantes (procedimentos de manutenção, orientações de segurança, catálogo de ocorrências) para validar a classificação e fornecer orientações imediatas ao solicitante.

4. **Registro e encaminhamento automático do chamado** — Cria o chamado no sistema de gestão (CMMS/ITSM), atribui prioridade, define responsável e notifica a equipe técnica.

5. **Acompanhamento e feedback** — Informa o solicitante sobre o status do chamado e coleta avaliação após a conclusão do atendimento.

---

## 4. Limites do Agente (mínimo 3)

1. **Não executa reparos nem toma decisões técnicas** — O agente apenas registra, classifica e encaminha. A execução física e decisões técnicas são responsabilidade dos profissionais de manutenção.

2. **Não autoriza gastos ou contratações** — Solicitações que envolvam orçamento, compra de materiais ou contratação de terceiros devem ser aprovadas por um gestor humano.

3. **Não atende emergências de segurança de forma autônoma** — Situações de risco (vazamento de gás, incêndio, risco elétrico grave) são imediatamente escaladas para a equipe de segurança/bombeiros, sem tentativa de resolução pelo agente.

4. **Não acessa dados pessoais além do necessário** — Restringe-se a informações funcionais (nome, ramal, localização) sem consultar dados sensíveis de RH ou financeiros.

---

## 5. Fontes de Conhecimento

| Fonte | Conteúdo | Formato |
|-------|----------|---------|
| Procedimentos de Manutenção | Passo-a-passo para cada tipo de reparo, SLAs, escalas de plantão | Documentos PDF/Word indexados |
| Orientações de Segurança | Normas NR-10, NR-35, procedimentos de evacuação, EPI obrigatório | Base vetorial (embeddings) |
| Catálogo de Tipos de Ocorrência | Taxonomia de problemas, campos obrigatórios por categoria, fluxos de aprovação | Tabela estruturada (banco de dados) |
| Histórico de Chamados | Chamados anteriores com resolução, tempo médio, reincidências | Data warehouse / CMMS |

---

## 6. RAG e Grounding — Como Funcionam na Solução

### RAG (Retrieval-Augmented Generation)

Quando o usuário descreve um problema, o agente:

1. Converte a descrição em um vetor (embedding).
2. Busca na base vetorial os trechos mais relevantes dos procedimentos de manutenção, orientações de segurança e catálogo de ocorrências.
3. Usa esses trechos como contexto para gerar uma resposta fundamentada — por exemplo, confirmar a classificação, sugerir ações imediatas ao usuário ou definir a prioridade.

### Grounding

O grounding garante que as respostas do agente estejam ancoradas em fontes reais e verificáveis:

- Toda resposta cita a fonte consultada (ex.: "Conforme Procedimento PM-042, seção 3.1...").
- O agente não inventa procedimentos; se não encontra informação na base, informa que precisa de apoio humano.
- Dados factuais (localização de quadros elétricos, contatos de emergência, horários de equipe) vêm de sistemas integrados, não de geração livre.

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUXO RAG SIMPLIFICADO                    │
│                                                             │
│  Usuário: "O ar-condicionado da sala 405 está vazando"      │
│       │                                                     │
│       ▼                                                     │
│  [Embedding da consulta]                                    │
│       │                                                     │
│       ▼                                                     │
│  [Busca vetorial] → Top-3 trechos relevantes:               │
│    • Procedimento PM-018: Vazamento em split                │
│    • Catálogo: Categoria "Climatização > Vazamento"         │
│    • Segurança: "Desligar equipamento antes de inspeção"    │
│       │                                                     │
│       ▼                                                     │
│  [LLM + Contexto recuperado]                                │
│       │                                                     │
│       ▼                                                     │
│  Resposta fundamentada + Chamado classificado               │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Diagrama Conceitual da Arquitetura

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ARQUITETURA DO AGENTE                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                    │
│  │   E-mail    │   │    Chat     │   │  Formulário │  ← CANAIS DE       │
│  │             │   │  (Teams)    │   │    Web      │    ENTRADA          │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                    │
│         │                 │                 │                            │
│         └────────────────┬┘─────────────────┘                            │
│                          ▼                                               │
│         ┌────────────────────────────────┐                               │
│         │      CAMADA DE ORQUESTRAÇÃO    │                               │
│         │   (Power Automate / n8n / API) │                               │
│         └────────────────┬───────────────┘                               │
│                          ▼                                               │
│         ┌────────────────────────────────┐                               │
│         │     AGENTE CONVERSACIONAL      │                               │
│         │         (LLM + Prompts)        │                               │
│         │                                │                               │
│         │  • Classificação de ocorrência │                               │
│         │  • Coleta de dados faltantes   │                               │
│         │  • Consulta RAG               │                               │
│         │  • Geração de resposta         │                               │
│         └───┬────────────┬───────────┬───┘                               │
│             │            │           │                                    │
│             ▼            ▼           ▼                                    │
│  ┌──────────────┐ ┌───────────┐ ┌────────────────┐                      │
│  │ BASE VETORIAL│ │   CMMS    │ │  NOTIFICAÇÕES  │                      │
│  │ (Embeddings) │ │ (Chamados)│ │ (Teams/E-mail) │                      │
│  │              │ │           │ │                │                      │
│  │• Procedim.   │ │• Criar    │ │• Equipe técnica│                      │
│  │• Segurança   │ │• Atualizar│ │• Solicitante   │                      │
│  │• Catálogo    │ │• Consultar│ │• Gestor        │                      │
│  └──────────────┘ └───────────┘ └────────────────┘                      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │              CAMADA DE DADOS E GOVERNANÇA                │            │
│  │  • Controle de acesso (RBAC)                             │            │
│  │  • Logs de auditoria                                     │            │
│  │  • Criptografia em trânsito e repouso                    │            │
│  └──────────────────────────────────────────────────────────┘            │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │              PAINEL DE INDICADORES (BI)                   │            │
│  │  • Tempo de abertura • SLA • Reaberturas • Satisfação    │            │
│  └──────────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Integração com Sistema

### Integração: Sistema de Gestão de Manutenção (CMMS)

| Aspecto | Detalhe |
|---------|---------|
| Sistema | CMMS (ex.: Fracttal, Manusis, ou módulo SAP PM) |
| Protocolo | API REST |
| Operações | Criar chamado, atualizar status, consultar histórico, atribuir responsável |
| Dados trafegados | Unidade, local, tipo de problema, urgência, responsável, status, descrição, anexos |
| Autenticação | OAuth 2.0 com token de serviço (service account) |

**Fluxo:**
1. Agente coleta todas as informações obrigatórias.
2. Chama a API `POST /ordens-servico` com os dados estruturados.
3. Recebe o número do chamado e informa ao solicitante.
4. Monitora webhooks de atualização de status para notificar o solicitante.

---

## 9. Automação de Processo

### Automação: Triagem e Encaminhamento Automático

```
┌───────────────────────────────────────────────────────────────┐
│              FLUXO AUTOMATIZADO DE TRIAGEM                     │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Solicitação recebida (qualquer canal)                     │
│       │                                                       │
│  2. Agente identifica tipo + coleta dados faltantes           │
│       │                                                       │
│  3. Classificação automática (categoria + prioridade)         │
│       │                                                       │
│       ├── Prioridade CRÍTICA ──→ Escala humano imediatamente  │
│       │                          + Notifica gestor            │
│       │                                                       │
│       ├── Prioridade ALTA ────→ Cria chamado + Notifica       │
│       │                          técnico de plantão           │
│       │                                                       │
│       └── Prioridade NORMAL/BAIXA → Cria chamado + Fila      │
│                                       padrão                  │
│                                                               │
│  4. Confirmação ao solicitante (número + previsão)            │
│                                                               │
│  5. Após resolução: pesquisa de satisfação automática         │
└───────────────────────────────────────────────────────────────┘
```

**Ferramenta de automação sugerida:** Power Automate (ambiente Microsoft) ou n8n (open-source).

---

## 10. Dados Principais e Cuidados de Segurança

### Dados Principais

| Campo | Tipo | Obrigatório |
|-------|------|-------------|
| Unidade | Texto (ex.: "Sede SP", "Filial RJ") | Sim |
| Local | Texto (ex.: "4º andar, sala 405") | Sim |
| Tipo de problema | Enumerado (catálogo) | Sim |
| Urgência | Enumerado (Crítica / Alta / Normal / Baixa) | Sim |
| Responsável | Atribuído automaticamente pela regra de negócio | Automático |
| Status | Enumerado (Aberto / Em andamento / Pendente / Concluído) | Automático |
| Solicitante | Nome + ramal/e-mail | Sim |
| Descrição | Texto livre | Sim |
| Anexos | Imagens/documentos | Opcional |

### Cuidados de Segurança

| Risco | Controle |
|-------|----------|
| Acesso indevido a chamados de outras áreas | RBAC — cada usuário vê apenas chamados da sua unidade; gestores veem consolidado |
| Vazamento de dados pessoais | Dados minimizados (apenas nome funcional e ramal); sem CPF, endereço residencial ou dados de saúde |
| Manipulação de prioridade | Apenas o agente ou gestor podem alterar prioridade após abertura; log de auditoria |
| Injeção de prompt / abuso do agente | Guardrails de conteúdo, limitação de escopo de conversa, detecção de tentativas de manipulação |
| Disponibilidade | Fallback para formulário web caso o agente esteja indisponível |
| Dados em trânsito | TLS 1.3 em todas as APIs |
| Dados em repouso | Criptografia AES-256 no banco de dados |

---

## 11. Situações que Exigem Participação Humana

| Situação | Motivo | Ação |
|----------|--------|------|
| Ocorrência de risco ou emergência (vazamento de gás, princípio de incêndio, risco elétrico) | Risco à vida; decisão técnica urgente | Escalar imediatamente para equipe de segurança + brigada |
| Solicitação com custo acima de limite pré-definido | Requer aprovação orçamentária | Encaminhar ao gestor de facilities para aprovação |
| Classificação ambígua (agente não consegue determinar categoria com confiança > 80%) | Evitar erro de encaminhamento | Transferir para atendente humano de triagem |
| Reclamação recorrente sem resolução (3+ chamados iguais em 30 dias) | Pode indicar problema sistêmico | Alertar coordenador para investigação de causa-raiz |
| Solicitação fora do escopo (ex.: mudança de layout, obra civil) | Requer planejamento e contrato | Redirecionar ao setor de projetos/engenharia |

---

## 12. Indicadores de Resultado (mínimo 4)

| # | Indicador | Métrica | Meta sugerida |
|---|-----------|---------|---------------|
| 1 | Tempo para abertura correta do chamado | Minutos entre primeiro contato e registro completo no CMMS | ≤ 5 min (vs. 15-30 min manual) |
| 2 | Tempo médio de atendimento (TMA) | Horas entre abertura e conclusão do chamado | Redução de 20% no primeiro trimestre |
| 3 | Taxa de chamados reabertos | % de chamados reabertos em até 7 dias | ≤ 5% |
| 4 | Percentual de classificação correta | % de chamados cuja categoria atribuída pelo agente é confirmada pela equipe técnica | ≥ 90% |
| 5 | Satisfação do solicitante (NPS/CSAT) | Nota média na pesquisa pós-atendimento | ≥ 4.0 / 5.0 |
| 6 | Taxa de coleta completa na primeira interação | % de chamados abertos sem necessidade de retorno para coletar dados | ≥ 85% |

---

## 13. Respostas às Perguntas-Chave (Seção 9 do Enunciado)

**Qual problema concreto o agente resolve?**
Elimina a triagem manual de solicitações de manutenção, reduz chamados incompletos e acelera o encaminhamento à equipe correta.

**Por que um agente é adequado para esse caso?**
Porque o processo é repetitivo, baseado em regras e texto, com alto volume e necessidade de disponibilidade 24/7. Um agente conversacional lida naturalmente com linguagem variada dos solicitantes e consegue conduzir um diálogo estruturado para completar informações.

**Quais informações o agente precisa consultar para responder corretamente?**
Procedimentos de manutenção, catálogo de tipos de ocorrência, orientações de segurança e histórico de chamados.

**O que acontece quando o agente não encontra informação suficiente?**
Informa ao solicitante que precisa de apoio especializado, registra o chamado como "pendente de triagem humana" e escala para um atendente.

**Qual etapa deve ser automatizada e qual deve continuar com uma pessoa?**
Automatizar: recepção, coleta de dados, classificação, abertura de chamado, notificações e pesquisa de satisfação. Manter com pessoas: execução dos reparos, decisões de segurança, aprovações financeiras e investigação de causas-raiz.

**Quais dados precisam de controle de acesso?**
Localização de infraestrutura crítica (quadros elétricos, servidores), histórico consolidado de chamados por área, dados de contato dos técnicos e informações de contratos com fornecedores.

**Qual integração é necessária para que a solução funcione?**
Integração com o CMMS via API REST para criação, consulta e atualização de ordens de serviço, além de integração com o sistema de notificações (Teams/e-mail) para alertas em tempo real.

**Como a empresa saberá se o agente gerou resultado?**
Através do painel de indicadores (BI) que acompanha tempo de abertura, TMA, taxa de reaberturas, classificação correta e satisfação — comparando o período pré e pós-implantação do agente.

---

## 14. Considerações Finais

Esta proposta demonstra como conhecimento (base vetorial com procedimentos), dados (campos estruturados do chamado), automação (triagem e encaminhamento), integração (CMMS via API), segurança (RBAC, criptografia, logs) e participação humana (emergências, aprovações, causas-raiz) se articulam em um agente corporativo coerente e viável para implementação em plataforma low-code.
