#!/usr/bin/env python3
"""AI関与スコア 説明資料（社長決裁資料）の PowerPoint を生成する。

トンマナ:
  16:9 / 背景白 / 文字黒 / アクセント #3E8C7C
  フォント: ヒラギノ角ゴ ProN（本文 W3・10.5pt以上 / 見出し W6・18pt以上）
日本語の禁則: 意味の区切りで明示改行し、数字+単位・括弧の分断を避ける。
"""

from pptx import Presentation
from pptx.util import Pt, Emu, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---- 配色（トンマナ） ----
ACCENT = RGBColor(0x3E, 0x8C, 0x7C)   # #3E8C7C
TINT   = RGBColor(0xE2, 0xEF, 0xEC)   # アクセントの淡色（淡teal）
TINT2  = RGBColor(0xF1, 0xF7, 0xF5)   # さらに淡い
BLACK  = RGBColor(0x1A, 0x1A, 0x1A)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAYBORDER = RGBColor(0xCF, 0xDD, 0xD9)

W3 = "ヒラギノ角ゴ ProN W3"
W6 = "ヒラギノ角ゴ ProN W6"
MONO = "Osaka-Mono"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def _set_ea(run, name):
    """East Asian フォントを runs に確実に設定する。"""
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", name)


def box(slide, l, t, w, h):
    tf = slide.shapes.add_textbox(l, t, w, h).text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(0); tf.margin_right = Emu(0)
    tf.margin_top = Emu(0); tf.margin_bottom = Emu(0)
    return tf


def rect(slide, l, t, w, h, color, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(1)
    shp.shadow.inherit = False
    return shp


def line_para(tf, runs, first=False, align=PP_ALIGN.LEFT, after=4, level=0):
    """runs: list of (text, size, color, font)。1段落=1行として禁則を制御。"""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(after)
    p.space_before = Pt(0)
    p.level = level
    for text, size, color, font in runs:
        r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.color.rgb = color
        _set_ea(r, font)
    return p


def title(slide, text, num):
    # 左にアクセントの縦バー、黒のタイトル、下にアクセントの罫
    rect(slide, Inches(0.0), Inches(0.45), Inches(0.16), Inches(0.62), ACCENT)
    tf = box(slide, Inches(0.45), Inches(0.4), Inches(11.6), Inches(0.75))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    line_para(tf, [(text, 24, BLACK, W6)], first=True)
    rect(slide, Inches(0.45), Inches(1.22), Inches(12.45), Pt(2.2), ACCENT)
    tfn = box(slide, Inches(12.5), Inches(0.5), Inches(0.6), Inches(0.5))
    line_para(tfn, [(str(num), 12, ACCENT, W6)], first=True, align=PP_ALIGN.RIGHT)


def chip(slide, l, t, w, h, label, fill, txtcolor, size=12):
    rect(slide, l, t, w, h, fill)
    tf = box(slide, l, t, w, h); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    line_para(tf, [(label, size, txtcolor, W6)], first=True, align=PP_ALIGN.CENTER)


# ============ スライド1：表紙 ============
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, Inches(2.35), SW, Pt(3), ACCENT)
rect(s, 0, Inches(4.35), SW, Pt(3), ACCENT)
tf = box(s, Inches(0.9), Inches(2.6), Inches(11.5), Inches(1.7))
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
line_para(tf, [("AI関与スコア　算出方法 説明資料", 34, BLACK, W6)], first=True, align=PP_ALIGN.CENTER, after=8)
line_para(tf, [("作文が生成AIで書かれた可能性を、", 18, ACCENT, W6)], align=PP_ALIGN.CENTER, after=0)
line_para(tf, [("どのように判定しているか", 18, ACCENT, W6)], align=PP_ALIGN.CENTER)
tf2 = box(s, Inches(0.9), Inches(5.4), Inches(11.5), Inches(1.0))
line_para(tf2, [("社長決裁資料　／　2026年6月15日", 13, BLACK, W3)], first=True, align=PP_ALIGN.CENTER, after=3)
line_para(tf2, [("位置づけ：参考指標（断定ではなく、人による最終判断を前提とする）", 13, BLACK, W3)], align=PP_ALIGN.CENTER)


# ============ スライド2：結論＋スコアの意味 ============
s = prs.slides.add_slide(BLANK)
title(s, "結論 — 何を、どう判定しているか", 2)
# 左：結論3点
rect(s, Inches(0.45), Inches(1.45), Inches(6.55), Inches(5.55), TINT2)
tf = box(s, Inches(0.7), Inches(1.65), Inches(6.1), Inches(5.2))
line_para(tf, [("結論（要点）", 16, ACCENT, W6)], first=True, after=8)
line_para(tf, [("① 「AIが書いたか／自分で考えたか」を", 13, BLACK, W3)], after=0)
line_para(tf, [("　 断定するものではありません。", 13, BLACK, W3)], after=2)
line_para(tf, [("　 “丸写しの可能性”を 0〜100 で示す", 13, BLACK, W3)], after=0)
line_para(tf, [("　 参考指標です。", 13, BLACK, W3)], after=10)
line_para(tf, [("② 統計式や検出器による", 13, BLACK, W3)], after=0)
line_para(tf, [("　 機械的な計算ではありません。", 13, BLACK, W3)], after=2)
line_para(tf, [("　 判定用の生成AI（LLM）が、全作文を", 13, BLACK, W3)], after=0)
line_para(tf, [("　 同一の基準で読み、点数を付けています。", 13, BLACK, W3)], after=10)
line_para(tf, [("③ 見ているのは次の3点です。", 13, BLACK, W3)], after=2)
line_para(tf, [("　・本人の体験・実感・固有性が見えるか", 13, BLACK, W3)], after=0)
line_para(tf, [("　・文章が整いすぎていないか", 13, BLACK, W3)], after=0)
line_para(tf, [("　・AI特有の抽象論や定型表現、", 13, BLACK, W3)], after=0)
line_para(tf, [("　　均質な構成が続いていないか", 13, BLACK, W3)], after=0)
# 右：スコア帯の表
tf3 = box(s, Inches(7.3), Inches(1.5), Inches(5.6), Inches(0.4))
line_para(tf3, [("スコアの意味（0〜100の整数）", 16, ACCENT, W6)], first=True)
bands = [
    ("0〜30", "書き写した可能性は低い", RGBColor(0x2E, 0x7D, 0x57)),
    ("31〜60", "一部参考にした／判定困難", ACCENT),
    ("61〜80", "可能性がやや高い", RGBColor(0xC2, 0x8A, 0x2B)),
    ("81〜100", "可能性が高い", RGBColor(0xB3, 0x3A, 0x2E)),
]
y = Inches(2.05)
for band, desc, col in bands:
    chip(s, Inches(7.3), y, Inches(1.8), Inches(0.72), band, col, WHITE, size=15)
    tf = box(s, Inches(9.25), y, Inches(3.65), Inches(0.72)); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    line_para(tf, [(desc, 13, BLACK, W3)], first=True)
    y = y + Inches(0.82)
rect(s, Inches(7.3), Inches(5.5), Inches(5.6), Inches(1.5), TINT)
tf = box(s, Inches(7.55), Inches(5.65), Inches(5.1), Inches(1.25))
line_para(tf, [("運用方針", 13, ACCENT, W6)], first=True, after=3)
line_para(tf, [("迷う場合は 40〜60 に寄せます。", 12, BLACK, W3)], after=0)
line_para(tf, [("0〜10 や 90〜100 の極端な値は、", 12, BLACK, W3)], after=0)
line_para(tf, [("明確な根拠が複数そろう場合のみ使用します。", 12, BLACK, W3)], after=0)


# ============ スライド3：判定の仕組み ============
s = prs.slides.add_slide(BLANK)
title(s, "判定の仕組み — どう点数を出しているか", 3)
steps = ["作文（手書き）", "テキスト化", "判定用AI（LLM）\n＋評価基準", "スコア 0〜100\n＋根拠3点"]
bw = Inches(2.75); bh = Inches(1.15); gp = Inches(0.5)
x = Inches(0.55); y = Inches(1.65)
for i, txt in enumerate(steps):
    fill = TINT if i < len(steps) - 1 else ACCENT
    fg = BLACK if i < len(steps) - 1 else WHITE
    rect(s, x, y, bw, bh, fill)
    tf = box(s, x, y, bw, bh); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for j, ln in enumerate(txt.split("\n")):
        line_para(tf, [(ln, 14, fg, W6)], first=(j == 0), align=PP_ALIGN.CENTER, after=0)
    if i < len(steps) - 1:
        ar = box(s, x + bw, y, gp, bh); ar.vertical_anchor = MSO_ANCHOR.MIDDLE
        line_para(ar, [("▶", 18, ACCENT, W6)], first=True, align=PP_ALIGN.CENTER)
    x = x + bw + gp
# 性質の解説
rect(s, Inches(0.55), Inches(3.25), Inches(12.25), Inches(3.6), TINT2)
tf = box(s, Inches(0.85), Inches(3.5), Inches(11.7), Inches(3.2))
line_para(tf, [("この仕組みの性質（社長への説明ポイント）", 16, ACCENT, W6)], first=True, after=8)
line_para(tf, [("●　スコアは採点者役のAIの“判断”であり、", 13, BLACK, W3)], after=0)
line_para(tf, [("　　固定の計算式から自動算出される値ではありません。", 13, BLACK, W3)], after=8)
line_para(tf, [("●　判断が人や日によってブレないよう、", 13, BLACK, W3)], after=0)
line_para(tf, [("　　評価の観点・各スコア帯の定義・禁止事項を文章で細かく固定しています。", 13, BLACK, W3)], after=0)
line_para(tf, [("　　→「全員を同じ物差しで読む」ことを担保しています。", 13, ACCENT, W6)], after=8)
line_para(tf, [("●　同じ作文でも判定は多少揺れ得るため、", 13, BLACK, W3)], after=0)
line_para(tf, [("　　確定値ではなく“目安”として扱います。", 13, BLACK, W3)], after=0)


# ============ スライド4：評価の3軸 ============
s = prs.slides.add_slide(BLANK)
title(s, "評価の3つの軸 — AIは何を見ているか", 4)
cols = [
    ("A. 具体性・本人性",
     ["経験・失敗・迷いの記述", "部活／家族／友人／地域", "固有名詞・具体的な場面"],
     ["一般論・大きな主語ばかり", "どの生徒でも書ける内容", "体験が抽象的で場面が不明"]),
    ("B. 文体・語彙",
     ["高校生らしい自然な言い回し", "文の長さにばらつき", "感情や言い直しの揺れ"],
     ["均質すぎる文体", "「〜が重要である」等の定型", "不自然に硬い抽象語の多用"]),
    ("C. 構成",
     ["多少の偏り・寄り道がある", "段落ごとに熱量差がある", "本人の考えの流れが見える"],
     ["整いすぎた序論・本論・結論", "機械的な整理（第一に…）", "模範解答的すぎる結び"]),
]
cw = Inches(4.05); gpc = Inches(0.25); cx = Inches(0.5); cy = Inches(1.5)
for tlt, low, high in cols:
    chip(s, cx, cy, cw, Inches(0.6), tlt, ACCENT, WHITE, size=15)
    # 人間らしい（可能性↓）
    rect(s, cx, cy + Inches(0.65), cw, Inches(2.45), TINT2)
    tf = box(s, cx + Inches(0.15), cy + Inches(0.78), cw - Inches(0.3), Inches(2.25))
    line_para(tf, [("人間らしい → 可能性は低", 12, RGBColor(0x2E, 0x7D, 0x57), W6)], first=True, after=4)
    for it in low:
        line_para(tf, [("・" + it, 12, BLACK, W3)], after=2)
    # AIらしい（可能性↑）
    rect(s, cx, cy + Inches(3.2), cw, Inches(2.45), TINT)
    tf = box(s, cx + Inches(0.15), cy + Inches(3.33), cw - Inches(0.3), Inches(2.25))
    line_para(tf, [("AIらしい → 可能性は高", 12, RGBColor(0xB3, 0x3A, 0x2E), W6)], first=True, after=4)
    for it in high:
        line_para(tf, [("・" + it, 12, BLACK, W3)], after=2)
    cx = cx + cw + gpc


# ============ スライド5：公平性のルール＋限界 ============
s = prs.slides.add_slide(BLANK)
title(s, "誤判定を防ぐルールと、この指標の限界", 5)
# 左：公平性ルール
chip(s, Inches(0.45), Inches(1.5), Inches(6.2), Inches(0.55), "公平性の担保（高スコアにしないルール）", ACCENT, WHITE, size=13)
rect(s, Inches(0.45), Inches(2.08), Inches(6.2), Inches(4.9), TINT2)
tf = box(s, Inches(0.7), Inches(2.25), Inches(5.75), Inches(4.6))
line_para(tf, [("単独の特徴だけでは高スコアにしません。", 13, BLACK, W6)], first=True, after=6)
for t in ["「手書きだから人間」とは判断しない",
          "「誤字脱字があるから人間」と単独で判断しない",
          "「文章が上手いからAI」とは判断しない",
          "「構成が整っているからAI」と単独で判断しない",
          "1つの特徴だけで極端なスコアにしない",
          "「AIが書いた」と断定的に表現しない"]:
    line_para(tf, [("・" + t, 12, BLACK, W3)], after=3)
line_para(tf, [("高スコアは複数の根拠がそろう場合のみ。", 13, ACCENT, W6)], after=2)
line_para(tf, [("（具体的体験がほぼない・抽象論が続く・", 12, BLACK, W3)], after=0)
line_para(tf, [("　定型表現が多い・整いすぎ などが同時）", 12, BLACK, W3)], after=0)
# 右：限界
chip(s, Inches(6.9), Inches(1.5), Inches(6.0), Inches(0.55), "この指標の限界（必ず共有）", ACCENT, WHITE, size=13)
rect(s, Inches(6.9), Inches(2.08), Inches(6.0), Inches(4.9), TINT)
tf = box(s, Inches(7.15), Inches(2.25), Inches(5.55), Inches(4.6))
line_para(tf, [("●　断定ではなく“可能性”の参考値です。", 13, BLACK, W3)], first=True, after=0)
line_para(tf, [("　　最終判断は必ず人が行います。", 13, BLACK, W6)], after=8)
line_para(tf, [("●　AI判定のため、同じ作文でも", 13, BLACK, W3)], after=0)
line_para(tf, [("　　スコアが多少揺れることがあります。", 13, BLACK, W3)], after=8)
line_para(tf, [("●　文章力が高い生徒を過剰に疑わない", 13, BLACK, W3)], after=0)
line_para(tf, [("　　設計ですが、誤判定を完全には", 13, BLACK, W3)], after=0)
line_para(tf, [("　　排除できません。", 13, BLACK, W3)], after=8)
line_para(tf, [("●　高スコアの作文は「クロ」ではなく、", 13, BLACK, W3)], after=0)
line_para(tf, [("　　「人による確認を優先すべき作文」", 13, ACCENT, W6)], after=0)
line_para(tf, [("　　と位置づけます。", 13, ACCENT, W6)], after=0)


# ============ スライド6：想定問答 ============
s = prs.slides.add_slide(BLANK)
title(s, "想定問答 — 社長質問への回答案", 6)
qa = [
    ("Q. どうやってAIが書いたか／自分で考えたかを判断しているのか？",
     ["A. 専用の生成AIに全作文を同一基準で読ませ、「本人の体験が見えるか」",
      "　 「整いすぎていないか」「AI特有の定型表現や均質な構成が続いていないか」の",
      "　 3観点から、0〜100のスコアと根拠3点を出力します。",
      "　 機械的な計算ではなく、基準を固定した採点者（AI）による見立てです。"]),
    ("Q. 文章がうまい生徒を、AI扱いしてしまわないか？",
     ["A. 「上手い・整っている・誤字が少ない」といった単独の特徴だけでは",
      "　 高スコアにしないルールを明示しています。",
      "　 高スコアになるのは、複数の根拠がそろった場合のみです。"]),
    ("Q. このスコアで処分や合否を決めてよいか？",
     ["A. いいえ。スクリーニング用の参考指標です。",
      "　 高スコアの作文を抽出し、最終的には根拠と原文を人が確認して",
      "　 判断する運用を想定しています。"]),
]
y = Inches(1.5)
for q, lines in qa:
    rect(s, Inches(0.45), y, Inches(12.45), Pt(2), ACCENT)
    tfq = box(s, Inches(0.5), y + Inches(0.08), Inches(12.3), Inches(0.45))
    line_para(tfq, [(q, 15, ACCENT, W6)], first=True)
    tfa = box(s, Inches(0.7), y + Inches(0.62), Inches(12.1), Inches(1.2))
    for j, ln in enumerate(lines):
        line_para(tfa, [(ln, 12.5, BLACK, W3)], first=(j == 0), after=1)
    y = y + Inches(1.83)


prs.save("AI関与スコア_算出方法_説明資料.pptx")
print("saved:", len(prs.slides._sldIdLst), "slides")
