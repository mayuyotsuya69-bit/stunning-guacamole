#!/usr/bin/env python3
"""志作文 分析レポートのスコアを抽出し、1レポート=1行のCSVに変換する。

使い方:
    python3 extract_scores.py 入力ファイル.txt -o scores.csv

589個のレポートが1ファイルに連結されている前提。
各レポートは「東大推薦ポテンシャルスコア」行をアンカーにして区切る。
区切り文字（--- など）が無くても動作する。
"""

import argparse
import csv
import re
import sys

# 各列の (見出し, 抽出に使う安定キーワードの正規表現)
# レポートごとに表現が多少ゆれても拾えるよう、特徴的な語を使う。
ITEMS = [
    ("課題設定の俯瞰性と社会的インパクト", r"俯瞰性と社会的インパクト"),
    ("学術的探究心と知識の解像度",       r"学術的探究心と知識の解像度"),
    ("主体的行動実績と自走力",           r"主体的行動実績と自走力"),
    ("論理的構成力と目的意識",           r"論理的構成力と目的意識"),
]

# 「キーワード ： 数字 / 数字」 から獲得点と満点を取る
def make_pattern(keyword):
    return re.compile(keyword + r"[^0-9]*?(\d+)\s*[/／]\s*(\d+)")

ITEM_PATTERNS = [(label, make_pattern(kw)) for label, kw in ITEMS]

# レポートの区切りアンカー（総合スコア行）。獲得点 / 100 も拾う。
TOTAL_PATTERN = re.compile(r"東大推薦ポテンシャルスコア[^0-9]*?(\d+)\s*[/／]\s*(\d+)")


def split_records(text):
    """総合スコア行の出現位置で本文を分割し、各レポートのテキストを返す。"""
    starts = [m.start() for m in TOTAL_PATTERN.finditer(text)]
    if not starts:
        # アンカーが無ければ全体を1件として扱う
        return [text]
    starts.append(len(text))
    return [text[starts[i]:starts[i + 1]] for i in range(len(starts) - 1)]


def extract_one(record):
    """1レポートのテキストから 総合点 と 4項目の点数 を取り出す。"""
    total_m = TOTAL_PATTERN.search(record)
    total = int(total_m.group(1)) if total_m else ""

    scores = []
    for _, pat in ITEM_PATTERNS:
        m = pat.search(record)
        scores.append(int(m.group(1)) if m else "")
    return total, scores


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="589個のレポートを連結した入力ファイル")
    ap.add_argument("-o", "--output", default="scores.csv", help="出力CSV (default: scores.csv)")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    records = split_records(text)

    header = ["ID"] + [label for label, _ in ITEMS] + ["合計"]
    rows = []
    incomplete = []
    for i, rec in enumerate(records, 1):
        total, scores = extract_one(rec)
        rows.append([i] + scores + [total])
        if any(s == "" for s in scores):
            incomplete.append(i)

    with open(args.output, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

    print(f"{len(rows)} 件を {args.output} に書き出しました。")
    if incomplete:
        print(f"⚠ 4項目すべてを抽出できなかったレポート（要確認）: {incomplete}", file=sys.stderr)


if __name__ == "__main__":
    main()
