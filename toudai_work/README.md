# 東大推薦スコア 妥当性検証（取り組み④/⑤）

志作文 AI評価プロジェクト：東大推薦ポテンシャルスコアの criterion validity 検証。

## 成果物
- `analysis_12.py` … ① ROC/AUC ＋ ② 増分妥当性（過去データ n=36）の計算スクリプト
- `fig1_roc.png` … ROC曲線（AUC=0.830, 95%CI 0.70–0.96）
- `fig2_incremental.png` … モデル別AUC（東大スコア / 作文スコア / 両方）

## 注意
- 入力データ（生徒名を含むPII）は `.gitignore` で除外。リポジトリには集計済み図表とコードのみ。
- 実行環境：Python 3.11 / pandas・numpy・scipy・statsmodels・scikit-learn・matplotlib(IPAGothic)。

## 主な結果
- ① AUC=0.830（95%CI DeLong 0.697–0.963 / bootstrap 0.684–0.944）, Mann–Whitney p=7.8e-4。Youden最適閾値64点で感度68%・特異度88%。
- ② 尤度比検定：作文スコアに東大スコアを追加 χ²(1)=6.00, p=0.014（上乗せ有意）／東大スコアに作文スコアを追加 χ²(1)=2.36, p=0.124（上乗せなし）。
- ③ 交絡調整は属性データ（暗号化中）受領後に追加予定。
