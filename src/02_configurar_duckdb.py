from pathlib import Path
import duckdb


ARQUIVO_PARQUET = Path("data/retail_sales.parquet")
BANCO_DADOS = Path("data/analytics.duckdb")


if not ARQUIVO_PARQUET.exists():
    print(
        "ERRO: retail_sales.parquet não encontrado.\n"
        "Execute primeiro: python src/01_preparar_olist.py"
    )
    raise SystemExit(1)


con = duckdb.connect(str(BANCO_DADOS))


con.execute(f"""
CREATE OR REPLACE TABLE retail_sales AS

SELECT *
FROM read_parquet(
    '{ARQUIVO_PARQUET.as_posix()}'
);
""")


total = con.execute("""
SELECT COUNT(*)
FROM retail_sales;
""").fetchone()[0]


print("=" * 75)
print("CONFIGURAÇÃO DO DUCKDB")
print("=" * 75)

print(f"[OK] Banco: {BANCO_DADOS}")
print("[OK] Tabela: retail_sales")
print(f"[OK] Registros: {total}")


con.close()