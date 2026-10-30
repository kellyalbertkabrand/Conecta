const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const dir=process.argv[2]; const S=JSON.parse(fs.readFileSync(path.join(dir,'..','spec3.json')));
const kw=s=>s.replace(/"([^"]+)"/g,'<b>$1</b>').replace(/\n/g,'<br>');
const css=`@font-face{font-family:Sora;src:url(sora-var.woff2) format('woff2');font-weight:100 800}
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;background:transparent;font-family:Sora;color:#fff}
.veil{position:absolute;left:0;right:0;bottom:0;height:1150px;background:linear-gradient(180deg,rgba(10,18,34,0),rgba(10,18,34,.6) 40%,rgba(10,18,34,.93))}
.topveil{position:absolute;left:0;right:0;top:0;height:520px;background:linear-gradient(180deg,rgba(10,18,34,.7),rgba(10,18,34,0))}
.logo{position:absolute;top:150px;left:80px;display:flex;align-items:center;gap:18px}.logo .s{height:60px}.logo .w{height:27px}
.box{position:absolute;left:80px;right:150px;bottom:470px}
.tag{font-weight:600;font-size:28px;letter-spacing:.22em;color:#00CEC9;text-transform:uppercase;margin-bottom:28px}
h1{font-weight:250;font-size:84px;line-height:1.1;letter-spacing:-.01em}h1 b{font-weight:800;color:#00CEC9}
.line{width:100px;height:4px;background:#00CEC9;margin-top:36px}
.sub{font-weight:300;font-size:32px;line-height:1.4;color:#C8D6E5;margin-top:30px}
.li{font-weight:300;font-size:70px;line-height:1.25;display:flex;align-items:center;gap:26px}.li i{font-style:normal;font-weight:200;font-size:34px;color:#00CEC9;width:60px}
.nome{position:absolute;top:930px;left:80px;max-width:820px;background:rgba(15,27,51,.86);border-left:6px solid #00CEC9;padding:26px 34px 28px}
.nome .tag{font-size:22px;margin-bottom:14px}.nome .n{font-weight:700;font-size:48px;text-transform:uppercase;letter-spacing:.02em;line-height:1.1}
.nome .s2{font-weight:300;font-size:30px;color:#C8D6E5;margin-top:10px}
.cap{position:absolute;left:110px;right:150px;bottom:500px;text-align:center;font-weight:600;font-size:56px;line-height:1.22;text-shadow:0 3px 14px rgba(0,0,0,.85),0 0 3px rgba(0,0,0,.9)}
.cap b{font-weight:800;color:#00CEC9}`;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const shot=async(name,body,transp=true)=>{fs.writeFileSync(path.join(dir,'_t.html'),`<html><head><style>${css}</style></head><body>${body}</body></html>`);
 await p.goto('file://'+path.join(dir,'_t.html'),{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:path.join(dir,name+'.png'),omitBackground:transp});};
await shot('logo',`<div class="topveil"></div><div class="logo"><img class="s" src="conecta-simbolo-branco.png"><img class="w" src="conecta-wordmark-branco.png"></div>`);
await shot('veil',`<div class="veil" style="height:900px"></div>`);
for(const [k,o] of Object.entries(S.frases)){
 let inner='';
 if(o.lista) inner+=o.lista.map((x,i)=>`<div class="li"><i>0${i+1}</i>${x}</div>`).join('');
 else inner+=`<h1${o.grande?' style="font-size:132px;line-height:1.02"':''}>${kw(o.h)}</h1>`;
 inner+=`<div class="line"></div>`+(o.sub?`<div class="sub">${kw(o.sub)}</div>`:'');
 await shot(k,`<div class="veil"></div><div class="box">${inner}</div>`);}
for(const [k,o] of Object.entries(S.nomes))
 await shot(k,`<div class="nome"><div class="n">${o.nome}</div><div class="s2">${o.sub}</div></div>`);
if(0)for(const [i,L] of Object.entries(S.leg)) for(let j=0;j<L.length;j++)
 await shot(`c${i}_${String(j).padStart(2,'0')}`,`<div class="cap">${kw(L[j][2])}</div>`);
await shot('end',`<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%, #243656 0%, #0F1B33 50%, #0A1222 100%)"></div>
 <div style="position:absolute;left:0;right:0;top:430px;display:flex;flex-direction:column;align-items:center;text-align:center">
 <img src="conecta-simbolo.png" style="height:220px;margin-bottom:52px"><img src="conecta-wordmark-branco.png" style="height:52px;margin-bottom:24px">
 <div style="height:110px"></div>
 <h1 style="font-size:78px">Pessoas que fortalecem pessoas.<br>Negócios que crescem<br><b>juntos</b></h1>
 <div class="line" style="margin:50px auto 0"></div><div class="sub" style="margin-top:46px;letter-spacing:.08em">@conecta.acigra</div></div>`,false);
await b.close();})();
