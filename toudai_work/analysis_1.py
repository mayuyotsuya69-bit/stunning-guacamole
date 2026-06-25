# -*- coding: utf-8 -*-
# ① ROC/AUC のみ。過去答案の「作文AIスコア(合計0-15)」は旧採点基準のため完全に不使用。
# 東大推薦ポテンシャルスコアは現行基準として扱う（②の作文スコア比較は実施不可・保留）。
import numpy as np, pandas as pd
from scipy import stats
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'; fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name(); plt.rcParams['axes.unicode_minus']=False
AC,DK,OR,LT,GR='#3E8C7C','#2E6457','#C2603F','#E7F1EE','#5C6663'

p = pd.read_csv('/root/.claude/uploads/c914e650-c81c-5244-ac94-41f0b5293dbd/bfd2100a-_________.csv')
d = p.drop_duplicates(subset='タイトル', keep='first').reset_index(drop=True)
d = d.rename(columns={'東大推薦ポテンシャルスコア(0-100)':'pot','東大合否':'y'})
# 作文AIスコア(合計スコア)は読み込まない＝完全排除
y=d['y'].values.astype(int); pot=d['pot'].values.astype(float)
n1,n0=int(y.sum()),int((1-y).sum())
d[['y','pot']].to_csv('past_clean.csv',index=False)

def midrank(x):
    J=np.argsort(x);Z=x[J];N=len(x);T=np.zeros(N);i=0
    while i<N:
        j=i
        while j<N and Z[j]==Z[i]: j+=1
        T[i:j]=0.5*(i+j-1)+1;i=j
    T2=np.empty(N);T2[J]=T;return T2
def fastDeLong(pr,m):
    pos=pr[:,:m];neg=pr[:,m:];k=pr.shape[0];n=neg.shape[1]
    tx=np.empty([k,m]);ty=np.empty([k,n]);tz=np.empty([k,m+n])
    for r in range(k): tx[r]=midrank(pos[r]);ty[r]=midrank(neg[r]);tz[r]=midrank(pr[r])
    auc=tz[:,:m].sum(1)/m/n-(m+1.0)/2.0/n
    sx=np.cov((tz[:,:m]-tx)/n);sy=np.cov(1.0-(tz[:,m:]-ty)/m)
    return auc,np.atleast_2d(sx/m+sy/n)
def delong_ci(yt,sc,a=0.95):
    o=np.argsort(-yt,kind='mergesort');lc=int(yt.sum())
    auc,cov=fastDeLong(sc[o][None,:],lc);auc=auc[0];se=np.sqrt(cov[0,0])
    z=stats.norm.ppf(0.5+a/2);return auc,se,max(0,auc-z*se),min(1,auc+z*se)

print("="*72);print("① ROC/AUC（再計算）：東大推薦ポテンシャルスコア → 実際の東大推薦合否")
print("  ※過去答案の作文AIスコア(旧基準)は解析から完全排除")
print("="*72)
print(f"n={len(y)} 合格={n1} 不合格={n0}")
auc,se,lo,hi=delong_ci(y,pot)
print(f"AUC={auc:.3f}  95%CI(DeLong)=[{lo:.3f},{hi:.3f}]  SE={se:.3f}")
rng=np.random.default_rng(42);i0=np.where(y==0)[0];i1=np.where(y==1)[0];bs=[]
for _ in range(5000):
    b=np.concatenate([rng.choice(i0,len(i0)),rng.choice(i1,len(i1))]);bs.append(roc_auc_score(y[b],pot[b]))
bl,bh=np.percentile(bs,[2.5,97.5]);print(f"AUC 95%CI(bootstrap)=[{bl:.3f},{bh:.3f}]")
U,pmw=stats.mannwhitneyu(pot[y==1],pot[y==0]);print(f"Mann-Whitney p={pmw:.2e}")
print(f"合格 vs 不合格 平均: {pot[y==1].mean():.1f} vs {pot[y==0].mean():.1f}")
fpr,tpr,thr=roc_curve(y,pot);ji=np.argmax(tpr-fpr);ythr=thr[ji]
def met(t):
    pr=(pot>=t).astype(int)
    TP=int(((pr==1)&(y==1)).sum());FP=int(((pr==1)&(y==0)).sum())
    TN=int(((pr==0)&(y==0)).sum());FN=int(((pr==0)&(y==1)).sum())
    return dict(TP=TP,FP=FP,TN=TN,FN=FN,sens=TP/(TP+FN),spec=TN/(TN+FP),
               ppv=TP/(TP+FP) if TP+FP else float('nan'),acc=(TP+TN)/len(y))
m=met(ythr);print(f"\nYouden最適閾値={ythr:.0f}点: 感度{m['sens']:.1%} 特異度{m['spec']:.1%} PPV{m['ppv']:.1%} 正解率{m['acc']:.1%} (TP{m['TP']}/FP{m['FP']}/TN{m['TN']}/FN{m['FN']})")
m85=met(85);print(f"運用閾値85点: 感度{m85['sens']:.1%} 特異度{m85['spec']:.1%} PPV{m85['ppv']:.1%}")

fig,ax=plt.subplots(figsize=(6.2,6))
ax.plot([0,1],[0,1],'--',color=GR,lw=1);ax.plot(fpr,tpr,color=AC,lw=2.6)
ax.fill_between(fpr,tpr,alpha=0.12,color=AC)
ax.scatter([m['FP']/n0],[m['sens']],color=OR,zorder=5,s=70)
ax.annotate(f"最適閾値 {ythr:.0f}点\n感度{m['sens']:.0%}・特異度{m['spec']:.0%}",(m['FP']/n0,m['sens']),
            xytext=(0.42,0.45),color=OR,fontsize=10,arrowprops=dict(arrowstyle='->',color=OR))
ax.text(0.55,0.10,f"AUC = {auc:.3f}\n95%CI [{lo:.2f}, {hi:.2f}]\n(n={len(y)})",fontsize=12,color=DK,
        bbox=dict(boxstyle='round',fc=LT,ec=AC))
ax.set_xlabel('偽陽性率 (1 − 特異度)');ax.set_ylabel('真陽性率 (感度)')
ax.set_title('ROC曲線：東大推薦スコアによる実合否の判別',fontproperties=fm.FontProperties(fname=fp,size=13))
ax.set_xlim(-0.02,1.02);ax.set_ylim(-0.02,1.02)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout();plt.savefig('fig1_roc.png',dpi=160);plt.close();print("saved fig1_roc.png")
