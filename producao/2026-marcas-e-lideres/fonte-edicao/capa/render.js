const { chromium } = require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(process.argv[2],'capa.html'),{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:path.join(process.argv[2],'capa.png')});await b.close();})();
