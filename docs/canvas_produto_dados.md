# Canvas do Data Product

## Data Product de Vendas de Varejo

**Nome técnico:** `retail_sales`  
**Domínio:** Varejo / Vendas  
**Owner:** Time de Sales Analytics  
**Versão:** 1.0.0  

---

## 1. Problema de Negócio

As informações necessárias para análise de vendas estão distribuídas
entre diferentes fontes operacionais de pedidos, itens e clientes.

Sem um Data Product governado, os consumidores precisam realizar suas
próprias integrações e recriar regras de negócio, aumentando o risco de
divergência entre indicadores e interpretações.

---

## 2. Proposta de Valor

Disponibilizar uma visão única, padronizada, documentada e
contratualizada das vendas de varejo.

O produto permite identificar:

- quando a venda ocorreu;
- qual pedido gerou a venda;
- qual cliente realizou a compra;
- qual produto foi vendido;
- quantas unidades foram vendidas;
- qual foi o valor da venda;
- qual é o status operacional do pedido.

---

## 3. Consumidores

### Sales Analytics

Análise de volume, valor e evolução das vendas.

### Business Intelligence

Construção de dashboards, relatórios e modelos semânticos.

### Gestão

Acompanhamento de indicadores comerciais.

---

## 4. Grão

Uma linha representa um **Produto dentro de um Pedido**.

Ocorrências repetidas do mesmo produto no mesmo pedido são agregadas
em uma única linha de venda.

---

## 5. Input Ports

Fontes provenientes do Brazilian E-Commerce Public Dataset by Olist:

- `olist_orders_dataset.csv`;
- `olist_order_items_dataset.csv`;
- `olist_customers_dataset.csv`.

---

## 6. Output Ports

### Parquet

`data/retail_sales.parquet`

### DuckDB

Banco:

`data/analytics.duckdb`

Tabela:

`retail_sales`

---

## 7. Métricas de Negócio

### Quantity

Quantidade de unidades de um produto dentro do pedido.

### Sales Amount

Soma dos preços dos itens da combinação Pedido + Produto.

O frete não está incluído.

---

## 8. Garantias de Qualidade

- `sales_line_id` deve ser único;
- campos críticos não podem ser nulos;
- `quantity` deve ser maior ou igual a 1;
- `sales_amount` deve ser maior ou igual a 0.01;
- `order_status` deve pertencer ao domínio definido pelo contrato.

---

## 9. Níveis de Serviço

### Freshness

Atualização em até 24 horas.

### Disponibilidade

SLO mensal de 99,5%.

### Qualidade

100% das regras críticas do Data Contract devem ser atendidas
antes da publicação.

### Retenção

365 dias.

---

## 10. Métricas de Sucesso

- 100% de validação contratual antes da publicação;
- redução de lógica de vendas duplicada;
- consistência na definição de quantidade e valor de vendas;
- menor impacto downstream provocado por mudanças de schema.