const pptxgen=require("pptxgenjs"); const p=new pptxgen();
p.defineLayout({name:"W",width:13.333,height:7.5}); p.layout="W";
const AC="3E8C7C",DK="2E6457",OR="C2603F",LT="E7F1EE",BK="1A1A1A",GR="5C6663",WH="FFFFFF",F="游ゴシック";
const sh=()=>({type:"outer",color:"BFBFBF",blur:6,offset:2,angle:90,opacity:0.35});
function header(s,k,t){ s.background={color:WH};
  s.addShape(p.ShapeType.rect,{x:0,y:0,w:0.28,h:7.5,fill:{color:AC}});
  s.addText(k,{x:0.6,y:0.34,w:12,h:0.4,fontFace:F,bold:true,fontSize:13,color:OR,charSpacing:1});
  s.addText(t,{x:0.6,y:0.66,w:12.2,h:0.7,fontFace:F,bold:true,fontSize:23,color:DK});
  s.addShape(p.ShapeType.line,{x:0.62,y:1.5,w:12.1,h:0,line:{color:AC,width:1.5}}); }
function foot(s,t){ s.addText(t,{x:0.6,y:7.08,w:12.2,h:0.32,fontFace:F,fontSize:9,color:GR}); }
function bl(s,x,y,w,items){ s.addText(items.map(it=>({text:it.t,options:{bullet:it.b!==false?{code:"2022",indent:14}:false,
  fontFace:F,bold:!!it.bold,fontSize:it.fs||13,color:it.c||BK,breakLine:true,paraSpaceAfter:9}})),{x,y,w,h:5,valign:"top"}); }

/* Slide 1: 循環論法 concept */
let s=p.addSlide(); header(s,"補足 ｜ 属性差の読み方 (1/2)","「高3・早稲田塾が高い」だけでは、妥当性の証明にならない");
s.addImage({path:"figC_confound_diagram.png",x:0.5,y:1.7,w:7.5,h:4.2,shadow:sh()});
bl(s,8.2,1.75,4.7,[
 {t:"観察：早稲田塾の生徒は東大スコアが高い（79点 vs 63点）",bold:true,fs:13,c:DK},
 {t:"一見、スコアが“優秀な層”を見抜けている証拠に見える",fs:12.5},
 {t:"でもその層は そもそも作文が上手い。東大スコアは作文スコアと相関0.78（≒8割同じ動き）",fs:12.5},
 {t:"＝差の原因は「スコアの実力」ではなく「作文力」かもしれない（循環論法の危険）",bold:true,fs:12.5,c:OR},
]);
foot(s,"循環論法＝『作文が上手い層は作文スコアが高い』という当たり前を、言い換えて“妥当性”と呼んでしまう誤り。");

/* Slide 2: evidence */
s=p.addSlide(); header(s,"補足 ｜ 属性差の読み方 (2/2)","作文力を“差し引く”と、属性差はほぼ消える");
s.addImage({path:"fig3_confound.png",x:0.5,y:1.75,w:6.5,h:4.05,shadow:sh()});
bl(s,7.25,1.7,5.6,[
 {t:"「作文の上手さが同じ生徒どうし」で比べ直す＝作文力を統制（差し引く）",bold:true,fs:13,c:DK},
 {t:"すると差は大きく縮む：学年 0.28→0.10／高校ランク 0.07→0.03／早稲田塾 +17点→ほぼ0",fs:12.5},
]);
s.addShape(p.ShapeType.rect,{x:7.25,y:3.45,w:5.55,h:1.5,fill:{color:LT},line:{color:AC,width:1}});
s.addText([{text:"決め手　",options:{fontFace:F,bold:true,fontSize:12.5,color:DK}},
 {text:"同じ属性が「作文スコア」を予測する強さ(0.285)と「東大スコア」を予測する強さ(0.278)はほぼ同じ。＝属性差の正体は作文力だと分かる。",options:{fontFace:F,fontSize:12,color:BK}}],
 {x:7.45,y:3.57,w:5.2,h:1.28,valign:"middle"});
s.addShape(p.ShapeType.rect,{x:7.25,y:5.15,w:5.55,h:1.35,fill:{color:DK}});
s.addText([{text:"だから①が本命　",options:{fontFace:F,bold:true,fontSize:12.5,color:WH}},
 {text:"属性比較では妥当性を示せない。実際の合否そのものと照合する①ROC/AUCこそが、循環論法を受けない直接の証拠。",options:{fontFace:F,fontSize:12,color:WH}}],
 {x:7.45,y:5.27,w:5.2,h:1.13,valign:"middle"});
foot(s,"出典：現役 n=582。偏相関＝作文AIスコアを共変量に統制した属性と東大スコアの関係。係数は標準化回帰係数。");

p.writeFile({fileName:"補足_属性差の読み方.pptx"}).then(f=>console.log("WROTE",f));
