# -*- coding: utf-8 -*-
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
fp='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'; fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name(); plt.rcParams['axes.unicode_minus']=False
def T(s): return fm.FontProperties(fname=fp,size=s)
AC,DK,OR,LT,GR='#3E8C7C','#2E6457','#C2603F','#E7F1EE','#5C6663'

# ---- Fig A: 閾値トレードオフ（2分布） ----
x=np.linspace(0,100,500)
def g(m,s): return np.exp(-0.5*((x-m)/s)**2)/(s*np.sqrt(2*np.pi))
fail=g(42,16); pas=g(65,17)
thr=64
fig,ax=plt.subplots(figsize=(7.2,4.3))
ax.plot(x,fail,color=GR,lw=2); ax.plot(x,pas,color=AC,lw=2.2)
ax.fill_between(x,fail,where=(x>=thr),color=OR,alpha=0.35)
ax.fill_between(x,pas,where=(x>=thr),color=AC,alpha=0.30)
ax.axvline(thr,color=DK,lw=2,ls='--')
ax.text(thr+1,ax.get_ylim()[1]*0.96,'閾値（この線で合否を予測）',fontproperties=T(11),color=DK,va='top')
ax.text(30,g(42,16).max()*0.55,'不合格者',fontproperties=T(12),color=GR,ha='center')
ax.text(78,g(65,17).max()*0.62,'合格者',fontproperties=T(12),color=DK,ha='center')
ax.annotate('正しく拾えた合格者\n（＝感度）',(80,0.004),xytext=(86,0.018),fontproperties=T(10),color=DK,
            ha='center',arrowprops=dict(arrowstyle='->',color=AC))
ax.annotate('誤って合格と判定\n（不合格者の取り違え）',(67,0.002),xytext=(50,0.020),fontproperties=T(10),color=OR,
            ha='center',arrowprops=dict(arrowstyle='->',color=OR))
ax.set_xlabel('東大推薦スコア',fontproperties=T(11)); ax.set_yticks([])
ax.set_title('閾値はトレードオフ：右に動かすと誤判定は減るが取りこぼしは増える',fontproperties=T(12.5))
for s in ['top','right','left']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('figA_threshold.png',dpi=160); plt.close()

# ---- Fig B: ROC/AUC 概念図 ----
f=np.linspace(0,1,200); t=f**0.32   # concave good curve
fig,ax=plt.subplots(figsize=(6.0,5.6))
ax.plot([0,1],[0,1],'--',color=GR,lw=1.5)
ax.text(0.55,0.50,'でたらめ\n（AUC=0.5）',fontproperties=T(10),color=GR,rotation=33,ha='center')
ax.plot([0,0,1],[0,1,1],color=DK,lw=1.2,alpha=0.5)
ax.text(0.03,0.97,'完璧（AUC=1.0）',fontproperties=T(9.5),color=DK,va='top')
ax.plot(f,t,color=AC,lw=2.8); ax.fill_between(f,t,color=AC,alpha=0.13)
ax.text(0.52,0.30,'AUC\n＝曲線の下の面積',fontproperties=T(12),color=DK,ha='center')
ax.scatter([f[60]],[t[60]],color=OR,s=70,zorder=5)
ax.annotate('ある閾値での成績\n（縦=感度／横=誤判定率）',(f[60],t[60]),xytext=(0.40,0.70),
            fontproperties=T(10),color=OR,ha='center',arrowprops=dict(arrowstyle='->',color=OR))
ax.annotate('左上ほど良い',(0.08,0.93),xytext=(0.30,0.86),fontproperties=T(10.5),color=DK,
            arrowprops=dict(arrowstyle='->',color=DK))
ax.set_xlabel('誤判定率（1−特異度）',fontproperties=T(11)); ax.set_ylabel('感度（合格者を拾えた割合）',fontproperties=T(11))
ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.02,1.02)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig('figB_roc_concept.png',dpi=160); plt.close()
print('saved figA_threshold.png, figB_roc_concept.png')
