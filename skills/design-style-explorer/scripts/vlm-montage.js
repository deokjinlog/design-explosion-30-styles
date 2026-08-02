// ③ VLM 심판용 콘택트시트 — 갤러리 30장을 한 장의 그리드 PNG로.
// 이 PNG를 비전 모델(VLM)에게 주고 루브릭으로 판정: 변별력·깨짐·스타일 충실도.
// (규칙 게이트 visual-gate.js가 못 보는 "전체적 품질/다 비슷"을 잡는 층.)
//
// 설치: npm i playwright && npx playwright install chromium (repo 밖)
// 실행: node vlm-montage.js <gallery-dir> <out.png>
//
// VLM 루브릭(판정 기준 — 근거에 접지):
//  ① 변별력: 서로 구별되나, 똑같아 보이나? (프로젝트 목표: 30개가 갈려야)
//  ② 깨짐: 백지·잘림·겹침·오버플로? (WCAG·UX)
//  ③ 충실도: 이 사조처럼 보이나? (docs/design/2026-07-26-type-and-source-grounding.md 시그니처 표)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const dir = process.argv[2], out = process.argv[3] || 'montage.png';
if (!dir) { console.error('usage: node vlm-montage.js <gallery-dir> <out.png>'); process.exit(1); }
const files = fs.readdirSync(dir).filter(f => /^style-\d+\.html$/.test(f)).sort();

(async () => {
  const cellDir = path.join(path.dirname(out), 'cells');
  fs.mkdirSync(cellDir, { recursive: true });
  const b = await chromium.launch({ headless: true });
  const p = await b.newPage({ viewport: { width: 1400, height: 820 } });
  const figs = [];
  for (const f of files) {                                  // 각 스타일을 개별 페이지로 완전 로드 후 상단 클립
    const nn = f.match(/\d+/)[0];
    await p.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' });
    await p.waitForTimeout(800);
    const png = path.join(cellDir, `s-${nn}.png`);
    await p.screenshot({ path: png, clip: { x: 0, y: 0, width: 1400, height: 820 } });
    figs.push(`<figure><img src="cells/s-${nn}.png"><figcaption>${nn}</figcaption></figure>`);
  }
  // 콘택트시트를 실제 파일로 써서 file:// 이미지가 로드되게(setContent는 about:blank라 차단됨)
  const sheet = path.join(path.dirname(out), '_contact.html');
  fs.writeFileSync(sheet, `<!doctype html><meta charset=utf-8><style>
    body{margin:0;background:#0d1117;font-family:sans-serif}
    .g{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:6px}
    figure{margin:0}img{width:100%;display:block;border:1px solid #30363d}
    figcaption{color:#e6edf3;font-size:16px;padding:3px 2px 8px}
    </style><div class=g>${figs.join('')}</div>`);
  const p2 = await b.newPage({ viewport: { width: 1560, height: 1000 } });
  await p2.goto('file://' + path.resolve(sheet), { waitUntil: 'networkidle' });
  await p2.waitForTimeout(600);
  await p2.screenshot({ path: out, fullPage: true });
  console.log('montage saved:', out, `(${files.length} styles)`);
  await b.close();
})();
