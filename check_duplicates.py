import pandas as pd

# =========================================
# 設定
# =========================================

INPUT_FILE = "sample_data/train.csv"

FULL_DUPLICATE_OUTPUT = "output/duplicate_check/full_duplicates.csv"
SPLIT_ORDER_OUTPUT = "output/duplicate_check/split_order_candidates.csv"

# =========================================
# CSV読み込み
# =========================================

print("CSVファイルを読み込み中...")

df = pd.read_csv(INPUT_FILE)

print(f"読み込み完了: {len(df)} 件")

# =========================================
# 完全重複チェック用カラム
# Row ID は除外
# =========================================

compare_columns = [
    col for col in df.columns
    if col != "Row ID"
]

# =========================================
# 1. 完全重複チェック
# =========================================

print("完全重複データをチェック中...")

full_duplicate_df = df[
    df.duplicated(
        subset=compare_columns,
        keep=False
    )
].copy()

# =========================================
# 2. 分割注文候補チェック
#
# 条件:
# Customer ID
# Order Date
# Product Name
#
# ただし Sales が異なるもの
# =========================================

print("分割注文候補をチェック中...")

split_order_df = df[
    df.duplicated(
        subset=[
            "Customer ID",
            "Order Date",
            "Product Name"
        ],
        keep=False
    )
].copy()

# 完全重複を除外
split_order_df = split_order_df.drop_duplicates()

# Sales が異なるデータのみ抽出
split_order_df = split_order_df.groupby(
    [
        "Customer ID",
        "Order Date",
        "Product Name"
    ]
).filter(
    lambda x: x["Sales"].nunique() > 1
)

# =========================================
# 結果表示
# =========================================

print("=================================")
print(f"完全重複件数       : {len(full_duplicate_df)}")
print(f"分割注文候補件数   : {len(split_order_df)}")
print("=================================")

# =========================================
# CSV出力
# =========================================

if not full_duplicate_df.empty:

    full_duplicate_df = full_duplicate_df.sort_values(
        by=["Customer ID", "Order Date"]
    )

    full_duplicate_df.to_csv(
        FULL_DUPLICATE_OUTPUT,
        index=False
    )

    print(
        f"完全重複データを出力しました: "
        f"{FULL_DUPLICATE_OUTPUT}"
    )

else:
    print("完全重複データは見つかりませんでした。")

# -----------------------------------------

if not split_order_df.empty:

    split_order_df = split_order_df.sort_values(
        by=["Customer ID", "Order Date"]
    )

    split_order_df.to_csv(
        SPLIT_ORDER_OUTPUT,
        index=False
    )

    print(
        f"分割注文候補を出力しました: "
        f"{SPLIT_ORDER_OUTPUT}"
    )

else:
    print("分割注文候補は見つかりませんでした。")