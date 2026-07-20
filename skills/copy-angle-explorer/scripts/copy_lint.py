#!/usr/bin/env python3
"""copy-explosion 카피 린터 — 크리틱 루프의 기계화 (design-explosion style-lint.py 미러).

각도별 히어로 시안(angle-NN-*.html)이 히어로 제약과 진실성 규율을 지키는지
결정론적으로 검사한다. 하이브리드: 기계적 FAIL(히어로 제약 + 정량 클레임) +
[MANUAL] 판정(미묘 진실성·각도 구별성 → 판정 서브에이전트).

사용법:
  python3 copy_lint.py <html 또는 디렉토리>   # 같은 폴더의 spec.json 을 화이트리스트로 사용
종료코드: FAIL 있으면 1, 없으면 0.
"""
import re
import json, os, sys, glob

HEADLINE_MAX = 60
SUB_MAX = 140


def _text(html, cls):
    m = re.search(r'class="' + cls + r'"[^>]*>(.*?)<', html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def extract_hero(html):
    return {
        "headline": _text(html, "cx-headline"),
        "sub": _text(html, "cx-sub"),
        "ctas": re.findall(r'class="cx-cta"', html),
    }


def hero_violations(hero):
    v = []
    if len(hero["headline"]) > HEADLINE_MAX:
        v.append(f"헤드라인 {len(hero['headline'])}자 (상한 {HEADLINE_MAX})")
    if len(hero["sub"]) > SUB_MAX:
        v.append(f"서브 {len(hero['sub'])}자 (상한 {SUB_MAX})")
    if len(hero["ctas"]) != 1:
        v.append(f"CTA {len(hero['ctas'])}개 (정확히 1개여야 함)")
    return v


# 정량 클레임 — 지어내면 가장 위험한 형태 (없는 숫자·수상·고객사)
SUPERLATIVES = ["1위", "1등", "최초", "유일", "최고", "넘버원", "업계 최고", "세계 최초"]


def claim_violations(text, facts):
    """text 의 정량 표현이 facts 화이트리스트에 근거하지 않으면 위반.
    숫자·% ·수상어 = FAIL (지어내면 사고), 라틴 고유명사 = WARN (오탐 여지)."""
    # ⚠️ RISK(side-effect): 정량 추출은 휴리스틱 — 한글 수사("1만")·복합 고유명사는 미탐 가능,
    #    라틴 고유명사는 오탐 가능. 위험한 미탐은 판정 서브에이전트 2차 필터로 보완. — by copy-lint 진실성 게이트
    hay = " ".join(facts)
    fails, warns = [], []
    for num in re.findall(r"\d[\d,]*%?", text):
        if num.replace(",", "") not in hay.replace(",", ""):
            fails.append(f"근거 없는 수치 '{num}' (제품 스펙에 없음)")
    for sup in SUPERLATIVES:
        if sup in text and sup not in hay:
            fails.append(f"근거 없는 수상/최상급 '{sup}' (제품 스펙에 없음)")
    for prop in re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", text):
        if prop not in hay:
            warns.append(f"고유명사 '{prop}' 확인 필요 (오탐 가능)")
    return fails, warns


def load_spec(dirpath):
    p = os.path.join(str(dirpath), "spec.json")
    if not os.path.exists(p):
        return {"facts": [], "language": "ko"}
    d = json.load(open(p, encoding="utf-8"))
    d.setdefault("facts", [])
    d.setdefault("language", "ko")
    return d


def lint(path, spec):
    html = open(path, encoding="utf-8", errors="ignore").read()
    hero = extract_hero(html)
    fails = list(hero_violations(hero))
    copy_text = hero["headline"] + " " + hero["sub"] + " " + " ".join(
        re.findall(r'class="cx-cta"[^>]*>(.*?)<', html, re.S))
    cf, cw = claim_violations(copy_text, spec["facts"])
    fails += cf
    name = os.path.basename(str(path))
    tag = "FAIL" if fails else "PASS"
    print(f"[{tag}] {name}")
    for f in fails:
        print(f"    ✗ {f}")
    for w in cw:
        print(f"    ⚠ {w}")
    print("    [MANUAL] 각도 구별성 · 미묘한 진실성(과장·함의) → 판정 서브에이전트 확인")
    return fails, cw


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    targets = []
    for a in argv:
        if os.path.isdir(a):
            targets += [f for f in sorted(glob.glob(os.path.join(a, "*.html")))
                        if os.path.basename(f) != "gallery.html"]
        else:
            targets.append(a)
    total = 0
    for t in targets:
        spec = load_spec(os.path.dirname(t))
        fails, _ = lint(t, spec)
        total += len(fails)
    print(f"\n총 위반: {total}건 " + ("→ 수정 후 재린트" if total else "→ 통과 ✅"))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
