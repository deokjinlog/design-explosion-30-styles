#!/usr/bin/env python3
"""selector-coverage lint — Zen Garden 방식의 게이트 (archetype-lint 후계자).

CSS가 저지를 수 있는 나쁜 짓은 딱 둘이고, 이 린트가 그 전 집합을 덮는다:
  ① 환각 셀렉터 — 스켈레톤에 없는 요소를 스타일 (조용히 무시됨)
  ② 누락 영역   — data-region 중 규칙이 하나도 안 걸린 것 (맨몸으로 렌더)

usage: python3 coverage-lint.py <skeleton.html> <style.css>
"""
import re, sys

skel = open(sys.argv[1], encoding="utf-8").read()
css_raw = open(sys.argv[2], encoding="utf-8").read()

# ---------- 스켈레톤에 실재하는 것들 ----------
skel_classes = set()
for m in re.finditer(r'class="([^"]*)"', skel):
    skel_classes.update(m.group(1).split())
skel_ids   = set(re.findall(r'\bid="([^"]+)"', skel))
skel_tags  = set(t.lower() for t in re.findall(r'<([a-zA-Z][\w-]*)', skel))
skel_attrs = set(re.findall(r'[\s"]([a-zA-Z][a-zA-Z0-9-]*)=', skel))
skel_attr_vals = set((m.group(1), m.group(2)) for m in re.finditer(r'([a-zA-Z][\w-]*)="([^"]*)"', skel))
regions = re.findall(r'data-region="([^"]+)"', skel)

# region -> 그 요소의 클래스 집합
region_el_classes = {}
for r in set(regions):
    m = re.search(r'<[^>]*\bdata-region="' + re.escape(r) + r'"[^>]*>', skel)
    cm = re.search(r'class="([^"]*)"', m.group(0)) if m else None
    region_el_classes[r] = set(cm.group(1).split()) if cm else set()

# ---------- CSS 파싱 ----------
css = re.sub(r'/\*.*?\*/', ' ', css_raw, flags=re.S)          # 주석 제거
heads = re.findall(r'([^{}]+)\{', css)                          # "셀렉터 {" 의 앞부분

ALWAYS_OK_TAGS = {"html", "body", "from", "to"}
css_used_classes = set()

def css_unescape(s):
    """CSS 유니코드 이스케이프(\\XXXX 또는 \\XXXX+공백)를 실제 문자로."""
    return re.sub(r'\\([0-9A-Fa-f]{1,6})\s?', lambda m: chr(int(m.group(1), 16)), s)

def atom_check(sel):
    """한 콤마-단위 셀렉터에서 (환각목록) 반환. 부수효과로 css_used_classes 채움."""
    bad = []
    for x in re.findall(r'\.([A-Za-z_][\w-]*)', sel):
        css_used_classes.add(x)
        if x not in skel_classes:
            bad.append(("class", "." + x))
    for x in re.findall(r'#([A-Za-z_][\w-]*)', sel):
        if x not in skel_ids:
            bad.append(("id", "#" + x))
    for an, q, av in re.findall(r'\[([a-zA-Z][\w-]*)(?:[~|^$*]?=("?)([^\]"]*)\2)?\]', sel):
        av = css_unescape(av)
        if an not in skel_attrs:
            bad.append(("attr", "[%s]" % an))
        elif av and (an, av) not in skel_attr_vals:
            bad.append(("attr-val", "[%s=%s]" % (an, av)))
    # 태그: pseudo/attr/class/id/combinator 제거 후 남는 단어
    tmp = re.sub(r'\[[^\]]*\]', ' ', sel)
    tmp = re.sub(r'::?[A-Za-z-]+(\([^)]*\))?', ' ', tmp)
    tmp = re.sub(r'[.#][\w-]+', ' ', tmp)
    tmp = re.sub(r'[>+~*]', ' ', tmp)
    for t in re.findall(r'[A-Za-z][\w-]*', tmp):
        t = t.lower()
        if t in ALWAYS_OK_TAGS:
            continue
        if t not in skel_tags:
            bad.append(("tag", t))
    return bad

hallucinated = []   # (셀렉터, 종류, 원자)
for h in heads:
    h = h.strip()
    if not h or h.startswith('@'):
        continue
    if re.fullmatch(r'(\d+%|from|to)(\s*,\s*(\d+%|from|to))*', h):
        continue
    for part in h.split(','):
        part = part.strip()
        if not part or part == ':root' or part == '*':
            # :root / * 는 원자 없음
            atom_check(part)
            continue
        for kind, atom in atom_check(part):
            hallucinated.append((part, kind, atom))

# ---------- ② 누락 영역 ----------
missing_regions = []
for r in set(regions):
    styled = any(c in css_used_classes for c in region_el_classes[r]) \
             or ('data-region="%s"' % r) in css_raw or ("data-region='%s'" % r) in css_raw
    if not styled:
        missing_regions.append((r, sorted(region_el_classes[r])))

# ---------- 판정 ----------
print("=" * 60)
print("selector-coverage lint")
print(f"  스켈레톤: 클래스 {len(skel_classes)} · region {len(set(regions))} · 태그 {len(skel_tags)}")
print(f"  CSS: 사용 클래스 {len(css_used_classes)}")
print("=" * 60)

if hallucinated:
    print(f"\n[①] 환각 셀렉터 {len(hallucinated)}건 — 스켈레톤에 없는 걸 스타일:")
    for sel, kind, atom in hallucinated[:40]:
        print(f"    ✗ {atom:22} ({kind})   ← \"{sel[:60]}\"")
else:
    print("\n[①] 환각 셀렉터 0건 ✅ — 모든 셀렉터가 실재 요소를 타겟팅")

if missing_regions:
    print(f"\n[②] 누락 영역 {len(missing_regions)}건 — 규칙이 안 걸린 data-region:")
    for r, cls in missing_regions:
        print(f"    ✗ {r:16} (class={cls})  ← 맨몸 렌더")
else:
    print("[②] 누락 영역 0건 ✅ — 모든 region이 최소 1개 규칙에 잡힘")

ok = not hallucinated and not missing_regions
print("\n" + ("PASS ✅ — 남의 DOM에 안전하게 스타일" if ok else "FAIL ❌"))
sys.exit(0 if ok else 1)
