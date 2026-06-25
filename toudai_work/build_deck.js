const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.defineLayout({ name:"W", width:13.333, height:7.5 }); p.layout="W";
const AC="3E8C7C",DK="2E6457",OR="C2603F",LT="E7F1EE",BK="1A1A1A",GR="5C6663",WH="FFFFFF";
const W3="ヒラギノ角ゴシック W3", W6="ヒラギノ角ゴシック W6";
const sh=()=>({type:"outer",color:"BFBFBF",blur:6,offset:2,angle:90,opacity:0.35});
function header(s,k,t){ s.background={color:WH};
  s.addShape(p.ShapeType.rect,{x:0,y:0,w:0.28,h:7.5,fill:{color:AC}});
  s.addText(k,{x:0.6,y:0.34,w:12,h:0.4,fontFace:W6,fontSize:13,color:OR,charSpacing:1});
  s.addText(t,{x:0.6,y:0.66,w:12.2,h:0.7,fontFace:W6,fontSize:24,color:DK});
  s.addShape(p.ShapeType.line,{x:0.62,y:1.5,w:12.1,h:0,line:{color:AC,width:1.5}}); }
function foot(s,t){ s.addText(t,{x:0.6,y:7.06,w:12.2,h:0.32,fontFace:W3,fontSize:9,color:GR}); }
function bullets(s,x,y,w,items){
  s.addText(items.map(it=>({text:it.t,options:{bullet:it.b!==false?{code:"2022",indent:14}:false,
    fontFace:it.bold?W6:W3,fontSize:it.fs||13,color:it.c||BK,breakLine:true,paraSpaceAfter:8}})),
    {x,y,w,h:4.5,valign:"top"}); }

/* Slide 1: title */
let s=p.addSlide(); s.background={color:WH};
s.addShape(p.ShapeType.rect,{x:0,y:5.55,w:13.333,h:1.95,fill:{color:LT}});
s.addShape(p.ShapeType.rect,{x:0,y:0,w:13.333,h:0.22,fill:{color:AC}});
s.addText("取り組み④",{x:0.9,y:1.7,w:12,h:0.5,fontFace:W6,fontSize:16,color:OR,charSpacing:1});
s.addText("東大推薦スコアの妥当性検証",{x:0.9,y:2.25,w:12,h:1.0,fontFace:W6,fontSize:38,color:DK});
s.addText([{text:"「東大推薦ポテンシャルスコア」は、実際の東大推薦合格を当てられるか",options:{breakLine:true,fontFace:W3,fontSize:16,color:BK,paraSpaceAfter:4}},
 {text:"face validity（属性での見た目の妥当性）→ criterion validity（合否との照合）への格上げ",options:{fontFace:W3,fontSize:13,color:GR}}],
 {x:0.9,y:3.5,w:11.5,h:1.2});
s.addText("志作文 AI評価プロジェクト ／ コンテンツ本部 小論文リーダーチーム",{x:0.9,y:5.95,w:11.5,h:0.4,fontFace:W6,fontSize:13,color:DK});
s.addText("検証データ：過去答案 n=36（合格19・不合格17）／現役 n=589",{x:0.9,y:6.4,w:11.5,h:0.4,fontFace:W3,fontSize:12,color:GR});

/* Slide 2: ① ROC/AUC */
s=p.addSlide(); header(s,"① ROC / AUC ｜ 本命の検証","実際の合格者を AUC=0.83 で判別できる");
s.addImage({path:"fig1_roc.png",x:0.55,y:1.75,w:5.25,h:5.07,shadow:sh()});
bullets(s,6.2,1.85,6.7,[
 {t:"AUC = 0.830（95%CI 0.70–0.96／ブートストラップ 0.68–0.94）",bold:true,fs:15,c:DK},
 {t:"合格者と不合格者を分離（Mann–Whitney p = 7.8×10⁻⁴）",fs:13},
 {t:"最適閾値 64点：感度 68%・特異度 88%・的中率 87%・正解率 78%",fs:13},
 {t:"高精度運用（85点以上）：特異度 100%・的中率 100%（網羅は限定）",fs:13},
]);
s.addShape(p.ShapeType.rect,{x:6.2,y:4.55,w:6.55,h:1.95,fill:{color:LT},line:{color:AC,width:1}});
s.addText([{text:"読み方　",options:{fontFace:W6,fontSize:13,color:DK}},
 {text:"AUC=0.83 は「無作為に選んだ合格者の方が不合格者よりスコアが高い確率が83%」。",options:{fontFace:W3,fontSize:12.5,color:BK,breakLine:true,paraSpaceAfter:4}},
 {text:"属性比較ではなく『実際の合否』そのものを正解ラベルにした、最も直接的な妥当性検証。",options:{fontFace:W3,fontSize:12.5,color:BK}}],
 {x:6.4,y:4.7,w:6.2,h:1.7,valign:"top"});
foot(s,"出典：過去答案 n=36（合格19/不合格17）。重複答案は最新版を採用。本スコアのみで判別、作文スコアは不使用。n小につき点推定は高くてもCIは広く、確証には今後のサンプル追加が必要（誠実注記）。");

/* Slide 3: ③ 交絡調整 */
s=p.addSlide(); header(s,"② 交絡調整 ｜ 属性差の正体","属性差（学年・校舎等）は概ね『作文力』で説明できる");
s.addImage({path:"fig3_confound.png",x:0.55,y:1.95,w:5.95,h:3.86,shadow:sh()});
bullets(s,6.75,1.8,6.1,[
 {t:"作文AIスコアを統制すると、学年・高校ランク・校舎の差は大きく縮小",bold:true,fs:14,c:DK},
 {t:"学年：偏相関 0.28→0.10／高校ランク：0.07→0.03／校舎(早稲田塾) 生差+17点→統制後ほぼ0",fs:12.5},
 {t:"決め手：同じ属性が「作文スコア」を予測するβ(+0.285)と「東大スコア」を予測するβ(+0.278)はほぼ同一",fs:12.5},
]);
s.addShape(p.ShapeType.rect,{x:6.75,y:4.5,w:6.0,h:1.95,fill:{color:LT},line:{color:AC,width:1}});
s.addText([{text:"結論　",options:{fontFace:W6,fontSize:13,color:DK}},
 {text:"「高3が高い」「早稲田塾が高い」等の属性差は、その層が作文を上手く書くことの反映。",options:{fontFace:W3,fontSize:12.5,color:BK,breakLine:true,paraSpaceAfter:4}},
 {text:"＝属性比較だけでは妥当性を示せない。だからこそ①（合否との直接照合）が本命となる。",options:{fontFace:W3,fontSize:12.5,color:BK}}],
 {x:6.95,y:4.65,w:5.65,h:1.7,valign:"top"});
foot(s,"出典：現役 n=582（学年589・高校ランク582・校舎374で実施）。現行基準の作文AIスコアを共変量に統制。性別は提供データに無し。");

/* Slide 4: 結論 */
s=p.addSlide(); s.background={color:DK};
s.addShape(p.ShapeType.rect,{x:0,y:0,w:13.333,h:0.22,fill:{color:OR}});
s.addText("結論",{x:0.9,y:0.7,w:12,h:0.6,fontFace:W6,fontSize:16,color:LT,charSpacing:2});
s.addText("東大推薦スコアは、実際の合格者を AUC=0.83 で判別する",{x:0.9,y:1.4,w:11.6,h:1.4,fontFace:W6,fontSize:30,color:WH,lineSpacingMultiple:1.1});
s.addText([
 {text:"・ 過去の実合否で AUC=0.83（95%CI 0.70–0.96）。最適閾値で特異度88%・的中率87%。",options:{fontFace:W3,fontSize:16,color:WH,breakLine:true,paraSpaceAfter:10}},
 {text:"・ 属性差（学年・校舎等）の正体は概ね作文力。属性比較では示せない妥当性を、実際の合否との直接照合で確認した。",options:{fontFace:W3,fontSize:16,color:WH,breakLine:true,paraSpaceAfter:10}},
 {text:"・ 「作文スコアを超える予測（増分妥当性）」は、過去答案の作文スコアが旧採点基準のため保留。現行基準で再採点後に追加検証する。",options:{fontFace:W3,fontSize:16,color:WH}},
],{x:0.95,y:3.2,w:11.5,h:2.3,valign:"top"});
s.addShape(p.ShapeType.rect,{x:0.9,y:6.15,w:11.5,h:0.82,fill:{color:AC}});
s.addText("誠実注記：過去検証は n=36 と小規模。点推定は高いが信頼区間は広く、確証には今後の合否サンプル追加で再検証する。",
 {x:1.1,y:6.22,w:11.1,h:0.68,fontFace:W3,fontSize:12.5,color:WH,valign:"middle"});

p.writeFile({fileName:"取り組み④_東大推薦スコアの妥当性.pptx"}).then(f=>console.log("WROTE",f));
