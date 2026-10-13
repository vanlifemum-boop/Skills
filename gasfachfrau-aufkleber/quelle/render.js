const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch();
  const dir = __dirname;
  for (const f of process.argv.slice(2)) {
    const [w, h] = fs.readFileSync(path.join(dir, f + '.size'), 'utf8').split(' ').map(Number);
    const p = await b.newPage({ viewport: { width: Math.ceil(w * 3.7796), height: Math.ceil(h * 3.7796) }, deviceScaleFactor: 6 });
    await p.goto('file://' + path.join(dir, f + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(dir, f + '.png'), omitBackground: true });
    await p.pdf({ path: path.join(dir, f + '.pdf'), width: w + 'mm', height: h + 'mm', printBackground: true });
    await p.close();
  }
  await b.close();
})();
