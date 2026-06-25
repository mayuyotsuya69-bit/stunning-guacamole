# -*- coding: utf-8 -*-
import pandas as pd, numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pingouin as pg
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'; fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name(); plt.rcParams['axes.unicode_minus']=False
AC,DK,OR,LT,GR='#3E8C7C','#2E6457','#C2603F','#E7F1EE','#5C6663'
def T(s): return fm.FontProperties(fname=fp,size=s)

m=pd.read_csv('attr589.csv').rename(columns={'東大推薦ポテンシャルスコア(0-100)':'pot','AI評価スコア':'essay'})
# encode
gmap={31:1,32:2,33:3}
m['grade']=m['学年コード'].map(gmap)          # 1=高1,2=高2,3=高3
rmap={'S':8,'A':7,'B':6,'B-':5,'C':4,'D':3,'E':2,'F':1}
m['rank']=m['高校ランク'].map(rmap)            # higher=academically stronger
m['waseda']=(m['部門']=='早稲田塾').astype(float)
m.loc[m['部門'].isna(),'waseda']=np.nan

print("="*74); print("③ 交絡調整：属性差は『作文力』で説明できるか（循環論法チェック）")
print("="*74)
print("DV1=東大推薦スコア(0-100), DV2=作文AIスコア(0-15)。共変量=作文AIスコア。")
print("性別データは提供ファイルに無し → 学年・高校ランク・校舎で実施。\n")

# ---- FULL sample: 学年 + 高校ランク ----
full=m.dropna(subset=['pot','essay','grade','rank']).copy()
print(f"[全体サンプル n={len(full)}]  corr(pot,essay)={full['pot'].corr(full['essay']):.3f}")
def zscore(s): return (s-s.mean())/s.std()
for c in ['pot','essay','grade','rank']: full['z_'+c]=zscore(full[c])

m1=smf.ols('z_pot ~ z_grade + z_rank',data=full).fit(cov_type='HC3')
m2=smf.ols('z_pot ~ z_grade + z_rank + z_essay',data=full).fit(cov_type='HC3')
m3=smf.ols('z_essay ~ z_grade + z_rank',data=full).fit(cov_type='HC3')
print("\n― M1: 東大スコア ~ 学年+高校ランク（標準化β, 生の属性効果）")
for v in ['z_grade','z_rank']: print(f"     {v}: β={m1.params[v]:+.3f}  p={m1.pvalues[v]:.4f}")
print(f"     R²={m1.rsquared:.3f}")
print("\n― M2: ＋作文AIスコアを統制（共変量投入後の属性効果）")
for v in ['z_grade','z_rank','z_essay']: print(f"     {v}: β={m2.params[v]:+.3f}  p={m2.pvalues[v]:.4f}")
print(f"     R²={m2.rsquared:.3f}")
print("\n― M3: 作文AIスコア ~ 学年+高校ランク（同じ属性が作文力をどれだけ説明するか）")
for v in ['z_grade','z_rank']: print(f"     {v}: β={m3.params[v]:+.3f}  p={m3.pvalues[v]:.4f}")

print("\n■ 偏相関（作文AIスコアを統制した、属性 vs 東大スコア）")
for v,lab in [('grade','学年'),('rank','高校ランク')]:
    raw=pg.corr(full[v],full['pot']).iloc[0]
    par=pg.partial_corr(full,x=v,y='pot',covar='essay').iloc[0]
    print(f"   {lab}: 生r={raw['r']:+.3f}(p={raw['p_val']:.3g}) → 偏r(作文統制)={par['r']:+.3f}(p={par['p_val']:.3g})  残存率={par['r']/raw['r']*100:.0f}%")

# ---- 校舎 subsample ----
sub=m.dropna(subset=['pot','essay','waseda','grade','rank']).copy()
sub=sub[m['部門']!='東進個別']  # drop n=2
for c in ['pot','essay','grade','rank','waseda']: sub['z_'+c]=zscore(sub[c])
print(f"\n[校舎サブサンプル n={len(sub)}  早稲田塾{int(sub['waseda'].sum())} / 東進衛星{int((sub['waseda']==0).sum())}]")
w1=smf.ols('pot ~ waseda',data=sub).fit(cov_type='HC3')
w2=smf.ols('pot ~ waseda + essay',data=sub).fit(cov_type='HC3')
w3=smf.ols('pot ~ waseda + essay + grade + rank',data=sub).fit(cov_type='HC3')
print(f"   早稲田塾の生の差: {w1.params['waseda']:+.1f}点 (p={w1.pvalues['waseda']:.4f})")
print(f"   作文スコア統制後: {w2.params['waseda']:+.1f}点 (p={w2.pvalues['waseda']:.4f})")
print(f"   作文+学年+ランク統制後: {w3.params['waseda']:+.1f}点 (p={w3.pvalues['waseda']:.4f})")
raw=pg.corr(sub['waseda'],sub['pot']).iloc[0]; par=pg.partial_corr(sub,x='waseda',y='pot',covar='essay').iloc[0]
print(f"   偏相関: 生r={raw['r']:+.3f} → 偏r(作文統制)={par['r']:+.3f}  残存率={par['r']/raw['r']*100:.0f}%")
we=smf.ols('essay ~ waseda',data=sub).fit(cov_type='HC3')
print(f"   （参考）早稲田塾の作文AIスコア差: {we.params['waseda']:+.2f}点/15 (p={we.pvalues['waseda']:.4f})")

# ---- FIGURE: raw vs essay-controlled standardized effect ----
labels=['学年\n(高1→高3)','高校ランク','校舎\n(早稲田塾)']
raw_b=[abs(pg.corr(full['grade'],full['pot']).iloc[0]['r']),
       abs(pg.corr(full['rank'],full['pot']).iloc[0]['r']),
       abs(pg.corr(sub['waseda'],sub['pot']).iloc[0]['r'])]
par_b=[abs(pg.partial_corr(full,x='grade',y='pot',covar='essay').iloc[0]['r']),
       abs(pg.partial_corr(full,x='rank',y='pot',covar='essay').iloc[0]['r']),
       abs(pg.partial_corr(sub,x='waseda',y='pot',covar='essay').iloc[0]['r'])]
fig,ax=plt.subplots(figsize=(7,4.4))
x=np.arange(3); w=0.38
ax.bar(x-w/2,raw_b,w,color=OR,label='生の相関（属性 vs 東大スコア）')
ax.bar(x+w/2,par_b,w,color=AC,label='作文AIスコアを統制後（偏相関）')
for xi,v in zip(x-w/2,raw_b): ax.text(xi,v+0.008,f"{v:.2f}",ha='center',fontsize=9,color=GR)
for xi,v in zip(x+w/2,par_b): ax.text(xi,v+0.008,f"{v:.2f}",ha='center',fontsize=10,color=DK)
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel('|相関係数|')
ax.set_title('属性差は作文力で説明できるか：作文スコア統制で縮む量',fontproperties=T(13))
ax.legend(fontsize=9); ax.set_ylim(0,max(raw_b)*1.25)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('fig3_confound.png',dpi=160); plt.close()
print("\nsaved fig3_confound.png")
