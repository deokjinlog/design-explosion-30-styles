#!/usr/bin/env python3
"""화면 원형 적합성 린터 — "이 시안이 이 도메인의 화면이 맞나"를 기계로 검사.

style-lint.py 와 **직교**한다:
  - style-lint.py  : 이 시안이 그 *스타일*의 금지를 지켰나 (라운드·그림자·그라디언트…)
  - archetype-lint : 이 시안이 그 *도메인의 원형*에 맞나 (대화형에 KPI·도넛이 박혔나)

이게 없어서 실제 사고가 났다 — 문학 스토리 서비스(대화형)에 대시보드 원형을 이식해
"들은 스토리 1,284,000편 / 목표 달성률 65% / 축 구성비 도넛"이 30개 시안 전부에 들어갔고,
style-lint 는 30/30 PASS 를 냈다. 스타일 규칙은 다 지켰지만 **질문 자체가 틀린 갤러리**였다.

검사 모드 2가지:
  ① 속성 모드 (결정론, 권장) — HTML 에 data-region="…" 이 있으면 그걸로 검사.
     references/archetypes.md 의 "표준 data-region 어휘" 참조.
  ② 키워드 모드 (폴백, 부정확) — data-region 이 하나도 없으면 키워드로 추측.
  ※ 금지 요소는 두 모드 모두에서 항상 키워드로도 본다 (속성 없이 몰래 박힌 것 적발).

사용법:
  python3 archetype-lint.py <디렉토리>              # 폴더의 _spec.json 에서 원형을 읽음
  python3 archetype-lint.py <디렉토리> --archetype B
  python3 archetype-lint.py <파일.html> --archetype C

_spec.json (단일 화면):  {"archetype": "B", "domain": "연서", "note": "대화형(주)+읽기형(보조)"}

_spec.json (화면 세트 — 화면마다 원형이 다름):
  {"archetype": "D", "domain": "호텔 예약",
   "screens": {"screen-1-search": "D", "screen-2-booking": "E", "screen-3-mybookings": "K"}}
  → screens 키가 파일명에 포함되면 그 원형으로 검사. 없으면 archetype 기본값.

한계: 키워드 모드는 오탐이 가능하다. FAIL 은 실제 위반인지 확인 후 수정한다.
종료코드: FAIL 있으면 1, 없으면 0.
"""
import re, sys, os, glob, json

ARCHETYPE_NAME = {
    "A": "대시보드형", "B": "대화형", "C": "읽기형", "D": "컬렉션형",
    "E": "폼·입력형", "F": "피드형", "G": "에디터·캔버스형", "H": "검색·결과형",
    "I": "온보딩형", "J": "인증형", "K": "프로필·설정형",
}

# 원형별 필수/금지 region (references/archetypes.md 와 일치해야 함)
RULES = {
    "A": {"required": ["kpi", "chart-trend", "table"], "forbidden": []},
    "B": {"required": ["conversation", "composer"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal"]},
    "C": {"required": ["story-body", "meta"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal"]},
    "D": {"required": ["collection", "item-card", "filter"], "forbidden": ["kpi", "chart-part", "goal"]},
    "E": {"required": ["form"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal"]},
    "F": {"required": ["feed", "feed-item"], "forbidden": ["kpi", "chart-part", "goal"]},
    "G": {"required": ["canvas", "toolbar"], "forbidden": ["kpi", "chart-part", "goal"]},
    "H": {"required": ["search", "results"], "forbidden": ["kpi", "chart-part", "goal"]},
    "I": {"required": ["slides", "progress"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal", "table"]},
    "J": {"required": ["auth-form", "brand"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal", "table"]},
    "K": {"required": ["settings-list"], "forbidden": ["kpi", "chart-trend", "chart-part", "goal"]},
}

REGION_LABEL = {
    "kpi": "KPI 지표 카드", "chart-trend": "추이 차트/스파크라인", "chart-part": "구성비(도넛/파이) 차트",
    "goal": "목표 진행률/달성률", "table": "데이터 표",
    "conversation": "대화 흐름", "composer": "입력창", "response-card": "응답 카드",
    "story-body": "본문(긴 글)", "meta": "출처·저자", "excerpt": "인용/발췌",
    "collection": "아이템 목록/그리드", "item-card": "아이템 카드", "filter": "필터/탭",
    "form": "입력 폼", "steps": "단계 표시",
    "feed": "피드", "feed-item": "피드 항목",
    "canvas": "편집 캔버스", "toolbar": "툴바",
    "search": "검색 입력", "results": "결과 목록",
    "slides": "온보딩 슬라이드", "progress": "진행 표시",
    "auth-form": "인증 폼", "brand": "로고/브랜드",
    "settings-list": "설정 목록", "profile": "프로필 헤더",
}

# 키워드 감지기 — 금지 검사는 항상, 필수 검사는 속성이 없을 때만 사용
KEYWORDS = {
    "kpi": r"\bKPI\b|kpi-|전주 대비|전월 대비|전일 대비|지난주보다",
    "chart-part": r"도넛|구성비|conic-gradient|stroke-dasharray",
    "goal": r"달성률|목표 진행|진행률|goal-(bar|ring|pct)",
    "chart-trend": r"추이|line-chart|linechart|area-fill|스파크라인|sparkline",
    "table": r"<table\b|<tbody\b",
    "conversation": r"말풍선|bubble|chat-|-chat|대화|발화|speaker",
    "composer": r"<textarea\b|보내기|입력창|composer",
    "meta": r"작가|저자|출처",
    "collection": r"grid-template-columns|썸네일|thumb|card-grid",
    "item-card": r"카드|card",
    "filter": r"필터|filter|칩|chip",
    "form": r"<input\b|<select\b|<textarea\b",
    "feed": r"분 전|시간 전|방금|일 전",
    "feed-item": r"분 전|시간 전|방금|일 전",
    "canvas": r"캔버스|canvas",
    "toolbar": r"툴바|toolbar|tool-",
    "search": r"검색|search",
    "results": r"결과|result",
    "slides": r"슬라이드|slide|온보딩|튜토리얼|tutorial",
    "progress": r"진행|progress",
    "auth-form": r"로그인|비밀번호|password|회원가입|sign ?in|sign ?up",
    "brand": r"로고|logo|brand",
    "settings-list": r"설정|setting|토글|toggle",
}


def _strip_noise(html):
    """주석·script 를 지운다 — 설계 주석에 'KPI' 라 써서 자기가 걸리는 오탐 방지."""
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    return html


def _kw(html, key):
    pat = KEYWORDS.get(key)
    return bool(pat) and re.search(pat, html, re.I | re.S) is not None


def _longest_paragraph(html):
    best = 0
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", html, re.I | re.S):
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
        best = max(best, len(txt))
    return best


def regions_of(html):
    return set(re.findall(r'data-region\s*=\s*["\']([^"\']+)["\']', html, re.I))


def load_spec(path):
    """_spec.json 로드. 단일 화면이면 {"archetype":"D"}, 화면 세트면 screens 맵도 함께.

    화면 세트 예:
      {"archetype": "D", "domain": "호텔 예약",
       "screens": {"screen-1-search": "D", "screen-2-booking": "E", "screen-3-mybookings": "K"}}
    screens 키는 파일명에 포함되면 매칭된다 (부분 일치, 긴 키 우선).
    """
    d = path if os.path.isdir(path) else os.path.dirname(path)
    p = os.path.join(d, "_spec.json")
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def archetype_for(filepath, spec, override=None):
    """이 파일에 적용할 원형. override > screens 매칭 > 폴더 기본값."""
    if override:
        return override
    name = os.path.basename(str(filepath))
    screens = spec.get("screens") or {}
    # 긴 키부터 매칭 (screen-1 보다 screen-10 우선)
    for key in sorted(screens, key=len, reverse=True):
        if key in name:
            return str(screens[key]).upper()
    a = spec.get("archetype")
    return str(a).upper() if a else None


def lint(path, code):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    html = _strip_noise(raw)
    regions = regions_of(html)
    attr_mode = bool(regions)
    rule = RULES[code]
    fails, warns = [], []

    # 금지 — 속성 + 키워드 둘 다 (속성 없이 몰래 박힌 것도 잡는다)
    for key in rule["forbidden"]:
        label = REGION_LABEL.get(key, key)
        if key in regions:
            fails.append(f"{label} — {ARCHETYPE_NAME[code]}에 없어야 할 영역 (data-region=\"{key}\")")
        elif _kw(html, key):
            fails.append(f"{label} — {ARCHETYPE_NAME[code]}에 없어야 할 요소 (다른 원형에서 이식됨)")

    # 필수 — 속성 모드에선 부재도 FAIL(결정론), 키워드 폴백에선 WARN(퍼지)
    #   금지 침입("대화형에 KPI")뿐 아니라 필수 부재("폼인데 피드라 우김")도 잡아야
    #   게이트가 원형을 진짜 구분한다.
    for key in rule["required"]:
        label = REGION_LABEL.get(key, key)
        if attr_mode:
            ok = key in regions
        elif key == "story-body":
            ok = _longest_paragraph(html) >= 200
        else:
            ok = _kw(html, key)
        if not ok:
            if attr_mode:
                fails.append(f"{label} 없음 — {ARCHETYPE_NAME[code]}의 필수 영역 (data-region=\"{key}\" 누락)")
            else:
                warns.append(f"{label} 없음 — {ARCHETYPE_NAME[code]}의 필수 영역")

    mode = "속성" if attr_mode else "키워드추측"
    tag = "FAIL" if fails else "PASS"
    print(f"[{tag}] {os.path.basename(path)}  (원형 {code} · {ARCHETYPE_NAME[code]} · {mode} 모드)")
    for f in fails:
        print(f"    ✗ {f}")
    for w in warns:
        print(f"    ⚠ {w}")
    return len(fails), attr_mode


def main(argv):
    code, args = None, []
    it = iter(argv)
    for a in it:
        if a == "--archetype":
            code = (next(it, "") or "").upper()
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 0
    spec = load_spec(args[0])
    targets = []
    for a in args:
        if os.path.isdir(a):
            targets += [f for f in sorted(glob.glob(os.path.join(a, "*.html")))
                        if os.path.basename(f) not in ("index.html", "gallery.html")]
        else:
            targets.append(a)
    if not targets:
        # style-lint 와 같은 규율: 검사 0건은 통과가 아니다. 조용히 exit 0 을 내면
        # 게이트가 있다는 착각만 남는다.
        print("검사할 *.html 없음 → ❌ 게이트 무효. '통과' 로 세지 마세요.")
        return 1
    # 화면 세트면 파일마다 원형이 다를 수 있다
    resolved = [(t, archetype_for(t, spec, code)) for t in targets]
    unknown = [t for t, c in resolved if c not in RULES]
    if unknown and len(unknown) == len(resolved):
        print(f"[SKIP] 원형을 알 수 없음 — 폴더에 _spec.json 을 두거나 --archetype A~K 를 지정하세요.")
        print("       " + " · ".join(f"{k}={v}" for k, v in ARCHETYPE_NAME.items()))
        print("검사 0건 → ❌ 게이트 무효. '통과' 로 세지 마세요.")
        return 1
    if spec.get("screens"):
        print(f"ℹ️ 화면 세트 모드 — 화면마다 원형을 따로 검사합니다 ({len(spec['screens'])}개 정의)\n")
    total, legacy = 0, 0
    for t, c in resolved:
        if c not in RULES:
            print(f"[SKIP] {os.path.basename(t)} — 원형 미지정")
            continue
        n, attr = lint(t, c)
        total += n
        legacy += 0 if attr else 1
    if legacy:
        print(f"\nℹ️ {legacy}개 파일이 data-region 없이 키워드추측으로 검사됐습니다 (부정확). "
              f"생성 시 의미 영역에 data-region 을 박으면 결정론적으로 검사됩니다.")
    print(f"\n원형 위반: {total}건 " + (
        "→ 콘텐츠 스펙이 원형과 어긋납니다. 1단계로 돌아가 스펙을 고치세요 (시안만 고치면 재발합니다)"
        if total else "→ 통과 ✅"))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
