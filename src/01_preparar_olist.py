from pathlib import Path
import duckdb


PASTA_RAW = Path("data/raw")
ARQUIVO_SAIDA = Path("data/retail_sales.parquet")


arquivos = {
    "pedidos": PASTA_RAW / "olist_orders_dataset.csv",
    "itens_pedido": PASTA_RAW / "olist_order_items_dataset.csv",
    "clientes": PASTA_RAW / "olist_customers_dataset.csv",
}


# ---------------------------------------------------------
# 1. Validação arquivos de origem
# ---------------------------------------------------------

arquivos_ausentes = [
    str(caminho)
    for caminho in arquivos.values()
    if not caminho.exists()
]

if arquivos_ausentes:
    print("ERRO: arquivos de origem não encontrados:")

    for arquivo in arquivos_ausentes:
        print(f" - {arquivo}")

    raise SystemExit(1)


print("=" * 75)
print("CONSTRUINDO O DATA PRODUCT DE VENDAS DE VAREJO")
print("=" * 75)


# ---------------------------------------------------------
# 2. Criação engine DuckDB em memória
# ---------------------------------------------------------

con = duckdb.connect(database=":memory:")


# ---------------------------------------------------------
# 3. Construção do Data Product
# Grão: 1 linha por Pedido + Produto
# ---------------------------------------------------------

con.execute(f"""
COPY (

    WITH base_vendas AS (

        SELECT
            CAST(o.order_purchase_timestamp AS DATE)
                AS sale_date,
            CAST(oi.order_id AS VARCHAR)
                AS order_id,
            CAST(c.customer_unique_id AS VARCHAR)
                AS customer_id,
            CAST(oi.product_id AS VARCHAR)
                AS product_id,
            CAST(o.order_status AS VARCHAR)
                AS order_status,
            CAST(oi.price AS DECIMAL(18,2))
                AS item_price
        FROM read_csv_auto(
            '{arquivos["itens_pedido"].as_posix()}',
            HEADER = TRUE
        ) oi
        INNER JOIN read_csv_auto(
            '{arquivos["pedidos"].as_posix()}',
            HEADER = TRUE
        ) o
            ON oi.order_id = o.order_id
        INNER JOIN read_csv_auto(
            '{arquivos["clientes"].as_posix()}',
            HEADER = TRUE
        ) c
            ON o.customer_id = c.customer_id
    ),

    vendas_agregadas AS (

        SELECT
            sale_date,
            order_id,
            customer_id,
            product_id,
            CAST(COUNT(*) AS INTEGER)
                AS quantity,
            CAST(SUM(item_price) AS DECIMAL(18,2))
                AS sales_amount,
            order_status
        FROM base_vendas
        GROUP BY
            sale_date,
            order_id,
            customer_id,
            product_id,
            order_status
    )

    SELECT

        order_id
            || '-'
            || product_id
            AS sales_line_id,
        sale_date,
        order_id,
        customer_id,
        product_id,
        quantity,
        sales_amount,
        order_status
    FROM vendas_agregadas
    ORDER BY
        sale_date,
        order_id,
        product_id

)
TO '{ARQUIVO_SAIDA.as_posix()}'
(FORMAT PARQUET);
""")


# ---------------------------------------------------------
# 4. Validações básicas
# ---------------------------------------------------------

resumo = con.execute(f"""
SELECT
    COUNT(*) AS total_linhas,
    COUNT(DISTINCT sales_line_id)
        AS linhas_unicas,
    COUNT(DISTINCT order_id)
        AS total_pedidos,
    COUNT(DISTINCT customer_id)
        AS total_clientes,
    SUM(quantity)
        AS quantidade_total,
    ROUND(SUM(sales_amount), 2)
        AS valor_total_vendas,
    MIN(quantity)
        AS quantidade_minima,
    MIN(sales_amount)
        AS valor_minimo_venda
FROM read_parquet(
    '{ARQUIVO_SAIDA.as_posix()}'
);
""").fetchdf()

print()
print("RESUMO DE QUALIDADE DO DATA PRODUCT")
print(resumo.to_string(index=False))


# ---------------------------------------------------------
# 5. Amostra
# ---------------------------------------------------------

print()
print("AMOSTRA DO DATA PRODUCT")

amostra = con.execute(f"""
SELECT *
FROM read_parquet(
    '{ARQUIVO_SAIDA.as_posix()}'
)
LIMIT 10;
""").fetchdf()

print(amostra.to_string(index=False))


con.close()


print()
print(f"[OK] Arquivo criado: {ARQUIVO_SAIDA}")
print("=" * 75)
print("DATA PRODUCT DE VENDAS CRIADO COM SUCESSO")
print("=" * 75)