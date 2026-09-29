# Simulação de Incidente e Data Downtime

## Data Product de Vendas de Varejo

**Data Product:** `retail_sales`  
**Domínio:** Varejo / Vendas  
**Tipo de Cenário:** Simulação Acadêmica  

> **Observação:** todos os valores financeiros, tempos operacionais e impactos descritos neste documento são hipotéticos e utilizados exclusivamente para fins acadêmicos. Eles não representam dados operacionais ou financeiros reais da Olist.

---

## 1. Objetivo

Este documento simula um incidente envolvendo o Data Product `retail_sales` com o objetivo de avaliar:

- impacto de uma mudança upstream;
- tempo de detecção do incidente;
- tempo de resolução;
- Data Downtime total;
- impacto financeiro estimado;
- consumo do Error Budget;
- resposta de governança após a falha.

A simulação demonstra como alterações inesperadas nas fontes podem afetar consumidores analíticos mesmo quando os sistemas operacionais originais continuam disponíveis.

---

## 2. Contexto do Data Product

O `retail_sales` representa vendas de varejo no grão:

> **Um Produto dentro de um Pedido.**

Cada linha contém:

- `sales_line_id`
- `sale_date`
- `order_id`
- `customer_id`
- `product_id`
- `quantity`
- `sales_amount`
- `order_status`

O produto é construído a partir das fontes:

- Olist Orders;
- Olist Order Items;
- Olist Customers.

Os principais consumidores simulados são:

- Sales Analytics;
- Business Intelligence;
- Gestão.

No cenário operacional deste projeto, o Data Product deve ser atualizado diariamente em até 24 horas após a disponibilidade dos dados de origem.

---

## 3. Cenário do Incidente

Uma alteração inesperada ocorre na fonte upstream de itens dos pedidos.

O campo:

```text
product_id
```

é removido ou renomeado na origem.

Esse campo é crítico porque participa diretamente da construção do Data Product.

Ele é utilizado para:

1. identificar qual produto foi vendido;
2. definir o grão Pedido + Produto;
3. agrupar ocorrências do mesmo produto dentro do pedido;
4. calcular `quantity`;
5. construir `sales_line_id`;
6. permitir análises downstream por produto.

Sem `product_id`, a transformação não consegue gerar uma versão válida do `retail_sales`.

---

## 4. Impacto Técnico

A mudança upstream provoca a seguinte sequência:

```text
product_id removido ou renomeado
        ↓
Transformação Retail Sales não consegue executar corretamente
        ↓
retail_sales.parquet não é atualizado
        ↓
analytics.duckdb não recebe uma nova versão válida
        ↓
Data Contract não pode ser atendido
        ↓
Data Product não é publicado
```

A última versão válida pode continuar disponível, porém passa a ficar desatualizada.

Por esse motivo, o produto entra em situação de Data Downtime.

---

## 5. Impacto nos Consumidores

Durante o incidente, os consumidores deixam de receber dados atualizados.

Os principais impactos são:

### Sales Analytics

- atraso na análise diária de vendas;
- impossibilidade de avaliar corretamente produtos vendidos;
- uso de dados desatualizados;
- necessidade de investigação manual.

### Business Intelligence

- dashboards deixam de receber atualização;
- relatórios permanecem com dados antigos;
- modelos semânticos podem apresentar informação desatualizada.

### Gestão

- indicadores comerciais ficam defasados;
- decisões podem ser tomadas com base em dados anteriores;
- confiança na informação analítica pode ser reduzida.

---

## 6. Linha do Tempo do Incidente

A seguinte linha do tempo é utilizada na simulação:

| Horário | Evento |
|---|---|
| 08:00 | Publicação esperada do Data Product |
| 08:00 | Processo de transformação falha devido à ausência de `product_id` |
| 08:45 | Incidente é detectado pelo time responsável |
| 09:00 | Investigação de causa raiz é iniciada |
| 10:00 | Alteração upstream é identificada |
| 11:30 | Compatibilidade da transformação é corrigida |
| 11:45 | Data Contract é validado novamente |
| 12:00 | Data Product é republicado com sucesso |

---

## 7. MTTD

MTTD significa:

> **Mean Time to Detect**

Representa o tempo entre o início do incidente e sua detecção.

A publicação deveria ter ocorrido às:

```text
08:00
```

O problema foi detectado às:

```text
08:45
```

Portanto:

```text
MTTD = 45 minutos
```

---

## 8. MTTR

MTTR significa:

> **Mean Time to Resolve**

Representa o tempo entre a detecção do incidente e a restauração do serviço.

O incidente foi detectado às:

```text
08:45
```

O Data Product foi restaurado às:

```text
12:00
```

Portanto:

```text
MTTR = 3 horas e 15 minutos
```

---

## 9. Data Downtime

Para esta simulação, o Data Downtime é calculado como:

```text
Data Downtime = MTTD + MTTR
```

Substituindo os valores:

```text
Data Downtime = 45 minutos + 3 horas e 15 minutos
```

Resultado:

```text
Data Downtime = 4 horas
```

Portanto:

> **O Data Product ficou 4 horas em condição de indisponibilidade ou desatualização.**

---

## 10. Simulação de Impacto Financeiro

Para estimar o impacto operacional do incidente, são utilizadas premissas acadêmicas.

### Premissas

| Variável | Valor |
|---|---:|
| Consumidores impactados | 12 |
| Custo médio por profissional | R$ 150 por hora |
| Data Downtime | 4 horas |

O cálculo considera analistas e usuários de negócio que dependem do Data Product para executar suas atividades.

---

## 11. Cálculo do Impacto Financeiro

A fórmula utilizada é:

```text
Impacto Financeiro =
Consumidores Impactados
×
Custo Médio por Hora
×
Data Downtime
```

Substituindo os valores:

```text
12 × R$ 150 × 4 horas
```

Resultado:

```text
R$ 7.200
```

Portanto:

> **Impacto operacional estimado: R$ 7.200**

Esse valor representa apenas uma aproximação do custo de produtividade associada ao período de indisponibilidade.

---

## 12. Impactos Não Quantificados

O cálculo de R$ 7.200 não inclui impactos indiretos.

Exemplos:

- atraso na tomada de decisão;
- trabalho manual para validação de dados;
- criação de relatórios alternativos;
- divergência entre áreas;
- redução de confiança no Data Product;
- atraso na atualização de dashboards;
- tempo adicional gasto em investigação;
- retrabalho após a restauração.

Esses efeitos podem ampliar o impacto real do incidente.

---

## 13. SLI de Disponibilidade

O SLI de disponibilidade mede o percentual de tempo em que o Data Product permanece disponível e válido para consumo.

Conceitualmente:

```text
Availability =
Tempo Disponível
/
Tempo Total Esperado
```

A janela utilizada nesta simulação é mensal.

---

## 14. SLO de Disponibilidade

O SLO definido para disponibilidade é:

```text
99,5%
```

Isso significa que o Data Product deve permanecer disponível e válido durante pelo menos 99,5% da janela mensal considerada.

---

## 15. Cálculo do Error Budget

O Error Budget representa a indisponibilidade máxima tolerada sem violar o SLO.

Se:

```text
SLO = 99,5%
```

então:

```text
Error Budget = 100% - 99,5%
```

Resultado:

```text
Error Budget = 0,5%
```

Considerando um mês de 30 dias:

```text
30 × 24 = 720 horas
```

A indisponibilidade máxima tolerada é:

```text
720 × 0,5%
```

Resultado:

```text
3,6 horas
```

Portanto:

> **Error Budget mensal = 3,6 horas**

---

## 16. Consumo do Error Budget

O incidente simulado gerou:

```text
4 horas
```

de Data Downtime.

O Error Budget mensal disponível é:

```text
3,6 horas
```

Comparação:

```text
4,0 horas > 3,6 horas
```

Resultado:

> **Error Budget excedido**

O excesso foi de:

```text
4,0 - 3,6 = 0,4 horas
```

Convertendo:

```text
0,4 × 60 = 24 minutos
```

Portanto:

> **O incidente excedeu o Error Budget mensal em 24 minutos.**

---

## 17. Consequência do Error Budget Excedido

Quando o Error Budget é excedido, o time deve priorizar confiabilidade em vez de novas funcionalidades não críticas.

No cenário simulado, as seguintes ações seriam adotadas:

1. priorizar estabilização do Data Product;
2. revisar a causa raiz do incidente;
3. reforçar controles sobre mudanças upstream;
4. revisar a estratégia de validação;
5. postergar mudanças não críticas;
6. acompanhar mais de perto os SLIs;
7. comunicar consumidores sobre o incidente e a recuperação;
8. atualizar a documentação de governança.

---

## 18. Papel do Data Contract

O arquivo:

```text
datacontract.yaml
```

define formalmente o schema e as regras do Data Product.

Entre as garantias relevantes para este incidente estão:

- `product_id` obrigatório;
- `product_id` deve estar presente;
- `sales_line_id` obrigatório e único;
- `quantity >= 1`;
- `sales_amount >= 0.01`;
- `order_status` restrito ao domínio permitido.

Se `product_id` for removido ou alterado de forma incompatível, o Data Product deixa de atender seu contrato.

O contrato funciona como um mecanismo de proteção entre a implementação técnica e os consumidores.

---

## 19. Relação com o Quality Gate

A validação automatizada é realizada com:

```bash
datacontract test datacontract.yaml
```

Para o contrato válido, o resultado esperado é:

```text
PASS
```

Isso significa que o Data Product está aderente ao schema e às regras definidas.

O projeto também inclui:

```text
datacontract_quebra.yaml
```

Esse arquivo contém alterações propositalmente incompatíveis para demonstrar o comportamento do Quality Gate.

O resultado esperado nesse caso é:

```text
FAIL
```

A falha intencional demonstra que alterações incompatíveis podem ser identificadas antes que uma versão seja considerada válida para consumo.

---

## 20. Resposta ao Incidente

Após a identificação do problema, o fluxo operacional simulado é:

```text
Incidente detectado
        ↓
Consumidores são comunicados
        ↓
Investigação de causa raiz
        ↓
Alteração upstream identificada
        ↓
Transformação corrigida
        ↓
Data Product reconstruído
        ↓
Data Contract validado
        ↓
Nova versão publicada
        ↓
Consumidores informados sobre a restauração
```

---

## 21. Ações Preventivas

Após o incidente, o time deve implementar medidas para reduzir a probabilidade de recorrência.

### Gestão de Mudanças Upstream

Mudanças de schema em campos críticos devem ser comunicadas antes da implementação.

Campos como:

```text
product_id
order_id
customer_id
```

devem ser tratados como dependências críticas.

---

### Validação Automatizada

O Data Contract deve continuar sendo executado antes da publicação.

Exemplo:

```bash
datacontract test datacontract.yaml
```

Falhas críticas devem bloquear a liberação do produto.

---

### Monitoramento de Freshness

O time deve monitorar se a nova versão do Data Product foi publicada dentro da janela esperada.

Caso a publicação não ocorra, um incidente deve ser aberto.

---

### Monitoramento do Error Budget

Cada incidente que provoque indisponibilidade deve consumir o Error Budget mensal.

Caso o limite seja excedido, confiabilidade passa a ter prioridade sobre novas entregas não críticas.

---

### Análise de Causa Raiz

Incidentes críticos devem resultar em documentação de:

- causa raiz;
- impacto;
- tempo de detecção;
- tempo de resolução;
- consumidores afetados;
- ações corretivas;
- ações preventivas.

---

## 22. Fluxo do Incidente

```mermaid
flowchart LR

A[Mudança Upstream] --> B[product_id Removido ou Renomeado]

B --> C[Transformação Retail Sales Falha]

C --> D[Data Product Não Publicado]

D --> E[Incidente Detectado]

E --> F[Análise de Causa Raiz]

F --> G[Transformação Corrigida]

G --> H[Data Product Reconstruído]

H --> I[Validação do Data Contract]

I --> J[Data Product Republicado]

J --> K[Consumidores Restaurados]
```

---

## 23. Resumo do Incidente

| Indicador | Resultado |
|---|---:|
| Horário esperado de publicação | 08:00 |
| Horário de detecção | 08:45 |
| Horário de restauração | 12:00 |
| MTTD | 45 minutos |
| MTTR | 3h15 |
| Data Downtime | 4 horas |
| Consumidores impactados | 12 |
| Custo médio simulado | R$ 150/h |
| Impacto financeiro estimado | R$ 7.200 |
| Availability SLO | 99,5% |
| Error Budget mensal | 3,6 horas |
| Downtime do incidente | 4 horas |
| Situação do Error Budget | Excedido |
| Excesso de Error Budget | 24 minutos |

---

## 24. Relação com Governança

O incidente demonstra que a governança do Data Product não se limita ao schema.

Uma operação confiável depende da combinação de:

```text
Data Contract
+
SLIs
+
SLOs
+
SLA
+
Error Budget
+
Lineage
+
Gestão de Incidentes
```

Esses elementos permitem que o time não apenas identifique falhas técnicas, mas também avalie:

- impacto nos consumidores;
- impacto operacional;
- confiabilidade do produto;
- prioridade de correção;
- necessidade de mudanças preventivas.

---

## 25. Conclusão

A simulação demonstra como uma alteração aparentemente simples em uma fonte upstream pode causar impacto relevante em toda a cadeia analítica.

Neste cenário, a remoção ou alteração de `product_id` impede a construção correta do Data Product `retail_sales`.

O incidente resulta em:

- falha de publicação;
- dados desatualizados para consumidores;
- 4 horas de Data Downtime;
- impacto operacional estimado em R$ 7.200;
- violação do Error Budget mensal.

A utilização de um Data Contract formal, combinada com monitoramento de SLIs, SLOs, SLA, Error Budget e linhagem, permite tratar o Data Product como um produto confiável e governado.

O objetivo não é apenas restaurar um pipeline, mas preservar a confiabilidade da interface analítica oferecida aos consumidores.