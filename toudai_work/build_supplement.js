const pptxgen=require("pptxgenjs"); const p=new pptxgen();
p.defineLayout({name:"W",width:13.333,height:7.5}); p.layout="W";
const AC="3E8C7C",DK="2E6457",OR="C2603F",LT="E7F1EE",BK="1A1A1A",GR="5C6663",WH="FFFFFF",F="游ゴシック";
const sh=()=>({type:"outer",color:"BFBFBF",blur:6,offset:2,angle:90,opacity:0.35});
function header(s,k,t){ s.background={color:WH};
  s.addShape(p.ShapeType.rect,{x:0,y:0,w:0.28,h:7.5,fill:{color:AC}});
  s.addText(k,{x:0.6,y:0.34,w:12,h:0.4,fontFace:F,bold:true,fontSize:13,color:OR,charSpacing:1});
  s.addText(t,{x:0.6,y:0.66,w:12.2,h:0.7,fontFace:F,bold:true,fontSize:24,color:DK});
  s.addShape(p.ShapeType.line,{x:0.62,y:1.5,w:12.1,h:0,line:{color:AC,width:1.5}}); }
function foot(s,t){ s.addText(t,{x:0.6,y:7.08,w:12.2,h:0.32,fontFace:F,fontSize:9,color:GR}); }
function bl(s,x,y,w,items){ s.addText(items.map(it=>({text:it.t,options:{bullet:it.b!==false?{code:"2022",indent:14}:false,
  fontFace:F,bold:!!it.bold,fontSize:it.fs||13,color:it.c||BK,breakLine:true,paraSpaceAfter:9}})),{x,y,w,h:5,valign:"top"}); }

/* Slide 1: 閾値トレードオフ */
let s=p.addSlide(); header(s,"補足 ｜ ROC・AUCの読み方 (1/2)","「線引き（閾値）」には、ちょうど良い一点が無い");
s.addImage({path:"figA_threshold.png",x:0.5,y:1.7,w:7.3,h:4.36,shadow:sh()});
bl(s,8.05,1.8,4.85,[
 {t:"スコアで合否を予測するには「何点以上を合格とみなすか」の線引きが要る",bold:true,fs:13.5,c:DK},
 {t:"線を右へ：誤判定は減るが、合格者の取りこぼしが増える",fs:13},
 {t:"線を左へ：合格者をよく拾えるが、不合格者まで合格と誤判定",fs:13},
 {t:"＝1つの閾値の成績だけでは、スコア自体の良し悪しは測れない",bold:true,fs:13,c:OR},
]);
foot(s,"図は説明用の模式図（実データの平均値 合格65点・不合格42点に近い形で作成）。");

/* Slide 2: AUCの意味 */
s=p.addSlide(); header(s,"補足 ｜ ROC・AUCの読み方 (2/2)","ROC曲線とAUC：あらゆる閾値での実力を1枚に");
s.addImage({path:"figB_roc_concept.png",x:0.5,y:1.7,w:5.0,h:4.66,shadow:sh()});
bl(s,5.75,1.7,7.1,[
 {t:"ROC曲線：閾値を全範囲で動かしたときの「感度(縦)」と「誤判定率(横)」の軌跡。左上に張り付くほど良い",fs:13},
 {t:"斜め45度線＝でたらめ（コインで当てるのと同じ）。曲線がそこから上に膨らむ量が実力",fs:13},
 {t:"AUC＝曲線の下の面積。0.5=でたらめ／0.8=良好／1.0=完璧",bold:true,fs:13.5,c:DK},
]);
s.addShape(p.ShapeType.rect,{x:5.75,y:4.0,w:7.05,h:1.18,fill:{color:LT},line:{color:AC,width:1}});
s.addText([{text:"いちばん直感的な意味　",options:{fontFace:F,bold:true,fontSize:13,color:DK}},
 {text:"AUC＝「合格者と不合格者を1人ずつ無作為に選ぶと、合格者の方がスコアが高い確率」。今回0.83＝100回中83回。",options:{fontFace:F,fontSize:12.5,color:BK}}],
 {x:5.95,y:4.13,w:6.65,h:0.95,valign:"middle"});
// glossary row
const gy=5.45;
[["感度","実際の合格者を拾えた割合（今回68%）"],["特異度","実際の不合格者を正しく外せた割合（88%）"],["的中率","合格予測が当たった割合（87%）"]].forEach((c,i)=>{
  const x=5.75+i*2.38;
  s.addShape(p.ShapeType.rect,{x,y:gy,w:2.25,h:1.0,fill:{color:WH},line:{color:AC,width:1}});
  s.addText([{text:c[0]+"\n",options:{fontFace:F,bold:true,fontSize:12,color:AC}},
   {text:c[1],options:{fontFace:F,fontSize:9.5,color:BK}}],{x:x+0.1,y:gy+0.05,w:2.05,h:0.9,valign:"top"});
});
foot(s,"95%信頼区間：n=36と少ないため AUC=0.83 の真値は 0.70〜0.96 の幅。点推定は高いが、確証には今後の件数追加が必要（誠実注記）。");

p.writeFile({fileName:"補足_ROC・AUCの読み方.pptx"}).then(f=>console.log("WROTE",f));
