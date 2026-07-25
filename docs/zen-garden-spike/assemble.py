#!/usr/bin/env python3
"""assemble.py — 3층 조립기. 스켈레톤 + CSS층들 → 자립 HTML.

스켈레톤의 body(DOM)는 그대로 두고, base+tokens+signature 를 <style> 로 인라인한다.
→ 스타일이 뭐든 body 는 문자 그대로 동일(Zen Garden 보장), CSS만 다름.
→ GitHub Pages·iframe 갤러리에 그대로 쓸 자립 파일.

usage: python3 assemble.py <skeleton.html> <out.html> <css1> [css2 ...]
       (css 순서 = base → tokens → signature)
"""
import sys, re

skeleton = open(sys.argv[1], encoding="utf-8").read()
out_path  = sys.argv[2]
css_paths = sys.argv[3:]

combined = "\n\n".join(f"/* ==== {p.split('/')[-1]} ==== */\n" + open(p, encoding="utf-8").read()
                       for p in css_paths)

# 스켈레톤의 외부 3층 <link> 는 제거(인라인으로 대체)
html = re.sub(r'\s*<link rel="stylesheet"[^>]*>', '', skeleton)
# <style> 로 head 끝에 주입
html = html.replace('</head>', f'<style>\n{combined}\n</style>\n</head>')

open(out_path, "w", encoding="utf-8").write(html)
print(f"조립: {out_path} ({len(html)} bytes) ← {len(css_paths)}개 CSS 인라인")
