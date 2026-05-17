# EC売上データ監査・分析ツール

Pythonを用いて、ECサイトの売上CSVデータに対する\
データ監査・分析を行うツールです。

実務で行われるような「データ検証」「レポート確認」を意識し、\
重複チェック、日付異常検知、欠損確認、売上分析などを実装しています。

---

# 主な機能

## 1. 重複チェック

- 完全重複データ検知
- 分割注文候補検知
- 重複データCSV出力

### チェック例

- 全列一致データ
- 同一顧客・同日・同一商品の重複注文候補

---

## 2. 日付異常検知

- Ship Date が Order Date より前になっていないか確認
- 不正な日付フォーマットの検知

### チェック例

- `Ship Date < Order Date`
- 不正な日付形式

---

## 3. 欠損値チェック

- NULL / 空白データの検知
- カラム別欠損件数の集計

### チェック対象例

- Customer Name
- Postal Code
- Sales

---

## 4. 売上分析

- 月別売上推移分析
- TOP商品分析
- 州別売上ランキング
- カテゴリ別売上分析
- 地域別売上集計

### 分析例

- 州別売上 TOP10
- カテゴリ別売上比率

---


# ディレクトリ構成

```text
sales-tools/
├── sample_data/
│   └── train.csv
│
├── output/
│   ├── analysis/
│   └── date_check/
│
├── check_duplicates.py
├── check_date_errors.py
├── sales_analysis.py
├── main.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 使用技術

- Python
- pandas

---

# 使用データセット

Kaggleで公開されている売上データセットを利用しています。

- https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting

---

# 出力例

## 重複注文検知

```text
Duplicate Order IDs Found:
CA-2017-152156
```

---

## 日付異常検知

```text
Ship Date occurs before Order Date
```

---

## 欠損値レポート

```text
Customer Name : 3 null values
Postal Code   : 5 null values
```

---

# 今後追加予定の機能

- Streamlitによる画面UI化
- CSVドラッグ＆ドロップ対応
- 検証ルールの設定ファイル化
- Excelレポート出力
- ダッシュボード自動生成

---

# 制作目的

本ツールは、実務で行われるような\
「CSV検証」「レポート整合性確認」「売上分析」を想定し、\
Pythonによるデータ監査・分析の学習およびポートフォリオ用途として作成しています。