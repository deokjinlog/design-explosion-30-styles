#!/usr/bin/env python3
"""화면 원형 적합성 린터 — "이 시안이 이 도메인의 화면이 맞나"를 기계로 검사.

style-lint.py 와 **직교**한다:
  - style-lint.py  : 이 시안이 그 *스타일*의 금지를 지켰나 (라운드·그림자·그라디언트…)
  - archetype-lint : 이 시안이 그 *도메인의 원형*에 맞나 (대화형에 KPI·도넛이 박혔나)

이게 없어서 실제 사고가 났다 — 문학 스토리 서비스(대화형)에 대시보드 원형을 이식해
"들은 스토리 1,284,000편 / 목표 달성률 65% / 축 구성비 도넛"이 30개 시안 전부에 들어갔고,
style-lint 는 30/30 PASS 를 냈다. 스타일 규칙은 다 지켰지만 **질문 자체가 틀린 갤러리**였다.

사용법:
  python3 archetype-lint.py <디렉토리>            # 같은 폴더의 _spec.json 에서 원형을 읽음
  python3 archetype-lint.py <디렉토리> --archetype B
  python3 archetype-lint.py <파일.html> --archetype C

_spec.json 형식 (1단계에서 확정한 콘텐츠 스펙과 함께 저장):
  {"archetype": "B", "domain": "연서", "note": "대화형(주) + 읽기형(보조)"}

한계: 정규식 휴리스틱이라 오탐이 가능하다. FAIL 은 실제 위반인지 확인 후 수정한다.
종료코드: FAIL 있으면 1, 없으면 0.
"""
import re, sys, os, glob, json

ARCHETYPE_NAME = {
    "A": "대시보드형", "B": "대화형", "C": "읽기형", "D": "컬렉션형",
    "E": "폼·마법사형", "F": "피드형", "G": "에디터·캔버스형", "H": "검색·결과형",
}


def _has(s, pat):
    return re.search(pat, s, re.I | re.S) is not None


def _longest_paragraph(s):
    """가장 긴 <p> 의 순수 텍스트 길이 — 읽기형의 '본문이 주인공' 신호."""
    best = 0
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", s, re.I | re.S):
        txt = re.sub(r"<[^>]+>", "", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        best = max(best, len(txt))
    return best


# 신호 감지기 — (이름, 설명, 감지 함수)
SIGNALS = {
    "kpi": ("KPI 지표 카드", lambda s: _has(s, r"\bKPI\b|kpi-|전주 대비|전월 대비|전일 대비|지난주보다")),
    "donut": ("도넛/구성비 차트", lambda s: _has(s, r"도넛|구성비|conic-gradient|stroke-dasharray")),
    "goal": ("목표 진행률/달성률", lambda s: _has(s, r"달성률|목표 진행|진행률|goal-(bar|ring|pct)")),
    "spark": ("스파크라인", lambda s: _has(s, r"스파크라인|sparkline")),
    "trend": ("시간 추이 차트", lambda s: _has(s, r"추이|line-chart|area-fill|linechart")),
    "chat": ("대화/말풍선", lambda s: _has(s, r"말풍선|bubble|chat-|-chat|대화 기록|발화|speaker")),
    "body": ("긴 본문(200자+)", lambda s: _longest_paragraph(s) >= 200),
    "quote": ("인용/발췌", lambda s: _has(s, r"<blockquote|인용|발췌")),
    "grid": ("카드 그리드", lambda s: _has(s, r"grid-template-columns|card-grid|썸네일|thumb")),
    "form": ("입력 폼", lambda s: _has(s, r"<input\b|<textarea\b|<select\b")),
    "steps": ("단계 표시", lambda s: _has(s, r"단계|스텝|step-")),
    "feedtime": ("피드 시간 표기", lambda s: _has(s, r"분 전|시간 전|방금|일 전")),
    "toolbar": ("툴바/도구", lambda s: _has(s, r"툴바|toolbar|tool-")),
    "searchbar": ("검색 입력", lambda s: _has(s, r"검색|search")),
    "highlight": ("검색어 하이라이트", lambda s: _has(s, r"<mark\b|하이라이트|highlight")),
}

# 원형별 규칙 — required(없으면 WARN) / forbidden(있으면 FAIL, 이식된 남의 장기)
RULES = {
    "A": {"required": ["kpi", "trend"], "forbidden": []},
    "B": {"required": ["chat"], "forbidden": ["kpi", "donut", "goal", "spark"]},
    "C": {"required": ["body"], "forbidden": ["kpi", "donut", "goal", "spark"]},
    "D": {"required": ["grid"], "forbidden": ["kpi", "donut", "goal"]},
    "E": {"required": ["form", "steps"], "forbidden": ["kpi", "donut", "goal", "trend"]},
    "F": {"required": ["feedtime"], "forbidden": ["kpi", "donut", "goal"]},
    "G": {"required": ["toolbar"], "forbidden": ["kpi", "donut", "goal"]},
    "H": {"required": ["searchbar", "highlight"], "forbidden": ["kpi", "donut", "goal"]},
}


def load_archetype(path):
    """디렉토리(또는 파일이 속한 디렉토리)의 _spec.json 에서 원형 코드를 읽는다."""
    d = path if os.path.isdir(path) else os.path.dirname(path)
    p = os.path.join(d, "_spec.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8")).get("archetype")
    except (ValueError, OSError):
        return None


def lint(path, code):
    html = open(path, encoding="utf-8", errors="ignore").read()
    rule = RULES[code]
    fails, warns = [], []
    for key in rule["forbidden"]:
        label, fn = SIGNALS[key]
        if fn(html):
            fails.append(f"{label} — {ARCHETYPE_NAME[code]}에 없어야 할 요소 (다른 원형에서 이식됨)")
    for key in rule["required"]:
        label, fn = SIGNALS[key]
        if not fn(html):
            warns.append(f"{label} 없음 — {ARCHETYPE_NAME[code]}의 필수 신호")
    tag = "FAIL" if fails else "PASS"
    print(f"[{tag}] {os.path.basename(path)}  (원형 {code} · {ARCHETYPE_NAME[code]})")
    for f in fails:
        print(f"    ✗ {f}")
    for w in warns:
        print(f"    ⚠ {w}")
    return len(fails)


def main(argv):
    code = None
    args = []
    it = iter(argv)
    for a in it:
        if a == "--archetype":
            code = (next(it, "") or "").upper()
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 0
    target = args[0]
    code = code or load_archetype(target)
    if code not in RULES:
        print(f"[SKIP] 원형을 알 수 없음 — {target} 폴더에 _spec.json 을 두거나 --archetype A~H 를 지정하세요.")
        print(f"       사용 가능: " + " · ".join(f"{k}={v}" for k, v in ARCHETYPE_NAME.items()))
        return 0
    targets = []
    for a in args:
        if os.path.isdir(a):
            targets += [f for f in sorted(glob.glob(os.path.join(a, "*.html")))
                        if os.path.basename(f) not in ("index.html", "gallery.html")]
        else:
            targets.append(a)
    if not targets:
        print("검사할 *.html 없음")
        return 0
    total = sum(lint(t, code) for t in targets)
    print(f"\n원형 위반: {total}건 " + (
        "→ 콘텐츠 스펙이 원형과 어긋납니다. 1단계로 돌아가 스펙을 고치세요 (시안만 고치면 재발합니다)"
        if total else "→ 통과 ✅"))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
