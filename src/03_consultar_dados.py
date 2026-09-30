import duckdb


con = duckdb.connect("data/analytics.duckdb")


print("=" * 75)
print("DATA PRODUCT DE VENDAS - CONSULTA ANALÍTICA VIA DUCKDB")
print("=" * 75)


# ---------------------------------------------------------
# 1. Schema
# ---------------------------------------------------------

print("\n--- 1. INSPEÇÃO DE SCHEMA E TIPOS ---")

con.sql("""
DESCRIBE retail_sales
""").show()


# ---------------------------------------------------------
# 2. KPIs gerais
# ---------------------------------------------------------

print("\n--- 2. RESUMO DE VENDAS ---")

con.sql("""
SELECT
    COUNT(*) AS linhas_venda,
    COUNT(DISTINCT order_id)
        AS total_pedidos,
    COUNT(DISTINCT customer_id)
        AS total_clientes,
    COUNT(DISTINCT product_id)
        AS total_produtos,
    SUM(quantity)
        AS quantidade_total,
    ROUND(SUM(sales_amount), 2)
        AS valor_total_vendas
FROM retail_sales
""").show()


# ---------------------------------------------------------
# 3. Métricas por status
# ---------------------------------------------------------

print("\n--- 3. VENDAS POR STATUS DO PEDIDO ---")

con.sql("""
SELECT
    order_status,
    COUNT(DISTINCT order_id)
        AS pedidos,
    SUM(quantity)
        AS quantidade,
    ROUND(SUM(sales_amount), 2)
        AS valor_vendas
FROM retail_sales
GROUP BY order_status
ORDER BY valor_vendas DESC
""").show()


# ---------------------------------------------------------
# 4. Produtos com maior valor de vendas
# ---------------------------------------------------------

print("\n--- 4. TOP PRODUTOS POR VALOR DE VENDAS ---")

con.sql("""
SELECT
    product_id,
    SUM(quantity)
        AS quantidade,
    ROUND(SUM(sales_amount), 2)
        AS valor_vendas
FROM retail_sales
GROUP BY product_id
ORDER BY valor_vendas DESC
LIMIT 10
""").show()


# ---------------------------------------------------------
# 5. Amostra
# ---------------------------------------------------------

print("\n--- 5. AMOSTRA DO DATA PRODUCT ---")

con.sql("""
SELECT *
FROM retail_sales
LIMIT 10
""").show()


con.close()


print()
print("=" * 75)
print("[OK] Processamento analítico executado com sucesso.")
print("=" * 75)