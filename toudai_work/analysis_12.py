# -*- coding: utf-8 -*-
import numpy as np, pandas as pd
from scipy import stats
import statsmodels.api as sm
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
fm.fontManager.addfont(fp)
JP = fm.FontProperties(fname=fp).get_name()
plt.rcParams['font.family']=JP; plt.rcParams['axes.unicode_minus']=False
AC, DK, OR, LT, GR = '#3E8C7C','#2E6457','#C2603F','#E7F1EE','#5C6663'

d = pd.read_csv('past_clean.csv')
y = d['y'].values.astype(int); pot = d['pot'].values.astype(float); essay = d['essay'].values.astype(float)
n1, n0 = int(y.sum()), int((1-y).sum())

# ---------- DeLong (Sun & Xu 2014) ----------
def compute_midrank(x):
    J=np.argsort(x); Z=x[J]; N=len(x); T=np.zeros(N); i=0
    while i<N:
        j=i
        while j<N and Z[j]==Z[i]: j+=1
        T[i:j]=0.5*(i+j-1)+1; i=j
    T2=np.empty(N); T2[J]=T; return T2
def fastDeLong(preds, label1count):
    m=label1count; pos=preds[:,:m]; neg=preds[:,m:]; k=preds.shape[0]; n=neg.shape[1]
    tx=np.empty([k,m]); ty=np.empty([k,n]); tz=np.empty([k,m+n])
    for r in range(k):
        tx[r]=compute_midrank(pos[r]); ty[r]=compute_midrank(neg[r]); tz[r]=compute_midrank(preds[r])
    aucs=tz[:,:m].sum(axis=1)/m/n - (m+1.0)/2.0/n
    v01=(tz[:,:m]-tx)/n; v10=1.0-(tz[:,m:]-ty)/m
    sx=np.cov(v01); sy=np.cov(v10)
    delongcov=sx/m+sy/n
    return aucs, np.atleast_2d(delongcov)
def delong_ci(yt, sc, alpha=0.95):
    order=np.argsort(-yt,kind='mergesort'); lc=int(yt.sum())
    preds=sc[order][np.newaxis,:]
    auc,cov=fastDeLong(preds,lc); auc=auc[0]; se=np.sqrt(cov[0,0])
    z=stats.norm.ppf(0.5+alpha/2); lo=auc-z*se; hi=auc+z*se
    return auc, se, max(0,lo), min(1,hi)
def delong_test(yt, s1, s2):
    order=np.argsort(-yt,kind='mergesort'); lc=int(yt.sum())
    preds=np.vstack((s1,s2))[:,order]
    aucs,cov=fastDeLong(preds,lc)
    L=np.array([[1,-1]]); var=L@cov@L.T
    z=(aucs[0]-aucs[1])/np.sqrt(var[0,0]); p=2*(1-stats.norm.cdf(abs(z)))
    return aucs, z, p

print("="*72); print("① ROC / AUC  ：東大推薦ポテンシャルスコア → 実際の東大推薦合否")
print("="*72)
print(f"n={len(y)}  合格={n1}  不合格={n0}  （重複名は上の行=最新を採用してdedup）")
auc,se,lo,hi = delong_ci(y,pot)
print(f"\nAUC = {auc:.3f}   95%CI (DeLong) = [{lo:.3f}, {hi:.3f}]   SE={se:.3f}")
# bootstrap CI
rng=np.random.default_rng(42); boots=[]
idx0=np.where(y==0)[0]; idx1=np.where(y==1)[0]
for _ in range(5000):
    b=np.concatenate([rng.choice(idx0,len(idx0)),rng.choice(idx1,len(idx1))])
    boots.append(roc_auc_score(y[b],pot[b]))
bl,bh=np.percentile(boots,[2.5,97.5])
print(f"AUC 95%CI (stratified bootstrap 5000) = [{bl:.3f}, {bh:.3f}]")
# Mann-Whitney p for AUC != 0.5
U,pmw=stats.mannwhitneyu(pot[y==1],pot[y==0],alternative='two-sided')
print(f"Mann–Whitney U p = {pmw:.2e}  (AUC≠0.5 の検定)")

fpr,tpr,thr=roc_curve(y,pot)
youden=tpr-fpr; ji=np.argmax(youden); ythr=thr[ji]
def metrics(t):
    pred=(pot>=t).astype(int)
    TP=int(((pred==1)&(y==1)).sum()); FP=int(((pred==1)&(y==0)).sum())
    TN=int(((pred==0)&(y==0)).sum()); FN=int(((pred==0)&(y==1)).sum())
    sens=TP/(TP+FN) if TP+FN else float('nan'); spec=TN/(TN+FP) if TN+FP else float('nan')
    ppv=TP/(TP+FP) if TP+FP else float('nan'); npv=TN/(TN+FN) if TN+FN else float('nan')
    acc=(TP+TN)/len(y)
    return dict(t=t,TP=TP,FP=FP,TN=TN,FN=FN,sens=sens,spec=spec,ppv=ppv,npv=npv,acc=acc)
print(f"\n■ Youden最適閾値 = {ythr:.0f}点")
m=metrics(ythr)
print(f"   感度={m['sens']:.1%}  特異度={m['spec']:.1%}  的中率PPV={m['ppv']:.1%}  NPV={m['npv']:.1%}  正解率={m['acc']:.1%}")
print(f"   混同(TP/FP/TN/FN)={m['TP']}/{m['FP']}/{m['TN']}/{m['FN']}")
print(f"\n■ 運用閾値 = 85点")
m85=metrics(85)
print(f"   感度={m85['sens']:.1%}  特異度={m85['spec']:.1%}  PPV={m85['ppv']:.1%}  NPV={m85['npv']:.1%}  TP/FP/TN/FN={m85['TP']}/{m85['FP']}/{m85['TN']}/{m85['FN']}")
for t in [60,67,70]:
    mm=metrics(t); print(f"   参考 閾値{t}点: 感度={mm['sens']:.1%} 特異度={mm['spec']:.1%} PPV={mm['ppv']:.1%} 正解率={mm['acc']:.1%}")

# ROC figure
fig,ax=plt.subplots(figsize=(6.2,6))
ax.plot([0,1],[0,1],'--',color=GR,lw=1)
ax.plot(fpr,tpr,color=AC,lw=2.6)
ax.fill_between(fpr,tpr,alpha=0.12,color=AC)
ax.scatter([m['FP']/n0],[m['sens']],color=OR,zorder=5,s=70)
ax.annotate(f"最適閾値 {ythr:.0f}点\n感度{m['sens']:.0%}・特異度{m['spec']:.0%}",
            (m['FP']/n0, m['sens']), xytext=(0.42,0.45), color=OR, fontsize=10,
            arrowprops=dict(arrowstyle='->',color=OR))
ax.text(0.55,0.10,f"AUC = {auc:.3f}\n95%CI [{lo:.2f}, {hi:.2f}]\n(n={len(y)})",fontsize=12,color=DK,
        bbox=dict(boxstyle='round',fc=LT,ec=AC))
ax.set_xlabel('偽陽性率 (1 − 特異度)'); ax.set_ylabel('真陽性率 (感度)')
ax.set_title('ROC曲線：東大推薦スコアによる実合否の判別', fontproperties=fm.FontProperties(fname=fp,size=13))
ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.02,1.02)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('fig1_roc.png',dpi=160); plt.close()
print("saved fig1_roc.png")

print("\n"+"="*72); print("② 増分妥当性：作文AIスコアを超えて合否を当てるか")
print("="*72)
print(f"作文AIスコア(0-15)範囲={essay.min():.0f}-{essay.max():.0f}  corr(pot,essay)={np.corrcoef(pot,essay)[0,1]:.3f}")
def fit(cols):
    X=sm.add_constant(d[cols]); mdl=sm.Logit(y,X).fit(disp=0,maxiter=200)
    return mdl
def looauc(cols):
    from sklearn.linear_model import LogisticRegression
    p=np.zeros(len(y))
    Xall=d[cols].values
    for i in range(len(y)):
        tr=[j for j in range(len(y)) if j!=i]
        lr=LogisticRegression(max_iter=1000)
        lr.fit(Xall[tr],y[tr]); p[i]=lr.predict_proba(Xall[i:i+1])[0,1]
    return roc_auc_score(y,p), p
models={'東大スコアのみ':['pot'],'作文スコアのみ':['essay'],'両方':['pot','essay']}
fitres={}; insample={}; loo={}
for name,cols in models.items():
    mdl=fit(cols); fitres[(name)]=mdl
    sc=mdl.predict(sm.add_constant(d[cols]))
    insample[name]=roc_auc_score(y,sc)
    lc,lp=looauc(cols); loo[name]=lc
    print(f"\n― {name}: AUC(in-sample)={insample[name]:.3f}  AUC(LOO-CV)={loo[name]:.3f}  AIC={mdl.aic:.1f}  LLF={mdl.llf:.2f}")
    for v in cols:
        b=mdl.params[v]; p=mdl.pvalues[v]; orr=np.exp(b)
        print(f"     {v}: 係数={b:+.3f}  OR={orr:.3f}(/1点)  p={p:.4f}")
# LR tests (nested)
def lrtest(full,red,dfdiff):
    stat=2*(full.llf-red.llf); p=stats.chi2.sf(stat,dfdiff); return stat,p
full=fitres['両方']; mpot=fitres['東大スコアのみ']; mess=fitres['作文スコアのみ']
s1,p1=lrtest(full,mess,1)
s2,p2=lrtest(full,mpot,1)
print(f"\n■ 尤度比検定（増分）:")
print(f"   作文スコアモデルに東大スコアを追加 → χ²(1)={s1:.2f}, p={p1:.4f}  ※東大スコアの上乗せ予測")
print(f"   東大スコアモデルに作文スコアを追加 → χ²(1)={s2:.2f}, p={p2:.4f}  ※作文スコアの上乗せ予測")
# DeLong compare single-predictor AUCs
aucs,z,pdl=delong_test(y,pot,essay)
print(f"\n■ AUC比較（DeLong）: 東大スコア単独 AUC={aucs[0]:.3f} vs 作文スコア単独 AUC={aucs[1]:.3f}  z={z:.2f}, p={pdl:.4f}")

# fig2: incremental AUC bars (LOO honest)
fig,ax=plt.subplots(figsize=(6.6,4.2))
names=list(models.keys()); vals=[loo[n] for n in names]; insv=[insample[n] for n in names]
xpos=np.arange(len(names)); w=0.38
b1=ax.bar(xpos-w/2,insv,w,color=LT,edgecolor=AC,label='in-sample AUC')
b2=ax.bar(xpos+w/2,vals,w,color=AC,label='LOO-CV AUC（汎化性能）')
for x,v in zip(xpos-w/2,insv): ax.text(x,v+0.01,f"{v:.2f}",ha='center',fontsize=9,color=GR)
for x,v in zip(xpos+w/2,vals): ax.text(x,v+0.01,f"{v:.2f}",ha='center',fontsize=10,color=DK,fontweight='bold')
ax.axhline(0.5,ls='--',color=GR,lw=1); ax.set_ylim(0,1.05)
ax.set_xticks(xpos); ax.set_xticklabels(names); ax.set_ylabel('AUC')
ax.set_title('増分妥当性：予測モデル別のAUC', fontproperties=fm.FontProperties(fname=fp,size=13))
ax.legend(fontsize=9, loc='lower right')
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('fig2_incremental.png',dpi=160); plt.close()
print("saved fig2_incremental.png")
