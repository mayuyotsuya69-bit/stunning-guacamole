#!/usr/bin/env python3
"""志作文 分析レポートのスコアを抽出し、1レポート=1行のCSVに変換する。

入力は xlsx（列: 生徒番号, レポート全文）または、589件を連結したテキスト。

使い方:
    python3 extract_scores.py 入力.xlsx -o scores.csv
    python3 extract_scores.py 入力.txt  -o scores.csv
"""

import argparse
import csv
import re
import sys

# 各列の (見出し, 抽出に使う安定キーワード)
ITEMS = [
    ("課題設定の俯瞰性と社会的インパクト", r"俯瞰性と社会的インパクト"),
    ("学術的探究心と知識の解像度",       r"学術的探究心と知識の解像度"),
    ("主体的行動実績と自走力",           r"行動実績と自走力"),
    ("論理的構成力と目的意識",           r"論理的構成力と目的意識"),
]


def make_pattern(keyword):
    # 「キーワード … 数字 / 数字」 の獲得点と満点を取る
    return re.compile(keyword + r"[^0-9]*?(\d+)\s*[/／]\s*(\d+)")


ITEM_PATTERNS = [(label, make_pattern(kw)) for label, kw in ITEMS]
TOTAL_PATTERN = re.compile(r"東大推薦ポテンシャルスコア[^0-9]*?(\d+)\s*[/／]\s*(\d+)")


def extract_one(text):
    """1レポートのテキストから 総合点 と 4項目の点数 を取り出す。"""
    text = text or ""
    total_m = TOTAL_PATTERN.search(text)
    total = int(total_m.group(1)) if total_m else ""
    scores = []
    for _, pat in ITEM_PATTERNS:
        m = pat.search(text)
        scores.append(int(m.group(1)) if m else "")
    return total, scores


def read_xlsx(path):
    """(生徒番号, 本文) のタプルを生成。先頭行はヘッダーとみなしスキップ。"""
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:  # ヘッダー
            continue
        sid = row[0] if len(row) > 0 else None
        body = row[1] if len(row) > 1 else None
        if sid is None and not (body and str(body).strip()):
            continue
        yield ("" if sid is None else sid), ("" if body is None else str(body))


def read_text(path):
    """総合スコア行で区切ったテキストを (連番, 本文) で生成。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    starts = [m.start() for m in TOTAL_PATTERN.finditer(text)]
    if not starts:
        yield (1, text)
        return
    starts.append(len(text))
    for i in range(len(starts) - 1):
        yield (i + 1, text[starts[i]:starts[i + 1]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="入力ファイル (.xlsx または .txt)")
    ap.add_argument("-o", "--output", default="scores.csv", help="出力CSV (default: scores.csv)")
    args = ap.parse_args()

    if args.input.lower().endswith(".xlsx"):
        records = read_xlsx(args.input)
        id_header = "生徒番号"
    else:
        records = read_text(args.input)
        id_header = "ID"

    header = [id_header] + [label for label, _ in ITEMS] + ["合計"]
    rows = []
    incomplete = []
    for sid, body in records:
        total, scores = extract_one(body)
        rows.append([sid] + scores + [total])
        if any(s == "" for s in scores):
            incomplete.append(sid)

    with open(args.output, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    print(f"{len(rows)} 件を {args.output} に書き出しました。")
    if incomplete:
        print(f"⚠ 4項目すべてを抽出できなかった件（要確認）: {len(incomplete)} 件", file=sys.stderr)
        print(f"   該当ID: {incomplete}", file=sys.stderr)


if __name__ == "__main__":
    main()
