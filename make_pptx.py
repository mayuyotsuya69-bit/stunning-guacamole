#!/usr/bin/env python3
"""AI関与スコア 説明資料の PowerPoint を生成する。"""

from pptx import Presentation
from pptx.util import Pt, Emu, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

# 配色
NAVY = RGBColor(0x1F, 0x33, 0x5E)
BLUE = RGBColor(0x2E, 0x5C, 0xA6)
LIGHT = RGBColor(0xEE, 0xF2, 0xF8)
GRAY = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB3, 0x2A, 0x2A)
GREEN = RGBColor(0x1E, 0x7A, 0x46)

FONT = "Meiryo"  # 日本語フォント

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def add_box(slide, l, t, w, h):
    return slide.shapes.add_textbox(l, t, w, h).text_frame


def set_run(r, text, size, color=NAVY, bold=False, font=FONT):
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font


def fill_rect(slide, l, t, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def header(slide, title, num):
    fill_rect(slide, 0, 0, SW, Inches(1.1), NAVY)
    fill_rect(slide, 0, Inches(1.1), SW, Emu(40000), BLUE)
    tf = add_box(slide, Inches(0.5), Inches(0.18), Inches(11.5), Inches(0.8))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    set_run(p.add_run(), title, 28, WHITE, bold=True)
    # ページ番号
    tfn = add_box(slide, Inches(12.4), Inches(0.18), Inches(0.7), Inches(0.8))
    tfn.vertical_anchor = MSO_ANCHOR.MIDDLE
    pn = tfn.paragraphs[0]
    pn.alignment = PP_ALIGN.RIGHT
    set_run(pn.add_run(), str(num), 16, WHITE)


def bullets(slide, items, left=Inches(0.7), top=Inches(1.5),
            width=Inches(11.9), height=Inches(5.6), size=18, gap=8):
    """items: list of (level, text, color, bold)"""
    tf = add_box(slide, left, top, width, height)
    tf.word_wrap = True
    first = True
    for level, text, color, bold in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = level
        p.space_after = Pt(gap)
        prefix = "" if level == 0 else ""
        marker = "● " if level == 0 else "－ "
        set_run(p.add_run(), marker + text, size - level * 2, color, bold)
    return tf


# ---------- スライド1：表紙 ----------
s = prs.slides.add_slide(BLANK)
fill_rect(s, 0, 0, SW, SH, NAVY)
fill_rect(s, 0, Inches(2.55), SW, Inches(2.3), BLUE)
tf = add_box(s, Inches(0.8), Inches(2.7), Inches(11.7), Inches(2.0))
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
set_run(p.add_run(), "AI関与スコア　算出方法 説明資料", 40, WHITE, bold=True)
p2 = tf.add_paragraph()
p2.alignment = PP_ALIGN.CENTER
set_run(p2.add_run(), "― 作文が生成AIで書かれた可能性を、どう判定しているか ―", 20, WHITE)
tf3 = add_box(s, Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.8))
p3 = tf3.paragraphs[0]
p3.alignment = PP_ALIGN.CENTER
set_run(p3.add_run(), "2026年6月15日　／　経営層向け報告　／　位置づけ：参考指標（断定ではない）", 14, RGBColor(0xCF, 0xD8, 0xE8))


# ---------- スライド2：結論（先出し） ----------
s = prs.slides.add_slide(BLANK)
header(s, "結論（先に要点）", 2)
bullets(s, [
    (0, "「AIが書いたか／自分で考えたか」を断定するものではありません。", NAVY, True),
    (1, "生成AIへの「丸写し・大部分の写し」の“可能性の高さ”を 0〜100 で示す参考指標です。", GRAY, False),
    (0, "数値は統計式や検出器による機械的な計算ではありません。", NAVY, True),
    (1, "判定用の生成AI（LLM）が、各作文を“同一の評価基準”で読み、点数を付けています。", GRAY, False),
    (1, "＝「採点ルールを固定した採点者（AI）に、全員分を同じ物差しで読ませている」仕組み。", GRAY, False),
    (0, "判定の核心は、次の3点を見ていることです。", NAVY, True),
    (1, "① 本人の体験・実感・固有性が見えるか", BLUE, True),
    (1, "② 文章が整いすぎていないか", BLUE, True),
    (1, "③ AI特有の抽象論・定型表現・均質な構成が続いていないか", BLUE, True),
], top=Inches(1.45))


# ---------- スライド3：目的 ----------
s = prs.slides.add_slide(BLANK)
header(s, "1. 目的", 3)
bullets(s, [
    (0, "手書き提出の作文について、生成AI（ChatGPT等）の文章を「そのまま／大部分写している可能性」を見立てる指標。", NAVY, True),
    (0, "手書きであること自体は、人間が書いた根拠として扱いません。", GRAY, False),
    (1, "手書きでもAI出力を写すことは可能なため。", GRAY, False),
    (0, "判定対象は、文章の「内容・構成・語彙・表現」のみ。", GRAY, False),
    (0, "目的はスクリーニング（要確認の作文を見つけること）。最終判断は人が行う前提。", RED, True),
], top=Inches(1.6))


# ---------- スライド4：スコアの意味 ----------
s = prs.slides.add_slide(BLANK)
header(s, "2. スコアの意味（0〜100の整数）", 4)
# 表
from pptx.enum.shapes import MSO_SHAPE
rows = [
    ("0〜30", "書き写した可能性は低い", GREEN),
    ("31〜60", "一部参考にした／判定困難", BLUE),
    ("61〜80", "書き写した可能性がやや高い", RGBColor(0xC9, 0x7A, 0x12)),
    ("81〜100", "書き写した可能性が高い", RED),
]
top = Inches(1.6)
for i, (band, desc, col) in enumerate(rows):
    y = top + Inches(0.95) * i
    fill_rect(s, Inches(0.7), y, Inches(2.6), Inches(0.8), col)
    tf = add_box(s, Inches(0.7), y, Inches(2.6), Inches(0.8))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), band, 20, WHITE, bold=True)
    tf2 = add_box(s, Inches(3.5), y, Inches(8.8), Inches(0.8))
    tf2.vertical_anchor = MSO_ANCHOR.MIDDLE
    set_run(tf2.paragraphs[0].add_run(), desc, 20, NAVY, bold=False)
tf3 = add_box(s, Inches(0.7), Inches(5.6), Inches(11.9), Inches(1.4))
tf3.word_wrap = True
set_run(tf3.paragraphs[0].add_run(), "運用方針：迷う場合は 40〜60 に寄せる。0〜10／90〜100 の極端な値は、明確な根拠が複数そろう場合のみ使用。", 16, GRAY)


# ---------- スライド5：判定の仕組み ----------
s = prs.slides.add_slide(BLANK)
header(s, "3. 判定の仕組み（どう点数を出すか）", 5)
# フロー
steps = ["作文（手書き）", "テキスト化", "判定用AI(LLM)\n＋評価基準", "スコア0〜100\n＋根拠3点"]
bx_w = Inches(2.7); bx_h = Inches(1.1); gap = Inches(0.45)
start = Inches(0.7); y = Inches(1.7)
for i, txt in enumerate(steps):
    x = start + (bx_w + gap) * i
    col = BLUE if i < len(steps) - 1 else NAVY
    fill_rect(s, x, y, bx_w, bx_h, col)
    tf = add_box(s, x, y, bx_w, bx_h)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    for j, line in enumerate(txt.split("\n")):
        p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        set_run(p.add_run(), line, 15, WHITE, bold=True)
    if i < len(steps) - 1:
        ar = add_box(s, x + bx_w, y, gap, bx_h)
        ar.vertical_anchor = MSO_ANCHOR.MIDDLE
        pa = ar.paragraphs[0]; pa.alignment = PP_ALIGN.CENTER
        set_run(pa.add_run(), "▶", 20, NAVY, bold=True)
bullets(s, [
    (0, "スコアはAI（採点者役）の判断であり、固定の計算式から自動算出される値ではありません。", NAVY, True),
    (0, "判断がブレないよう、評価の観点・各スコア帯の定義・禁止事項を文章で細かく固定しています。", GRAY, False),
    (1, "→「全員を同じ物差しで読む」ことを担保。", GRAY, False),
    (0, "同じ作文でも判定は多少揺れ得るため、確定値ではなく目安として扱います。", RED, True),
], top=Inches(3.4), size=17)


# ---------- スライド6：評価の3軸 ----------
s = prs.slides.add_slide(BLANK)
header(s, "4. 評価の3つの軸（AIは何を見ているか）", 6)
cols = [
    ("A. 具体性・本人性", ["経験・失敗・迷いの記述", "部活/家族/友人/地域", "固有名詞・具体的場面", "↑あればAI可能性は低", "一般論・大きな主語のみ", "どの生徒でも書ける内容", "↑ならAI可能性は高"]),
    ("B. 文体・語彙", ["自然な言い回し", "文の長さのばらつき", "感情・言い直しの揺れ", "↑あればAI可能性は低", "均質すぎる文体", "定型表現・硬い抽象語", "↑ならAI可能性は高"]),
    ("C. 構成", ["多少の偏り・寄り道", "段落ごとの熱量差", "考えの流れが見える", "↑あればAI可能性は低", "整いすぎた序論本論結論", "機械的整理・模範解答型", "↑ならAI可能性は高"]),
]
cw = Inches(4.0); cx0 = Inches(0.5); cy = Inches(1.5); gapc = Inches(0.25)
for i, (title, items) in enumerate(cols):
    x = cx0 + (cw + gapc) * i
    fill_rect(s, x, cy, cw, Inches(0.7), BLUE)
    tf = add_box(s, x, cy, cw, Inches(0.7)); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), title, 18, WHITE, bold=True)
    fill_rect(s, x, cy + Inches(0.7), cw, Inches(5.0), LIGHT)
    body = add_box(s, x + Inches(0.15), cy + Inches(0.85), cw - Inches(0.3), Inches(4.8))
    body.word_wrap = True
    first = True
    for it in items:
        p = body.paragraphs[0] if first else body.add_paragraph()
        first = False
        p.space_after = Pt(5)
        if it.startswith("↑"):
            col = GREEN if "低" in it else RED
            set_run(p.add_run(), it, 13, col, bold=True)
        else:
            set_run(p.add_run(), "・" + it, 14, GRAY, bold=False)


# ---------- スライド7：誤判定を防ぐルール ----------
s = prs.slides.add_slide(BLANK)
header(s, "5. 誤判定を防ぐルール（公平性の担保）", 7)
bullets(s, [
    (0, "「文章がうまい子をAI扱いしてしまわないか」への対策を明示しています。", NAVY, True),
    (0, "単独の特徴だけでは高スコアにしない：", RED, True),
    (1, "「手書きだから人間」とは判断しない", GRAY, False),
    (1, "「誤字脱字があるから人間」とは単独で判断しない", GRAY, False),
    (1, "「文章が上手いからAI」とは判断しない", GRAY, False),
    (1, "「構成が整っているからAI」とは単独で判断しない", GRAY, False),
    (1, "1つの特徴だけで極端なスコアにしない／「AIが書いた」と断定しない", GRAY, False),
    (0, "高スコアにしてよいのは複数の根拠がそろう場合のみ。", GREEN, True),
    (1, "具体的体験がほぼない・抽象論が続く・定型表現が多い・整いすぎ 等が同時に見られる場合。", GRAY, False),
], top=Inches(1.45), size=17)


# ---------- スライド8：出力形式 ----------
s = prs.slides.add_slide(BLANK)
header(s, "6. 出力形式（1件ごと）", 8)
bullets(s, [
    (0, "スコアだけでなく根拠3点をセットで残し、後から人が確認・反証できるようにしています。", NAVY, True),
], top=Inches(1.5), size=18)
fill_rect(s, Inches(0.9), Inches(2.5), Inches(11.5), Inches(3.0), LIGHT)
tf = add_box(s, Inches(1.2), Inches(2.7), Inches(11.0), Inches(2.7))
tf.word_wrap = True
lines = ["スコア: <0〜100の整数>", "", "根拠:", "  - <根拠1>", "  - <根拠2>", "  - <根拠3>"]
first = True
for ln in lines:
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    first = False
    set_run(p.add_run(), ln, 18, NAVY, bold=False, font="Consolas")
tf2 = add_box(s, Inches(0.9), Inches(5.8), Inches(11.5), Inches(1.0))
tf2.word_wrap = True
set_run(tf2.paragraphs[0].add_run(), "根拠は必ず3点。可能な場合は作文中の該当箇所を「」で短く引用させています。", 16, GRAY)


# ---------- スライド9：限界 ----------
s = prs.slides.add_slide(BLANK)
header(s, "7. この指標の限界（必ず共有すべき点）", 9)
bullets(s, [
    (0, "断定ではなく「可能性」の参考値。最終判断は必ず人が行う。", RED, True),
    (0, "AI判定のため、同じ作文でもスコアが多少揺れることがある。", GRAY, False),
    (0, "文章力が高い生徒を過剰に疑わない設計だが、誤判定を完全には排除できない。", GRAY, False),
    (0, "高スコアの作文は「クロ」ではなく「人による確認を優先すべき作文」と位置づける。", BLUE, True),
], top=Inches(1.7), size=20, gap=14)


# ---------- スライド10：想定問答 ----------
s = prs.slides.add_slide(BLANK)
header(s, "8. 想定問答（社長質問への回答案）", 10)
qa = [
    ("Q. どうやってAIが書いたか／自分で考えたかを判断しているのか？",
     "A. 専用の生成AIに全作文を同一基準で読ませ、「本人の体験が見えるか」「整いすぎていないか」「AI特有の定型表現・均質な構成が続いていないか」の3観点で、0〜100のスコアと根拠3点を出力。機械的計算ではなく、基準を固定した採点者（AI）による見立てです。"),
    ("Q. うまい作文をAI扱いしてしまわないか？",
     "A. 「上手い／整っている／誤字が少ない」等の単独特徴だけでは高スコアにしないルールを明示。高スコアは複数の根拠がそろった場合のみです。"),
    ("Q. このスコアで処分や合否を決めてよいか？",
     "A. いいえ。スクリーニング用の参考指標です。高スコアを抽出し、最終的には根拠と原文を人が確認して判断する運用を想定しています。"),
]
y = Inches(1.45)
for q, a in qa:
    tfq = add_box(s, Inches(0.6), y, Inches(12.1), Inches(0.5))
    tfq.word_wrap = True
    set_run(tfq.paragraphs[0].add_run(), q, 17, NAVY, bold=True)
    tfa = add_box(s, Inches(0.8), y + Inches(0.5), Inches(11.9), Inches(1.2))
    tfa.word_wrap = True
    set_run(tfa.paragraphs[0].add_run(), a, 14, GRAY, bold=False)
    y = y + Inches(1.85)


prs.save("AI関与スコア_算出方法_説明資料.pptx")
print("saved:", len(prs.slides._sldIdLst), "slides")
