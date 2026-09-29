# Data Product Canvas

## Data Product de Vendas de Varejo

**Nome técnico:** `retail_sales`  
**Domínio:** Varejo / Vendas  
**Versão:** 1.0.0  
**Status:** Ativo  
**Data Product Owner:** Time de Sales Analytics  

> Este Canvas foi elaborado para fins acadêmicos com base no Brazilian E-Commerce Public Dataset by Olist.

---

# 1. Proposta de Valor e Objetivo de Negócio

## Problema de Negócio

As informações necessárias para análise de vendas estão distribuídas entre diferentes fontes operacionais de pedidos, itens e clientes.

Sem uma visão governada, diferentes consumidores podem realizar suas próprias integrações e recriar regras de negócio de maneiras distintas.

Isso pode gerar:

- métricas inconsistentes;
- duplicação de transformações;
- interpretações diferentes sobre vendas;
- maior esforço para consumidores analíticos;
- dificuldade de rastreabilidade;
- maior impacto de alterações nas fontes.

## Proposta de Valor

Disponibilizar uma visão analítica única, padronizada, documentada e contratualizada das vendas de varejo.

O Data Product permite responder de forma consistente:

- quando a venda ocorreu;
- qual pedido originou a venda;
- qual cliente realizou a compra;
- qual produto foi vendido;
- quantas unidades foram vendidas;
- qual foi o valor dos produtos vendidos;
- qual é o status operacional do pedido.

## Objetivo de Negócio

Reduzir a necessidade de cada consumidor reconstruir individualmente a lógica de vendas, disponibilizando uma interface analítica confiável e reutilizável.

## Grão

O grão do Data Product é:

> **Um Produto dentro de um Pedido.**

Cada linha representa uma combinação única entre:

```text
order_id + product_id
```

Quando o mesmo produto aparece mais de uma vez dentro do mesmo pedido, as ocorrências são agregadas.

Exemplo:

```text
Pedido 123 | Produto A | R$ 100
Pedido 123 | Produto A | R$ 100
Pedido 123 | Produto A | R$ 100
```

é representado como:

```text
Pedido 123
Produto A
Quantidade: 3
Valor de Vendas: R$ 300
```

---

# 2. Consumidores-Alvo e Casos de Uso

## Sales Analytics

### Casos de Uso

- analisar volume de vendas;
- analisar valor de vendas;
- acompanhar evolução das vendas ao longo do tempo;
- analisar atividade de clientes;
- analisar desempenho de produtos;
- analisar vendas por status do pedido.

### Necessidade

Consumir uma visão única de vendas sem reconstruir joins e regras de agregação a cada análise.

---

## Business Intelligence

### Casos de Uso

- construção de dashboards;
- criação de relatórios;
- alimentação de modelos semânticos;
- utilização de métricas padronizadas de vendas.

### Necessidade

Utilizar uma fonte governada, com schema conhecido e regras documentadas.

---

## Gestão

### Casos de Uso

- acompanhamento de indicadores comerciais;
- monitoramento de tendências;
- análise de volume e valor das vendas;
- suporte à tomada de decisão.

### Necessidade

Consumir indicadores derivados de uma fonte analítica consistente e rastreável.

---

# 3. Fontes de Entrada e Fronteira do Domínio

## Input Sources

O produto utiliza três arquivos do Brazilian E-Commerce Public Dataset by Olist.

### Olist Orders

Arquivo:

```text
olist_orders_dataset.csv
```

Atributos utilizados:

- `order_id`;
- `customer_id`;
- `order_purchase_timestamp`;
- `order_status`.

Responsabilidade no produto:

- identificar o pedido;
- identificar o cliente operacional;
- determinar a data da venda;
- fornecer o status do pedido.

---

### Olist Order Items

Arquivo:

```text
olist_order_items_dataset.csv
```

Atributos utilizados:

- `order_id`;
- `product_id`;
- `price`.

Responsabilidade no produto:

- identificar o produto;
- relacionar produtos aos pedidos;
- calcular quantidade;
- calcular valor de vendas.

---

### Olist Customers

Arquivo:

```text
olist_customers_dataset.csv
```

Atributos utilizados:

- `customer_id`;
- `customer_unique_id`.

Responsabilidade no produto:

- converter o identificador operacional de cliente em um identificador analítico único e anonimizado.

---

## Integração das Fontes

```text
Olist Order Items
        │
        │ order_id
        ▼
   Olist Orders
        │
        │ customer_id
        ▼
 Olist Customers
```

---

## Fronteira do Domínio

O Data Product pertence ao domínio:

```text
Varejo / Vendas
```

O escopo do produto inclui:

- pedidos;
- produtos vendidos;
- clientes anonimizados;
- quantidade de produtos;
- valor dos itens;
- status operacional do pedido.

Não fazem parte do escopo deste Data Product:

- pagamentos;
- avaliações de clientes;
- informações de vendedores;
- geolocalização;
- custos logísticos;
- cálculo de margem;
- reconhecimento contábil de receita.

Essas informações podem ser incorporadas em outros Data Products ou em evoluções futuras.

---

# 4. Output Ports

O Data Product disponibiliza duas formas principais de saída.

## Parquet

Arquivo:

```text
data/retail_sales.parquet
```

Finalidade:

- saída analítica portável;
- armazenamento eficiente;
- reutilização por outras ferramentas e processos.

---

## DuckDB

Banco:

```text
data/analytics.duckdb
```

Tabela:

```text
retail_sales
```

Finalidade:

- consumo analítico;
- execução de consultas;
- inspeção de schema;
- validação automatizada do Data Contract.

---

## Schema de Saída

| Campo | Tipo | Definição |
|---|---|---|
| `sales_line_id` | String | Identificador técnico único da combinação Pedido + Produto |
| `sale_date` | Date | Data em que o pedido foi realizado |
| `order_id` | String | Identificador do pedido |
| `customer_id` | String | Identificador único e anonimizado do cliente |
| `product_id` | String | Identificador do produto vendido |
| `quantity` | Integer | Quantidade daquele produto dentro do pedido |
| `sales_amount` | Decimal | Soma dos preços dos itens da combinação Pedido + Produto, sem frete |
| `order_status` | String | Status operacional do pedido |

---

## Contrato da Interface

O contrato formal do Data Product está disponível em:

```text
datacontract.yaml
```

O contrato define:

- schema;
- tipos;
- obrigatoriedade;
- unicidade;
- regras de valor;
- domínio de valores;
- níveis de serviço.

---

# 5. Service Level Objectives - SLOs

Os níveis de serviço abaixo representam o cenário operacional simulado do projeto.

## Freshness

Meta:

> **≤ 24 horas**

O Data Product deve ser atualizado em até 24 horas após a disponibilidade dos dados de origem.

---

## Disponibilidade

Meta mensal:

> **≥ 99,5%**

O produto deve permanecer disponível e válido para consumo durante pelo menos 99,5% da janela mensal.

---

## Qualidade

Meta:

> **100% de conformidade das regras críticas do Data Contract antes da publicação**

Uma versão com falha em regra crítica não deve ser considerada pronta para consumo.

---

## Comunicação de Incidente

Meta:

> **≤ 1 hora após a detecção de um incidente crítico**

Consumidores impactados devem ser comunicados dentro da janela definida.

---

## Retenção

Meta:

> **≥ 365 dias**

O histórico analítico deve permanecer disponível por pelo menos 365 dias.

---

## Error Budget

Considerando o SLO de disponibilidade:

```text
99,5%
```

a indisponibilidade tolerada é:

```text
100% - 99,5% = 0,5%
```

Para uma janela de 30 dias:

```text
30 × 24 = 720 horas
```

Logo:

```text
720 × 0,5% = 3,6 horas
```

Portanto:

> **Error Budget mensal = 3,6 horas**

A simulação detalhada está documentada em:

[`simulacao_incidente.md`](simulacao_incidente.md)

---

# 6. Governança de Dados e Papéis de Segurança

## Data Product Owner

Responsável:

> **Time de Sales Analytics**

Principais responsabilidades:

- definir e manter conceitos de negócio;
- manter o Data Product Canvas;
- manter o Data Contract;
- definir requisitos de qualidade;
- acompanhar níveis de serviço;
- comunicar mudanças aos consumidores;
- coordenar resposta a incidentes;
- administrar o versionamento do produto.

---

## Produtor do Data Product

Responsável pela implementação técnica da transformação.

Responsabilidades:

- integrar as fontes;
- aplicar regras de transformação;
- gerar `retail_sales.parquet`;
- carregar `retail_sales` no DuckDB;
- executar validações;
- corrigir falhas técnicas.

---

## Consumidores

Consumidores simulados:

- Sales Analytics;
- Business Intelligence;
- Gestão.

Responsabilidades:

- utilizar o produto de acordo com sua semântica documentada;
- respeitar o grão definido;
- não reinterpretar métricas sem alinhamento;
- comunicar necessidades de mudança ao owner.

---

## Garantias de Qualidade

O Data Contract formaliza as principais garantias.

### Unicidade

```text
sales_line_id
```

deve ser único.

---

### Completude

Os seguintes campos são obrigatórios:

```text
sales_line_id
sale_date
order_id
customer_id
product_id
quantity
sales_amount
order_status
```

---

### Quantidade

```text
quantity >= 1
```

---

### Valor de Vendas

```text
sales_amount >= 0.01
```

---

### Domínio de Status

Os valores permitidos são:

```text
approved
canceled
created
delivered
invoiced
processing
shipped
unavailable
```

---

## Segurança e Privacidade

O produto utiliza somente identificadores anonimizados do dataset Olist.

O campo:

```text
customer_id
```

é derivado de:

```text
customer_unique_id
```

e não contém nome, e-mail, documento ou outra informação pessoal diretamente identificável.

No cenário acadêmico atual, o consumo ocorre localmente por meio do repositório e do DuckDB.

Em uma implementação corporativa, o acesso ao produto deveria seguir mecanismos formais de autorização e controle de acesso definidos pela organização.

---

## Gestão de Mudanças

O Data Product utiliza versionamento semântico.

Versão atual:

```text
1.0.0
```

Mudanças compatíveis podem resultar em nova versão minor:

```text
1.0.0 → 1.1.0
```

Mudanças incompatíveis devem resultar em nova versão major:

```text
1.0.0 → 2.0.0
```

Exemplos de breaking changes:

- remoção de campo obrigatório;
- alteração incompatível de tipo;
- mudança no significado de uma métrica;
- introdução de regra obrigatória incompatível;
- restrição incompatível de valores permitidos.

O projeto inclui:

```text
datacontract_quebra.yaml
```

para demonstrar a detecção de mudanças incompatíveis.

---

# Resumo do Canvas

| Bloco do Canvas | Definição no Projeto |
|---|---|
| Proposta de Valor e Objetivo de Negócio | Padronizar e governar a visão analítica de vendas |
| Consumidores-Alvo | Sales Analytics, BI e Gestão |
| Input Sources | Orders, Order Items e Customers |
| Fronteira do Domínio | Varejo / Vendas |
| Output Ports | Parquet e DuckDB |
| Freshness SLO | ≤ 24 horas |
| Availability SLO | ≥ 99,5% |
| Data Quality SLO | 100% de checks críticos |
| Retenção | ≥ 365 dias |
| Owner | Time de Sales Analytics |
| Contrato | `datacontract.yaml` |
| Versão | 1.0.0 |