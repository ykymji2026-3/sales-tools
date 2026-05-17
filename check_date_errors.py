import pandas as pd
from datetime import datetime

# =========================================
# 設定
# =========================================

INPUT_FILE = "sample_data/train.csv"

FORMATTED_OUTPUT = "output/date_check/formatted_sales_report.csv"

INVALID_DATE_OUTPUT = "output/date_check/invalid_dates.csv"
INVALID_FORMAT_OUTPUT = "output/date_check/invalid_format_dates.csv"
FUTURE_DATE_OUTPUT = "output/date_check/future_dates.csv"
LONG_DELIVERY_OUTPUT = "output/date_check/long_delivery.csv"
SAME_DAY_OUTPUT = "output/date_check/same_day_delivery.csv"
NULL_DATE_OUTPUT = "output/date_check/null_dates.csv"

# =========================================
# CSV読み込み
# =========================================

print("CSVファイルを読み込み中...")

df = pd.read_csv(INPUT_FILE)

print(f"読み込み完了: {len(df)} 件")

# =========================================
# 元の日付保持
# =========================================

df["Original Order Date"] = df["Order Date"]
df["Original Ship Date"] = df["Ship Date"]

# =========================================
# 日付変換
# =========================================

print("日付フォーマットを変換中...")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d/%m/%Y",
    errors="coerce"
)

# =========================================
# 配送日数計算
# =========================================

df["Delivery Days"] = (
    df["Ship Date"] -
    df["Order Date"]
).dt.days

# =========================================
# 日本形式へ変換
# =========================================

df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d")
df["Ship Date"] = df["Ship Date"].dt.strftime("%Y-%m-%d")

# =========================================
# フォーマット済みレポート出力
# =========================================

print("フォーマット済みレポートを出力中...")

df.to_csv(
    FORMATTED_OUTPUT,
    index=False
)

print(
    f"フォーマット済みレポート出力完了: "
    f"{FORMATTED_OUTPUT}"
)

# =========================================
# チェック用DataFrame
# =========================================

check_df = df.copy()

check_df["Order Date"] = pd.to_datetime(
    check_df["Order Date"],
    format="%Y-%m-%d",
    errors="coerce"
)

check_df["Ship Date"] = pd.to_datetime(
    check_df["Ship Date"],
    format="%Y-%m-%d",
    errors="coerce"
)

today = pd.Timestamp(datetime.today().date())

# =========================================
# 1. 配送日逆転
# Ship Date < Order Date
# =========================================

invalid_date_df = check_df[
    check_df["Ship Date"] <
    check_df["Order Date"]
].copy()

# =========================================
# 2. 異常に遅い配送
# Delivery Days > 30
# =========================================

long_delivery_df = check_df[
    check_df["Delivery Days"] > 30
].copy()

# =========================================
# 3. 即日配送
# Delivery Days == 0
# =========================================

same_day_df = check_df[
    check_df["Delivery Days"] == 0
].copy()

# =========================================
# 4. NULL日付
# =========================================

null_date_df = check_df[
    check_df["Order Date"].isna() |
    check_df["Ship Date"].isna()
].copy()

# =========================================
# 5. 未来日
# =========================================

future_date_df = check_df[
    (check_df["Order Date"] > today) |
    (check_df["Ship Date"] > today)
].copy()

# =========================================
# 6. 年異常
# 2030年以降を異常扱い
# =========================================

year_error_df = check_df[
    (check_df["Order Date"].dt.year > 2030) |
    (check_df["Ship Date"].dt.year > 2030)
].copy()

# =========================================
# 7. 日付変換失敗
# =========================================

invalid_format_df = check_df[
    check_df["Order Date"].isna() |
    check_df["Ship Date"].isna()
].copy()

# =========================================
# 結果表示
# =========================================

print("=================================")
print(f"配送日逆転件数       : {len(invalid_date_df)}")
print(f"長期配送件数         : {len(long_delivery_df)}")
print(f"即日配送件数         : {len(same_day_df)}")
print(f"NULL日付件数         : {len(null_date_df)}")
print(f"未来日件数           : {len(future_date_df)}")
print(f"年異常件数           : {len(year_error_df)}")
print(f"日付変換失敗件数     : {len(invalid_format_df)}")
print("=================================")

# =========================================
# CSV出力関数
# =========================================

def export_csv(dataframe, output_path, label):

    if not dataframe.empty:

        export_df = dataframe.copy()

        date_columns = [
            "Order Date",
            "Ship Date"
        ]

        for col in date_columns:

            if col in export_df.columns:

                export_df[col] = export_df[col].dt.strftime(
                    "%Y-%m-%d"
                )

        export_df.to_csv(
            output_path,
            index=False
        )

        print(f"{label} を出力しました: {output_path}")

    else:
        print(f"{label} は見つかりませんでした。")

# =========================================
# CSV出力
# =========================================

export_csv(
    invalid_date_df,
    INVALID_DATE_OUTPUT,
    "配送日逆転データ"
)

export_csv(
    long_delivery_df,
    LONG_DELIVERY_OUTPUT,
    "長期配送データ"
)

export_csv(
    same_day_df,
    SAME_DAY_OUTPUT,
    "即日配送データ"
)

export_csv(
    null_date_df,
    NULL_DATE_OUTPUT,
    "NULL日付データ"
)

export_csv(
    future_date_df,
    FUTURE_DATE_OUTPUT,
    "未来日データ"
)

export_csv(
    invalid_format_df,
    INVALID_FORMAT_OUTPUT,
    "日付変換失敗データ"
)