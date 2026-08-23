# Catálogo de Tipos de Ocorrência
## Base de Conhecimento para RAG

---

## 1. Elétrica

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Queda de energia (parcial) | 2h | Verificar disjuntor do setor | Eletricista de plantão |
| Queda de energia (total) | 1h | Acionar gerador se disponível | Coordenador elétrico |
| Tomada/interruptor com defeito | 24h | Não usar a tomada; sinalizar | Eletricista |
| Curto-circuito / faísca | EMERGÊNCIA | Desligar disjuntor geral do setor; evacuar | Brigada + Eletricista |
| Luminária apagada | 48h | Nenhuma | Manutenção geral |
| Luminária piscando | 24h | Desligar a luminária se possível | Eletricista |

---

## 2. Climatização / Refrigeração

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Ar-condicionado não liga | 8h | Verificar se o controle está no modo correto | Técnico HVAC |
| Ar-condicionado vazando | 4h | Colocar balde/pano; não usar equipamentos embaixo | Técnico HVAC |
| Temperatura inadequada | 8h | Ajustar setpoint se acessível | Técnico HVAC |
| Ruído excessivo no AC | 24h | Nenhuma | Técnico HVAC |
| Vazamento de amônia (industrial) | EMERGÊNCIA | Evacuar área; acionar brigada | SST + Brigada |
| Câmara fria com defeito | 1h | Não abrir a porta; verificar termômetro externo | Técnico refrigeração |

---

## 3. Hidráulica

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Vazamento de água (pequeno) | 8h | Colocar recipiente; fechar registro se acessível | Encanador |
| Vazamento de água (grande/inundação) | 1h | Fechar registro geral do andar | Encanador + Coordenador |
| Entupimento (pia/vaso) | 4h | Não usar o equipamento | Encanador |
| Sem água no setor | 2h | Reportar imediatamente | Encanador |
| Descarga com defeito | 24h | Nenhuma | Encanador |
| Infiltração/goteira | 48h | Proteger equipamentos embaixo | Manutenção predial |

---

## 4. Limpeza / Higienização

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Limpeza emergencial (derramamento) | 30min | Sinalizar área molhada | Equipe limpeza |
| Banheiro sem material (papel/sabão) | 1h | Nenhuma | Equipe limpeza |
| Lixeiras cheias | 2h | Nenhuma | Equipe limpeza |
| Odor forte / mau cheiro | 4h | Ventilar o ambiente se possível | Equipe limpeza + Manutenção |
| Limpeza de rotina não realizada | 8h | Nenhuma | Coordenador limpeza |

---

## 5. Mobiliário

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Cadeira quebrada | 48h | Não usar; sinalizar | Manutenção geral |
| Mesa/bancada danificada | 48h | Nenhuma | Manutenção geral |
| Porta/janela com defeito | 24h | Não forçar; sinalizar | Manutenção geral |
| Fechadura/tranca com problema | 8h | Não trancar a porta | Manutenção geral |
| Divisória danificada | 72h | Nenhuma | Manutenção geral |

---

## 6. Infraestrutura (Docas / Estrutural)

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Portão de doca com defeito | 2h | Operar manualmente se seguro | Manutenção industrial |
| Piso danificado/buraco | 4h | Sinalizar com cone | Manutenção predial |
| Rachadura em parede/pilar | 24h | Evacuar se parecer estrutural | Engenharia |
| Elevador parado | 1h | Se alguém preso: acionar bombeiros | Empresa terceirizada |
| Infiltração em telhado/laje | 24h | Proteger área abaixo | Manutenção predial |
| Nivelador de doca quebrado | 2h | Não usar a doca; sinalizar | Manutenção industrial |

---

## 7. Predial Geral / Outros

| Subcategoria | SLA | Ação Imediata | Responsável |
|-------------|-----|---------------|-------------|
| Sinalização danificada | 48h | Nenhuma | Manutenção geral |
| Paisagismo/área externa | 72h | Nenhuma | Equipe jardim |
| Pintura (descascando/suja) | 72h | Nenhuma | Manutenção geral |
| Estacionamento (problema) | 24h | Depende do tipo | Segurança patrimonial |
| Controle de acesso (catraca/biometria) | 4h | Usar entrada alternativa | TI + Segurança |

---

## Regras de Escalonamento Automático

```
SE urgência = "Crítica" E tipo ∈ [Elétrica, Hidráulica, Climatização]:
  → Notificar Coordenador + Técnico de plantão imediatamente
  → SLA máximo: conforme tabela acima

SE chamado não atendido em 50% do SLA:
  → Alerta amarelo para coordenador

SE chamado não atendido em 100% do SLA:
  → Alerta vermelho para gestor de facilities

SE 3+ chamados iguais no mesmo local em 30 dias:
  → Flag "problema recorrente" → Investigação de causa-raiz
```

---

## Classificação de Urgência (Guia para a IA)

| Nível | Critério | Exemplos |
|-------|----------|----------|
| **Crítica** | Risco à segurança ou parada operacional | Vazamento de gás, curto-circuito, inundação, câmara fria parada |
| **Alta** | Impacto significativo na produtividade | AC principal parado, sem água no andar, portão de doca travado |
| **Normal** | Desconforto ou problema pontual | AC com ruído, vazamento leve, luminária apagada |
| **Baixa** | Melhoria ou manutenção preventiva | Pintura, paisagismo, cadeira com ajuste |
