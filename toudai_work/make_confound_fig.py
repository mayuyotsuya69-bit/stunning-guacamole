# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager as fm
fp='/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'; fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name(); plt.rcParams['axes.unicode_minus']=False
def T(s): return fm.FontProperties(fname=fp,size=s)
AC,DK,OR,LT,GR='#3E8C7C','#2E6457','#C2603F','#E7F1EE','#5C6663'

fig,ax=plt.subplots(figsize=(8.2,4.6)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
def box(x,y,w,h,lines,fc,ec,tc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.12",
                fc=fc,ec=ec,lw=2))
    ax.text(x+w/2,y+h/2,lines,ha='center',va='center',fontproperties=T(12.5),color=tc)
# boxes
box(0.3,3.6,3.0,1.5,"属性\n（高3・早稲田塾・上位校）",LT,AC,DK)
box(3.7,1.0,2.6,1.4,"作文力\n（作文の上手さ）",'#FBEYE' if False else '#F6E4DC',OR,OR)
box(6.9,3.6,2.8,1.5,"東大推薦スコア",LT,AC,DK)
# arrows: 属性->作文力, 作文力->東大スコア (real chain, solid green)
ax.add_patch(FancyArrowPatch((1.8,3.6),(4.3,2.4),arrowstyle='-|>',mutation_scale=20,color=AC,lw=2.4))
ax.add_patch(FancyArrowPatch((6.3,2.4),(8.0,3.6),arrowstyle='-|>',mutation_scale=20,color=AC,lw=2.4))
ax.text(2.4,2.75,'上手い層が\n集まる',fontproperties=T(10),color=AC,ha='center')
ax.text(7.7,2.75,'作文が上手いと\nスコアも高い',fontproperties=T(10),color=AC,ha='center')
# direct dashed arrow 属性->東大スコア with ? (spurious)
ax.add_patch(FancyArrowPatch((3.3,4.45),(6.9,4.45),arrowstyle='-|>',mutation_scale=18,color=GR,lw=2,ls=(0,(4,3))))
ax.text(5.1,4.75,'作文力を差し引くと ほぼ0（？）',fontproperties=T(10.5),color=GR,ha='center')
ax.text(5.0,5.6,'「高3・早稲田塾が高い」の正体は、共通の原因＝作文力',fontproperties=T(13),color=DK,ha='center')
ax.text(5.0,0.35,'作文力という共通の原因が、属性と東大スコアの両方を押し上げている（これを交絡という）',
        fontproperties=T(10.5),color=GR,ha='center')
plt.tight_layout(); plt.savefig('figC_confound_diagram.png',dpi=160,bbox_inches='tight'); plt.close()
print('saved figC_confound_diagram.png')
