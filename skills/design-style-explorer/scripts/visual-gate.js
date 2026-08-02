// 시각 게이트 ① — WCAG AA 대비 + 가로 오버플로. Playwright 헤드리스 크로미움으로 실제 렌더 후 측정.
// coverage-lint(구조 배선)이 못 잡는 "글자 안 읽힘·레이아웃 깨짐"을 결정적으로 잡는다.
//
// 설치(1회, repo 밖 아무 데나): npm i playwright && npx playwright install chromium
// 실행: node visual-gate.js <gallery-dir>
//
// 기준: WCAG 2.x AA — 본문 대비 4.5:1, 큰 글자(≥24px 또는 ≥18.66px bold) 3:1.
// 한계: 그라디언트/이미지 배경 위 글자는 CSS값으론 측정 불가라 스킵(정확히는 실제 픽셀 샘플링 필요 — 후속).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const dir = process.argv[2];
if (!dir) { console.error('usage: node visual-gate.js <gallery-dir>'); process.exit(1); }
const files = fs.readdirSync(dir).filter(f => /^style-\d+\.html$/.test(f)).sort();

const AUDIT = () => {
  // 색 파서: rgb()/rgba() 0-255, color(srgb ..) 0-1 float(color-mix 결과), 알파 포함 → [r,g,b,a]
  const parse = c => {
    if (!c) return null;
    const n = c.match(/[\d.]+/g); if (!n) return null;
    if (c.startsWith('color(')) return [n[0]*255, n[1]*255, n[2]*255, n[3]!==undefined?+n[3]:1];
    return [+n[0], +n[1], +n[2], n[3]!==undefined?+n[3]:1];
  };
  const lum = ([r,g,b]) => { const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)}; return .2126*f(r)+.7152*f(g)+.0722*f(b); };
  const ratio = (a,b) => { const l1=lum(a),l2=lum(b),hi=Math.max(l1,l2),lo=Math.min(l1,l2); return (hi+.05)/(lo+.05); };
  const blend = (fg, bg) => { const a=fg[3]; return [0,1,2].map(i=>fg[i]*a+bg[i]*(1-a)); };  // 반투명 글자를 배경 위에 합성
  // 유효 배경: 그라디언트/이미지면 측정불가(null=스킵), 불투명 색 만나면 그 색, 없으면 흰색
  const bgOf = el => {
    let e = el;
    while (e) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
      const c = parse(cs.backgroundColor);
      if (c && c[3] > .5) return c.slice(0,3);
      e = e.parentElement;
    }
    return [255,255,255];
  };
  const results = [];
  for (const el of document.querySelectorAll('*')) {
    const direct = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim().length>1);
    if (!direct) continue;                                          // 직접 텍스트 있는 요소만
    const cs = getComputedStyle(el), rect = el.getBoundingClientRect();
    if (rect.width<2 || rect.height<2 || cs.visibility==='hidden' || +cs.opacity===0) continue;
    const fgRaw = parse(cs.color); if (!fgRaw) continue;
    const bg = bgOf(el); if (!bg) continue;                        // 그라디언트 배경 = 스킵
    const fg = fgRaw[3] < 1 ? blend(fgRaw, bg) : fgRaw.slice(0,3);
    const r = ratio(fg, bg);
    const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
    const thr = (px >= 24 || (px >= 18.66 && bold)) ? 3.0 : 4.5;   // WCAG AA
    results.push({ r: +r.toFixed(2), thr, tag: el.className || el.tagName, txt: el.textContent.trim().slice(0,24) });
  }
  const fails = results.filter(x => x.r < x.thr).sort((a,b)=>a.r-b.r);
  return { overflow: document.documentElement.scrollWidth > window.innerWidth + 2, worst: fails[0]||null, failN: fails.length };
};

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  console.log(`\n=== ${path.basename(dir)} — WCAG 대비(AA) + 오버플로 ===`);
  let pass=0, fail=0;
  for (const f of files) {
    await page.goto('file://' + path.join(dir, f), { waitUntil: 'networkidle' });
    const a = await page.evaluate(AUDIT);
    const bad = a.overflow || a.failN > 0;
    bad ? fail++ : pass++;
    const flags = [];
    if (a.overflow) flags.push('가로overflow');
    if (a.failN) flags.push(`대비FAIL ${a.failN}건(최저 ${a.worst.r}<${a.worst.thr}, .${a.worst.tag} "${a.worst.txt}")`);
    console.log(`${bad?'✗':'✓'} ${f}  ${flags.join(' · ')||'clean'}`);
  }
  console.log(`\n합계: PASS ${pass} · FLAG ${fail} / ${files.length}`);
  await browser.close();
})();
