// poster.svg를 미리보기 PNG와 A3 PDF로 렌더링
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [svgPath, pngPath, pdfPath, scale] = process.argv.slice(2);
  const svg = fs.readFileSync(svgPath, 'utf8');
  const html = `<!doctype html><html><head><style>@page{size:297mm 420mm;margin:0}html,body{margin:0}svg{display:block;width:297mm;height:420mm}</style></head><body>${svg}</body></html>`;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1188, height: 1680 }, deviceScaleFactor: Number(scale || 1) });
  await p.setContent(html);
  await p.waitForTimeout(300);
  const el = await p.$('svg');
  await el.screenshot({ path: pngPath });
  if (pdfPath && pdfPath !== '-') await p.pdf({ path: pdfPath, width: '297mm', height: '420mm', printBackground: true });
  await b.close();
})();
