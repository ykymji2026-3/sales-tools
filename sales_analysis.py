import pandas as pd

# =========================================
# 設定
# =========================================

INPUT_FILE = "output/date_check/formatted_sales_report.csv"

MONTHLY_SALES_OUTPUT = (
    "output/analysis/monthly_sales_summary.csv"
)

TOP_PRODUCTS_OUTPUT = (
    "output/analysis/top_products.csv"
)

TOP_N = 10

# =========================================
# CSV読み込み
# =========================================

print("売上レポートを読み込み中...")

df = pd.read_csv(INPUT_FILE)

print(f"読み込み完了 : {len(df)} 件")

# =========================================
# データ型変換
# =========================================

print("データ型を変換中...")

# Sales を数値化
df["Sales"] = pd.to_numeric(
    df["Sales"],
    errors="coerce"
)

# Order Date を datetime 化
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%Y-%m-%d",
    errors="coerce"
)

# =========================================
# NULL除外
# =========================================

print("NULLデータを除外中...")

sales_df = df.dropna(
    subset=[
        "Sales",
        "Order Date"
    ]
).copy()

print(f"分析対象件数 : {len(sales_df)} 件")

# =========================================
# 年月列作成
# =========================================

print("年月列を作成中...")

sales_df["YearMonth"] = (
    sales_df["Order Date"]
    .dt.strftime("%Y-%m")
)

# =========================================
# 1. 月別売上推移
# =========================================

print("月別売上推移を集計中...")

monthly_sales_df = (
    sales_df
    .groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
)

# 年月順ソート
monthly_sales_df = monthly_sales_df.sort_values(
    by="YearMonth",
    ascending=False
)

# index リセット
monthly_sales_df = monthly_sales_df.reset_index(
    drop=True
)

monthly_sales_df.insert(
    0,
    "Rank",
    range(1, len(monthly_sales_df) + 1)
)

# 小数点2桁へ丸め
monthly_sales_df["Sales"] = (
    monthly_sales_df["Sales"]
    .round(2)
)

# =========================================
# 2. TOP商品分析
# =========================================

print("TOP商品を集計中...")

top_products_df = (
    sales_df
    .groupby("Product Name")["Sales"]
    .sum()
    .reset_index()
)

# 売上降順
top_products_df = top_products_df.sort_values(
    by="Sales",
    ascending=False
)

# TOP N 抽出
top_products_df = top_products_df.head(TOP_N)

# index リセット
top_products_df = top_products_df.reset_index(
    drop=True
)

# 順位列追加
top_products_df.insert(
    0,
    "Rank",
    range(1, len(top_products_df) + 1)
)

# 小数点2桁へ丸め
top_products_df["Sales"] = (
    top_products_df["Sales"]
    .round(2)
)

# =========================================
# CSV出力
# =========================================

print("分析レポートをCSV出力中...")

monthly_sales_df.to_csv(
    MONTHLY_SALES_OUTPUT,
    index=False
)

top_products_df.to_csv(
    TOP_PRODUCTS_OUTPUT,
    index=False
)

# =========================================
# 結果表示
# =========================================

print("\n=================================")
print("月別売上推移")
print("=================================")

print(
    monthly_sales_df.to_string(index=False)
)

print("\n=================================")
print(f"売上 TOP {TOP_N} 商品")
print("=================================")

print(
    top_products_df.to_string(index=False)
)

# =========================================
# 出力完了
# =========================================

print("\n=================================")
print("分析レポート出力完了")
print("=================================")

print(f"月別売上推移 : {MONTHLY_SALES_OUTPUT}")
print(f"TOP商品分析  : {TOP_PRODUCTS_OUTPUT}")