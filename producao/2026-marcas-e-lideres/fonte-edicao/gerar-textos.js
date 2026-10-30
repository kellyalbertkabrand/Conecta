const { chromium } = require('playwright');
const path = require('path');
const dir = process.argv[2];
const kw = s => s.replace(/"([^"]+)"/g, '<b>$1</b>').replace(/\n/g,'<br>');
const css = `
@font-face{font-family:Sora;src:url(sora-var.woff2) format('woff2');font-weight:100 800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;background:transparent;font-family:Sora}
.veil{position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(180deg,rgba(10,18,34,0) 0%,rgba(10,18,34,.55) 45%,rgba(10,18,34,.92) 100%)}
.topveil{position:absolute;left:0;right:0;top:0;height:260px;background:linear-gradient(180deg,rgba(10,18,34,.55),rgba(10,18,34,0))}
.logo{position:absolute;top:64px;left:72px;display:flex;align-items:center;gap:18px}
.logo img.s{height:58px}.logo img.w{height:26px}
.box{position:absolute;left:72px;right:72px;bottom:120px;color:#fff}
.tag{font-weight:600;font-size:26px;letter-spacing:.24em;color:#00CEC9;text-transform:uppercase;margin-bottom:26px}
h1{font-weight:250;font-size:76px;line-height:1.1;letter-spacing:-.01em}
h1 b{font-weight:800;color:#00CEC9}
.line{width:96px;height:4px;background:#00CEC9;margin-top:34px}
.sub{font-weight:300;font-size:30px;color:#C8D6E5;margin-top:26px}
`;
const ovs = {
  t1:{tag:'Marcas & Líderes · Gravataí 2026', h:'Por trás de cada marca,\numa "história"'},
  t2:{tag:'Reconhecimento', h:'Nucleados do Conecta\nentre as "mais lembradas"'},
  t3:{tag:'Conecta no palco', h:'Cada prêmio,\numa "trajetória"'},
  t4:{tag:'Núcleo de Negócios ACIGRA', h:'Pessoas que fortalecem\n"pessoas"'},
  logo:{only:true},
};
(async()=>{
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1350}});
  for (const [k,o] of Object.entries(ovs)) {
    const body = o.only
      ? `<div class="topveil"></div><div class="logo"><img class="s" src="conecta-simbolo-branco.png"><img class="w" src="conecta-wordmark-branco.png"></div>`
      : `<div class="veil"></div><div class="box"><div class="tag">${o.tag}</div><h1>${kw(o.h)}</h1><div class="line"></div></div>`;
    require('fs').writeFileSync(path.join(dir,'_t.html'),`<html><head><style>${css}</style></head><body>${body}</body></html>`);
    await p.goto('file://'+path.join(dir,'_t.html'),{waitUntil:'load'}); await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:path.join(dir,k+'.png'),omitBackground:true});
  }
  // end card
  const end = `<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%, #243656 0%, #0F1B33 50%, #0A1222 100%)"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff">
   <img src="conecta-simbolo.png" style="height:190px;margin-bottom:46px">
   <img src="conecta-wordmark-branco.png" style="height:46px;margin-bottom:22px">
   <div class="tag" style="margin-bottom:90px;font-size:22px">Núcleo de Negócios ACIGRA</div>
   <h1 style="font-size:72px">Negócios que crescem<br><b>juntos</b></h1>
   <div class="line" style="margin:44px auto 0"></div>
   <div class="sub" style="margin-top:44px;letter-spacing:.08em">@conecta.acigra</div></div>`;
  require('fs').writeFileSync(path.join(dir,'_t.html'),`<html><head><style>${css}</style></head><body>${end}</body></html>`);
  await p.goto('file://'+path.join(dir,'_t.html'),{waitUntil:'load'}); await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:path.join(dir,'end.png')});
  await b.close();
})();
