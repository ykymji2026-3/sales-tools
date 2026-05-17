import subprocess

scripts = [
    "check_duplicates.py",
    "check_date_errors.py",
    "sales_analysis.py"
]

for script in scripts:

    print(f"\n===== {script} 実行開始 =====")

    subprocess.run(
        ["python3", script],
        check=True
    )

print("\n全処理完了")