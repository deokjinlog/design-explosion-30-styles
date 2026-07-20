---
commit_policy: per-task
---

# copy-explosion (카피 폭발) 구현계획서

> **다음 단계 안내**: 이 계획을 task-by-task 로 실행하려면 `subagent-driven-development` (보조 에이전트 강제 모드, 권장) 또는 `executing-plans` (인라인 모드) 를 사용하세요. 각 step 은 체크박스 (`- [ ]`) 형식이라 진행 상황 추적이 가능합니다.

**Goal:** design-explosion 의 짝 스킬 — 제품 한 줄을 랜딩 히어로 30가지 메시지 각도로 폭발시켜 비교·조합하는 독립 플러그인 `copy-explosion-30-angles` 를 만든다.

**Architecture:** 독립 플러그인 안 스킬 1개(`copy-angle-explorer`). 7스테이지 파이프라인(입력→제품스펙 고정→30각도 병렬생성→카피-린트 게이트→갤러리→퍼널→역추출). 유일한 실행 코드는 하이브리드 린터 `copy-lint.py`; 나머지는 참조 마크다운(master-copy-prompt·30 각도 프롬프트·hero-template·SKILL).

**Tech Stack:** Python 3 (표준 라이브러리만, `re`) + pytest / Markdown 스킬 파일 / 순수 HTML 히어로 템플릿 / Claude Code 플러그인 매니페스트(JSON).

**Spec inputs:**
- copy-explosion-requirements.md — FR-1~17, NFR-1(진실성)·NFR-2(6패밀리)·NFR-3(자기완결), AC-1~10
- copy-explosion-tech-design.md — 결정1(별도 repo)·결정2(하이브리드 린트)·결정3(30파일+master)·결정4(중립 템플릿)·결정5(히어로 상한), §3.4 30각도×6패밀리, §6 위험

---

## 핵심 계약 — copy-lint 가 파싱하는 히어로 마크업 (모든 task 공유)

히어로 템플릿과 린터가 결합되는 지점. 모든 시안 HTML 은 아래 클래스를 쓴다 (hero-template.md 가 강제, copy-lint.py 가 파싱):

- 헤드라인: `<h1 class="cx-headline">…</h1>`
- 서브카피: `<p class="cx-sub">…</p>`
- CTA: `<a class="cx-cta" …>…</a>` (정확히 1개)
- 제품 사실 스펙: 갤러리 출력 폴더의 `spec.json` — `{"facts": ["...", ...], "language": "ko"}`. `facts` 가 copy-lint 진실성 화이트리스트.

히어로 상한 (결정5): 헤드라인 ≤ 60자, 서브 ≤ 140자, CTA 정확히 1개.

---

## 1. 단계별 작업

### Task 1: repo 스캐폴드 + git init

**Files:**
- Create: `copy-explosion-30-angles/.gitignore`
- Create: `copy-explosion-30-angles/LICENSE`
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/prompts/.gitkeep`
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/scripts/.gitkeep`

- [ ] **Step 1: 디렉토리 + 파일 생성**

```bash
cd /home/djchoi/deokjinlog
mkdir -p copy-explosion-30-angles/.claude-plugin
mkdir -p copy-explosion-30-angles/skills/copy-angle-explorer/references/prompts
mkdir -p copy-explosion-30-angles/skills/copy-angle-explorer/scripts
mkdir -p copy-explosion-30-angles/tests
touch copy-explosion-30-angles/skills/copy-angle-explorer/references/prompts/.gitkeep
touch copy-explosion-30-angles/skills/copy-angle-explorer/scripts/.gitkeep
```

- [ ] **Step 2: .gitignore 작성** (new file: `copy-explosion-30-angles/.gitignore`)

```gitignore
__pycache__/
*.pyc
.venv/
.DS_Store
# 시안 출력물은 세션 산출물 — 커밋하지 않음
docs/copy-gallery/
```

- [ ] **Step 3: LICENSE 작성** — design-explosion 의 MIT LICENSE 를 복사하고 연도/저작자만 유지 (new file: `copy-explosion-30-angles/LICENSE`). design-explosion-30-styles/LICENSE 내용을 그대로 사용.

- [ ] **Step 4: git init (로컬 전용 — push 안 함)**

```bash
cd /home/djchoi/deokjinlog/copy-explosion-30-angles && git init && git add -A
```

- [ ] **Step 5: Commit**

```bash
cd /home/djchoi/deokjinlog/copy-explosion-30-angles
git commit -m "chore: scaffold copy-explosion-30-angles repo"
```

---

### Task 2: 플러그인 매니페스트

**Files:**
- Create: `copy-explosion-30-angles/.claude-plugin/plugin.json`
- Create: `copy-explosion-30-angles/.claude-plugin/marketplace.json`
- Test: `copy-explosion-30-angles/tests/test_manifest.py`

**Model**: haiku

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_manifest.py`)

```python
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_plugin_manifest_valid():
    data = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert data["name"] == "copy-explosion-30-angles"
    assert "claude-code-plugin" in data["keywords"]

def test_marketplace_lists_plugin():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    names = [p["name"] for p in data["plugins"]]
    assert "copy-explosion-30-angles" in names
```

- [ ] **Step 2: 실패 확인**

Run: `cd /home/djchoi/deokjinlog/copy-explosion-30-angles && python3 -m pytest tests/test_manifest.py -v`
Expected: FAIL (파일 없음)

- [ ] **Step 3: plugin.json 작성** (new file: `.claude-plugin/plugin.json`)

```json
{
  "name": "copy-explosion-30-angles",
  "description": "제품 한 줄을 랜딩 히어로 30가지 메시지 각도로 폭발시켜 나란히 비교 — 카피 방향을 정하는 메시지 탐색",
  "version": "0.1.0",
  "author": { "name": "djchoi", "email": "deokjinlog@users.noreply.github.com" },
  "homepage": "https://github.com/deokjinlog/copy-explosion-30-angles",
  "repository": "https://github.com/deokjinlog/copy-explosion-30-angles",
  "license": "MIT",
  "keywords": ["copywriting", "landing-page", "hero", "messaging", "marketing", "html", "gallery", "claude-code", "claude-code-plugin"]
}
```

- [ ] **Step 4: marketplace.json 작성** (new file: `.claude-plugin/marketplace.json`)

```json
{
  "name": "copy-explosion-30-angles",
  "description": "제품 한 줄을 랜딩 히어로 30가지 메시지 각도로 폭발시켜 나란히 비교",
  "owner": { "name": "djchoi", "email": "deokjinlog@users.noreply.github.com" },
  "homepage": "https://github.com/deokjinlog/copy-explosion-30-angles",
  "plugins": [
    {
      "name": "copy-explosion-30-angles",
      "description": "제품 한 줄을 랜딩 히어로 30가지 메시지 각도로 폭발시켜 나란히 비교 — 카피 방향을 정하는 메시지 탐색",
      "version": "0.1.0",
      "source": "./",
      "homepage": "https://github.com/deokjinlog/copy-explosion-30-angles",
      "repository": "https://github.com/deokjinlog/copy-explosion-30-angles",
      "author": { "name": "djchoi", "email": "deokjinlog@users.noreply.github.com" }
    }
  ]
}
```

- [ ] **Step 5: 통과 확인 + Commit**

Run: `python3 -m pytest tests/test_manifest.py -v` → Expected: PASS
```bash
git add .claude-plugin tests/test_manifest.py
git commit -m "feat: add plugin + marketplace manifests"
```

---

### Task 3: copy-lint.py — 히어로 추출 + 히어로 제약 검사 (TDD)

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/scripts/copy_lint.py`
- Test: `copy-explosion-30-angles/tests/test_hero_constraints.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_hero_constraints.py`)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def _html(headline, sub, ctas=1):
    cta = '<a class="cx-cta" href="#">시작하기</a>' * ctas
    return f'<h1 class="cx-headline">{headline}</h1><p class="cx-sub">{sub}</p>{cta}'

def test_extract_hero_pulls_headline_sub_and_ctas():
    hero = cl.extract_hero(_html("헤드라인", "서브카피", ctas=1))
    assert hero["headline"] == "헤드라인"
    assert hero["sub"] == "서브카피"
    assert len(hero["ctas"]) == 1

def test_headline_over_limit_is_fail():
    long_headline = "가" * 61
    fails = cl.hero_violations(cl.extract_hero(_html(long_headline, "짧은 서브")))
    assert any("헤드라인" in f for f in fails)

def test_two_ctas_is_fail():
    fails = cl.hero_violations(cl.extract_hero(_html("헤드라인", "서브", ctas=2)))
    assert any("CTA" in f for f in fails)

def test_clean_hero_has_no_violation():
    fails = cl.hero_violations(cl.extract_hero(_html("적당한 헤드라인", "적당한 서브카피")))
    assert fails == []
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest tests/test_hero_constraints.py -v`
Expected: FAIL (`No module named 'copy_lint'`)

- [ ] **Step 3: 최소 구현** (new file: `skills/copy-angle-explorer/scripts/copy_lint.py`)

```python
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
```

- [ ] **Step 4: 통과 확인 + Commit**

Run: `python3 -m pytest tests/test_hero_constraints.py -v` → Expected: PASS
```bash
git add skills/copy-angle-explorer/scripts/copy_lint.py tests/test_hero_constraints.py
git commit -m "feat(lint): hero extraction + constraint checks"
```

---

### Task 4: copy-lint.py — 정량 클레임 추출 + 화이트리스트 검사 (TDD)

**Files:**
- Modify: `copy-explosion-30-angles/skills/copy-angle-explorer/scripts/copy_lint.py`
- Test: `copy-explosion-30-angles/tests/test_claims.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_claims.py`)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def test_number_not_in_whitelist_is_fail():
    fails, warns = cl.claim_violations("가입 고객 10000명 돌파", facts=["무료 체험 제공"])
    assert any("10000" in f for f in fails)

def test_number_in_whitelist_passes():
    fails, warns = cl.claim_violations("가입 고객 10000명 돌파", facts=["가입 고객 10000명"])
    assert fails == []

def test_superlative_not_in_whitelist_is_fail():
    fails, warns = cl.claim_violations("업계 1위 솔루션", facts=["빠른 처리 속도"])
    assert any("1위" in f or "업계" in f for f in fails)

def test_latin_propernoun_is_warn_not_fail():
    fails, warns = cl.claim_violations("Samsung 도 쓰는 도구", facts=["누구나 쓴다"])
    assert fails == []
    assert any("Samsung" in w for w in warns)
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest tests/test_claims.py -v`
Expected: FAIL (`module 'copy_lint' has no attribute 'claim_violations'`)

- [ ] **Step 3: copy_lint.py 에 추가**

**원본** (`skills/copy-angle-explorer/scripts/copy_lint.py:29-37`):
```python
def hero_violations(hero):
    v = []
    if len(hero["headline"]) > HEADLINE_MAX:
        v.append(f"헤드라인 {len(hero['headline'])}자 (상한 {HEADLINE_MAX})")
    if len(hero["sub"]) > SUB_MAX:
        v.append(f"서브 {len(hero['sub'])}자 (상한 {SUB_MAX})")
    if len(hero["ctas"]) != 1:
        v.append(f"CTA {len(hero['ctas'])}개 (정확히 1개여야 함)")
    return v
```

**수정 후**:
```python
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
```

- [ ] **Step 4: 통과 확인 + Commit**

Run: `python3 -m pytest tests/test_claims.py -v` → Expected: PASS
```bash
git add skills/copy-angle-explorer/scripts/copy_lint.py tests/test_claims.py
git commit -m "feat(lint): quantitative claim extraction vs whitelist"
```

---

### Task 5: copy-lint.py — spec 로더 + lint() 집계 + CLI (TDD)

**Files:**
- Modify: `copy-explosion-30-angles/skills/copy-angle-explorer/scripts/copy_lint.py`
- Test: `copy-explosion-30-angles/tests/test_lint_cli.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_lint_cli.py`)

```python
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def _write_case(tmp_path, headline, facts):
    (tmp_path / "spec.json").write_text(json.dumps({"facts": facts, "language": "ko"}), encoding="utf-8")
    html = f'<h1 class="cx-headline">{headline}</h1><p class="cx-sub">서브</p><a class="cx-cta" href="#">A</a>'
    p = tmp_path / "angle-01-fear.html"
    p.write_text(html, encoding="utf-8")
    return p

def test_lint_flags_invented_number(tmp_path):
    p = _write_case(tmp_path, "고객 9999명 돌파", facts=["무료 체험"])
    fails, warns = cl.lint(p, cl.load_spec(tmp_path))
    assert any("9999" in f for f in fails)

def test_lint_clean_passes(tmp_path):
    p = _write_case(tmp_path, "지금 무료로 시작하세요", facts=["무료 체험"])
    fails, warns = cl.lint(p, cl.load_spec(tmp_path))
    assert fails == []

def test_load_spec_missing_returns_empty_facts(tmp_path):
    assert cl.load_spec(tmp_path) == {"facts": [], "language": "ko"}
```

- [ ] **Step 2: 실패 확인**

Run: `python3 -m pytest tests/test_lint_cli.py -v`
Expected: FAIL (`no attribute 'lint'` / `'load_spec'`)

- [ ] **Step 3: copy_lint.py 하단에 추가** (파일 끝에 append)

**수정 후** (append to `skills/copy-angle-explorer/scripts/copy_lint.py`):
```python
import json, os, sys, glob

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
        print(__doc__); return 0
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
```

- [ ] **Step 4: 통과 확인 + 전체 스위트 + Commit**

Run: `python3 -m pytest tests/ -v` → Expected: 전부 PASS
```bash
git add skills/copy-angle-explorer/scripts/copy_lint.py tests/test_lint_cli.py
git commit -m "feat(lint): spec loader + lint aggregation + CLI"
```

---

### Task 6: hero-template.md — 중립 히어로 골격 (copy-lint 계약의 원천)

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/hero-template.md`
- Test: `copy-explosion-30-angles/tests/test_hero_template.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_hero_template.py`)

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "skills/copy-angle-explorer/references/hero-template.md"

def test_template_defines_contract_classes():
    s = T.read_text(encoding="utf-8")
    for cls in ("cx-headline", "cx-sub", "cx-cta"):
        assert cls in s, f"{cls} 누락 — copy-lint 파싱 계약"

def test_template_footer_slot_present():
    assert "ANGLE" in T.read_text(encoding="utf-8")
```

- [ ] **Step 2: 실패 확인** → Run: `python3 -m pytest tests/test_hero_template.py -v` → FAIL (파일 없음)

- [ ] **Step 3: hero-template.md 작성** (new file). 내용: 중립 스타일(무채색+단일 액센트, Pretendard) 단일 히어로 HTML 골격. **필수 요소** — `<h1 class="cx-headline">`, `<p class="cx-sub">`, `<a class="cx-cta">` 정확히 1개, 하단 `ANGLE {n} · {각도명} · {패밀리}` 푸터, `prefers-reduced-motion` 대응, self-contained(폰트 CDN만). 카피 자리는 `{{HEADLINE}}`·`{{SUB}}`·`{{CTA}}` 플레이스홀더로 표기. design-explosion 의 기술 요건(단일 .html, JS 연출 전용) 준수.

- [ ] **Step 4: 통과 확인 + Commit**

Run: `python3 -m pytest tests/test_hero_template.py -v` → PASS
```bash
git add skills/copy-angle-explorer/references/hero-template.md tests/test_hero_template.py
git commit -m "feat(refs): neutral hero template + lint contract"
```

---

### Task 7: master-copy-prompt.md

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/master-copy-prompt.md`

**Model**: sonnet

- [ ] **Step 1: 작성** (new file) — 세션당 1회 읽는 공통 프롬프트. 담을 것:
  1. **제품 사실 스펙 스키마** (§3.1: 제품명/한줄/타겟/핵심이득[]/근거·사실[]/언어/톤힌트)
  2. **최상위 규율(NFR-1)**: "근거·사실[] 밖의 수치·수상·고객사·기능을 절대 만들지 마라. 애매하면 빼라." — 굵게, 프롬프트 맨 앞.
  3. **히어로 HTML 기술 요건**: hero-template.md 사용, cx-* 클래스 준수, 히어로 상한(60/140/CTA 1), self-contained.
  4. **중립 스타일 스펙**: 모든 시안 공통(색·타이포·여백) — 스타일이 변수가 되면 안 됨(FR-8).
  5. **언어**: 제품 언어(기본 ko), 실존 인물·기업 예시 금지.

- [ ] **Step 2: 검증** — Run: `grep -c "근거·사실" skills/copy-angle-explorer/references/master-copy-prompt.md` → Expected: ≥ 1

- [ ] **Step 3: Commit** → `git add … && git commit -m "feat(refs): master-copy-prompt (product-spec + truthfulness + hero reqs)"`

---

### Task 8: truthfulness.md — 지어내지 않기 규율 + 클레임 판정 기준

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/truthfulness.md`

**Model**: sonnet

- [ ] **Step 1: 작성** (new file) — copy-lint 와 판정 서브에이전트가 공유하는 진실성 기준: (a) FAIL 대상(근거 없는 수치·%·수상어), (b) WARN 대상(고유명사 오탐 여지), (c) [MANUAL]/판정 에이전트 대상(과장·함의·각도 구별성). copy-lint.py 의 SUPERLATIVES 목록과 일치시킬 것.
- [ ] **Step 2: 검증** — Run: `grep -c "MANUAL" skills/copy-angle-explorer/references/truthfulness.md` → ≥ 1
- [ ] **Step 3: Commit** → `git commit -m "feat(refs): truthfulness discipline"`

---

### Task 9: angle-taxonomy.md — 30 각도 × 6 패밀리 인덱스

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/angle-taxonomy.md`
- Test: `copy-explosion-30-angles/tests/test_taxonomy.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_taxonomy.py`)

```python
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "skills/copy-angle-explorer/references/angle-taxonomy.md"

def test_taxonomy_has_30_numbered_angles():
    nums = set(re.findall(r"\b(0[1-9]|[12]\d|30)\b", T.read_text(encoding="utf-8")))
    assert len(nums) == 30, f"각도 번호 {len(nums)}개 (30 필요)"

def test_taxonomy_names_six_families():
    s = T.read_text(encoding="utf-8")
    for fam in ("감정", "논리", "사회적", "서사", "인지", "구조"):
        assert fam in s
```

- [ ] **Step 2: 실패 확인** → Run: `python3 -m pytest tests/test_taxonomy.py -v` → FAIL

- [ ] **Step 3: 작성** (new file) — tech-design §3.4 표를 그대로 옮긴 30×6 인덱스. 각 행: 번호·각도명·패밀리·한 줄 설명. 01~30 전부.

- [ ] **Step 4: 통과 확인 + Commit** → Run: `python3 -m pytest tests/test_taxonomy.py -v` → PASS → `git commit -m "feat(refs): 30-angle x 6-family taxonomy"`

---

### Task 10: decision-framework.md — 퍼널·조합·역추출

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/decision-framework.md`

**Model**: sonnet

- [ ] **Step 1: 작성** (new file) — design-explosion decision-framework.md 를 메시지 축으로 각색: 퍼널(패밀리 대표 방향 → 정독 → 결승 2~3개), 조합(헤드라인/서브/CTA/톤 축 병합), 역추출(확정 각도 → 포지셔닝 한 줄 + 핵심 약속 + 톤 규칙), design-explosion 핸드오프 안내. (FR-15,16,17)
- [ ] **Step 2: 검증** — Run: `grep -Ec "퍼널|역추출|핸드오프" skills/copy-angle-explorer/references/decision-framework.md` → ≥ 1
- [ ] **Step 3: Commit** → `git commit -m "feat(refs): decision framework (funnel/hybrid/extract)"`

---

### Task 11: 각도 프롬프트 스키마 + 예시 (angle-01)

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/references/prompts/angle-01-fear.md`
- Test: `copy-explosion-30-angles/tests/test_angle_prompts.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_angle_prompts.py`)

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "skills/copy-angle-explorer/references/prompts"

REQUIRED = ["각도명", "패밀리", "설득 구조", "헤드라인 공식", "톤", "좋은 예", "나쁜 예", "금지", "크리틱"]

def test_angle01_has_all_schema_sections():
    s = (P / "angle-01-fear.md").read_text(encoding="utf-8")
    missing = [k for k in REQUIRED if k not in s]
    assert not missing, f"angle-01 누락 섹션: {missing}"
```

- [ ] **Step 2: 실패 확인** → Run: `python3 -m pytest tests/test_angle_prompts.py -v` → FAIL

- [ ] **Step 3: angle-01-fear.md 작성** (new file) — 스키마 완성형 예시: 각도명(공포/불안)·패밀리(A 감정 소구)·설득 구조·헤드라인 공식·톤·좋은 예/나쁜 예·금지(공포 조장이 근거 없는 위협이 되지 않게 — 진실성 규율 재확인)·크리틱 루프. **이 파일이 나머지 29개의 템플릿.**

- [ ] **Step 4: 통과 확인 + Commit** → Run: `python3 -m pytest tests/test_angle_prompts.py -v` → PASS → `git commit -m "feat(prompts): angle schema + angle-01 exemplar"`

---

### Task 12: 각도 프롬프트 — 패밀리 A 나머지 (02~05)

**Files:**
- Create: `references/prompts/angle-02-desire.md`, `angle-03-relief.md`, `angle-04-pride.md`, `angle-05-belonging.md`
- Modify: `tests/test_angle_prompts.py`

**Model**: sonnet

- [ ] **Step 1: 테스트에 파일 존재 + 스키마 검사 추가**

**원본** (`tests/test_angle_prompts.py:9-12`):
```python
def test_angle01_has_all_schema_sections():
    s = (P / "angle-01-fear.md").read_text(encoding="utf-8")
    missing = [k for k in REQUIRED if k not in s]
    assert not missing, f"angle-01 누락 섹션: {missing}"
```

**수정 후**:
```python
def test_angle01_has_all_schema_sections():
    s = (P / "angle-01-fear.md").read_text(encoding="utf-8")
    missing = [k for k in REQUIRED if k not in s]
    assert not missing, f"angle-01 누락 섹션: {missing}"

def test_all_present_angle_files_follow_schema():
    for f in P.glob("angle-*.md"):
        s = f.read_text(encoding="utf-8")
        missing = [k for k in REQUIRED if k not in s]
        assert not missing, f"{f.name} 누락 섹션: {missing}"
```

- [ ] **Step 2: 실패 확인** → Run: `python3 -m pytest tests/test_angle_prompts.py -v` → FAIL (02~05 없음 → glob 통과하지만 존재 검사는 Task 17 종합에서; 여기선 스키마 검사가 새 파일 대상)
- [ ] **Step 3: 02~05 4개 파일 작성** — angle-01 스키마를 따르되 각 각도(열망·안도·자부심·소속감)에 맞는 설득 구조·헤드라인 공식·좋은/나쁜 예. angle-taxonomy.md 와 번호·이름 일치.
- [ ] **Step 4: 통과 확인 + Commit** → Run: `python3 -m pytest tests/test_angle_prompts.py -v` → PASS → `git commit -m "feat(prompts): family A angles 02-05"`

---

### Task 13: 각도 프롬프트 — 패밀리 B 논리·증거 (06~10)

**Files:** Create `references/prompts/angle-06-data.md` … `angle-10-mechanism.md`
**Model**: sonnet

- [ ] **Step 1**: angle-01 스키마로 06~10 작성 (데이터·수치 / 비교·경쟁우위 / ROI·비용 / 보증·리스크제거 / 메커니즘). **주의**: 이 패밀리는 수치를 자주 쓰므로 각 파일 금지 섹션에 "제품 스펙의 근거·사실[] 밖 수치 금지(copy-lint FAIL)" 를 명시.
- [ ] **Step 2**: Run `python3 -m pytest tests/test_angle_prompts.py -v` → PASS (스키마)
- [ ] **Step 3**: Commit → `git commit -m "feat(prompts): family B angles 06-10"`

---

### Task 14: 각도 프롬프트 — 패밀리 C 사회적 증명 (11~15)

**Files:** Create `angle-11-testimonial.md` … `angle-15-fomo.md`
**Model**: sonnet

- [ ] **Step 1**: 11~15 작성 (고객 목소리 / 권위·전문가 / 밴드왜건 / 희소성·긴급 / FOMO). **주의**: 고객사·수상 언급 각도이므로 금지 섹션에 "실존 고객사/수상 지어내기 금지 — 제품 스펙에 있을 때만".
- [ ] **Step 2**: Run pytest → PASS
- [ ] **Step 3**: Commit → `git commit -m "feat(prompts): family C angles 11-15"`

---

### Task 15: 각도 프롬프트 — 패밀리 D 서사 (16~20)

**Files:** Create `angle-16-story.md` … `angle-20-contrast.md`
**Model**: sonnet

- [ ] **Step 1**: 16~20 작성 (스토리 / 비포·애프터 / 적 프레이밍 / 은유 / 대비-전환점).
- [ ] **Step 2**: Run pytest → PASS
- [ ] **Step 3**: Commit → `git commit -m "feat(prompts): family D angles 16-20"`

---

### Task 16: 각도 프롬프트 — 패밀리 E 인지 단계 (21~25)

**Files:** Create `angle-21-problem-aware.md` … `angle-25-unaware.md`
**Model**: sonnet

- [ ] **Step 1**: 21~25 작성 (문제 인식 / 해결책 인식 / 제품 인식 / 가장 의식적-오퍼 / 미인식-교육형). Schwartz 인식 단계 근거를 각 파일에 한 줄.
- [ ] **Step 2**: Run pytest → PASS
- [ ] **Step 3**: Commit → `git commit -m "feat(prompts): family E angles 21-25"`

---

### Task 17: 각도 프롬프트 — 패밀리 F 구조·수사 (26~30) + 30개 완비 검증

**Files:** Create `angle-26-question.md` … `angle-30-minimal.md`; Modify `tests/test_angle_prompts.py`
**Model**: sonnet

- [ ] **Step 1: 30개 완비 테스트 추가**

**원본** (`tests/test_angle_prompts.py:1-6`):
```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "skills/copy-angle-explorer/references/prompts"

REQUIRED = ["각도명", "패밀리", "설득 구조", "헤드라인 공식", "톤", "좋은 예", "나쁜 예", "금지", "크리틱"]
```

**수정 후**:
```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "skills/copy-angle-explorer/references/prompts"

REQUIRED = ["각도명", "패밀리", "설득 구조", "헤드라인 공식", "톤", "좋은 예", "나쁜 예", "금지", "크리틱"]

def test_exactly_30_angle_files():
    files = sorted(P.glob("angle-*.md"))
    assert len(files) == 30, f"각도 파일 {len(files)}개 (30 필요)"
```

- [ ] **Step 2**: 26~30 작성 (질문형 / 대담한 주장 / How-to / 리스티클·숫자 / 미니멀 한 문장).
- [ ] **Step 3**: Run `python3 -m pytest tests/test_angle_prompts.py -v` → Expected: PASS (30개 완비 + 전부 스키마)
- [ ] **Step 4**: Commit → `git commit -m "feat(prompts): family F angles 26-30 + 30-file completeness gate"`

---

### Task 18: SKILL.md — 워크플로 + 트리거 + 참조 인덱스

**Files:**
- Create: `copy-explosion-30-angles/skills/copy-angle-explorer/SKILL.md`
- Test: `copy-explosion-30-angles/tests/test_skill_md.py`

**Model**: sonnet

- [ ] **Step 1: 실패 테스트 작성** (new file: `tests/test_skill_md.py`)

```python
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills/copy-angle-explorer/SKILL.md"

def test_frontmatter_has_name_and_description():
    s = S.read_text(encoding="utf-8")
    assert s.startswith("---")
    assert "name: copy-angle-explorer" in s
    assert "description:" in s

def test_workflow_covers_lint_and_gallery():
    s = S.read_text(encoding="utf-8")
    assert "copy_lint.py" in s
    assert "gallery.html" in s
```

- [ ] **Step 2: 실패 확인** → Run: `python3 -m pytest tests/test_skill_md.py -v` → FAIL

- [ ] **Step 3: SKILL.md 작성** (new file) — design-explosion SKILL.md 미러 구조:
  - frontmatter `name` + `description`(트리거: "카피 뽑아줘", "랜딩 카피 비교", "30가지 메시지", "히어로 카피", "카피 각도" 등 — design-explosion 처럼 풍부하게)
  - 7스테이지 워크플로(입력·되물음 → 제품스펙 고정 → 30각도 병렬생성[각 에이전트 자기 angle 파일만] → copy_lint.py 게이트 → gallery.html → 퍼널 → 역추출·핸드오프)
  - 병렬/직렬 자동 분기 안내
  - 참조 파일 인덱스(master-copy-prompt·angle-taxonomy·hero-template·truthfulness·decision-framework·prompts/·scripts/copy_lint.py)

- [ ] **Step 4: 통과 확인 + Commit** → Run: `python3 -m pytest tests/test_skill_md.py -v` → PASS → `git commit -m "feat: copy-angle-explorer SKILL.md workflow"`

---

### Task 19: README.md

**Files:** Create `copy-explosion-30-angles/README.md`
**Model**: sonnet

- [ ] **Step 1**: 작성 (new file) — design-explosion README 톤 미러: "막연한 '카피 잘 써줘'를, 30가지 확실히 다른 메시지 각도로". 설치 명령(`/plugin marketplace add deokjinlog/copy-explosion-30-angles`), 3단계 사용법, design-explosion 과의 짝 관계(스타일×메시지=랜딩) 명시.
- [ ] **Step 2**: 검증 — Run: `grep -c "design-explosion" README.md` → ≥ 1 (짝 관계 링크)
- [ ] **Step 3**: Commit → `git commit -m "docs: README"`

---

### Task 20: 문서 이전 + 최종 검증

**Files:**
- Create: `copy-explosion-30-angles/docs/features/2026-07-19-copy-explosion/` (3 MD + 2 HTML 복사)

**Model**: haiku

- [ ] **Step 1: 기획 문서 복사 (비파괴 — 원본 유지)**

```bash
mkdir -p /home/djchoi/deokjinlog/copy-explosion-30-angles/docs/features/2026-07-19-copy-explosion
cp /home/djchoi/deokjinlog/design-explosion-30-styles/docs/features/2026-07-19-copy-explosion/copy-explosion-*.md \
   /home/djchoi/deokjinlog/design-explosion-30-styles/docs/features/2026-07-19-copy-explosion/copy-explosion-*.html \
   /home/djchoi/deokjinlog/copy-explosion-30-angles/docs/features/2026-07-19-copy-explosion/
```

- [ ] **Step 2: 전체 테스트 스위트 최종 실행**

Run: `cd /home/djchoi/deokjinlog/copy-explosion-30-angles && python3 -m pytest tests/ -v`
Expected: 전부 PASS (manifest / hero / claims / lint CLI / hero-template / taxonomy / angle prompts×30 / SKILL)

- [ ] **Step 3: copy-lint 스모크 (지어낸 수치 잡히는지 실제 확인)**

```bash
cd /home/djchoi/deokjinlog/copy-explosion-30-angles
mkdir -p /tmp/cx-smoke && echo '{"facts":["무료 체험"],"language":"ko"}' > /tmp/cx-smoke/spec.json
printf '<h1 class="cx-headline">고객 1만명 돌파</h1><p class="cx-sub">서브</p><a class="cx-cta" href="#">시작</a>' > /tmp/cx-smoke/angle-01-fear.html
python3 skills/copy-angle-explorer/scripts/copy_lint.py /tmp/cx-smoke; echo "exit=$?"
```
Expected: `[FAIL]` + "근거 없는 수치 '1만'"? — (참고: "1만" 은 한글 혼합이라 현재 정규식은 아라비아 숫자만; 스모크는 "10000" 으로 확인) → `exit=1`

- [ ] **Step 4: Commit** → `git add docs && git commit -m "docs: copy planning docs into repo + final verification"`

---

## 2. 위험 코드 지점

- `skills/copy-angle-explorer/scripts/copy_lint.py:claim_violations` — **side-effect**: 정량 클레임 추출 휴리스틱의 오탐/미탐. 한글 수사("1만")·복합 고유명사는 현재 정규식이 놓칠 수 있음. (mitigation: 위험한 미탐은 판정 서브에이전트 2차 필터, 오탐은 WARN 등급; 한글 수사 확장은 백로그)
- `skills/copy-angle-explorer/scripts/copy_lint.py:extract_hero` — **breaking**: hero-template.md 의 cx-* 클래스명이 바뀌면 파싱이 전부 깨짐. (mitigation: Task 6 test_hero_template 이 클래스 계약을 고정, 템플릿·린터를 같은 계약 문서로 묶음)
- `references/prompts/angle-*.md` (병렬 생성 시) — **side-effect**: 각 에이전트가 제품 스펙 밖 사실을 추론·삽입(hallucination → NFR-1 위반). (mitigation: master-copy-prompt 최상위 금지 못박음 + copy_lint 정량 게이트 2중)
- 병렬 생성 공유 파일 — **race**: 없음. spec.json·angle 파일 모두 read-only.

## 3. 롤백 전략

- Code: `copy-explosion-30-angles` 는 신규 repo — task 별 커밋(per-task)이라 `git revert <SHA>` 또는 `git reset --hard <이전 SHA>` 로 task 단위 롤백. (로컬 전용, push 없음)
- 문서 이전(Task 20): 복사이므로 원본(design-explosion 하위)은 그대로 — 롤백 시 신규 repo 의 docs/ 만 삭제.
- 플러그인 등록: 아직 마켓 push 안 함 — 로컬 검증 단계라 외부 롤백 불필요.

---
## 변경이력
<!-- change-history skill auto-appends entries here, oldest first -->

### [2026-07-19 04:14] [구현계획서-수정]
- **id**: CH-20260719-003
- **이유**: 신규 구현계획 — copy-explosion 을 20 task(TDD)로 분해. copy_lint.py 3-task 엄격 TDD + 참조 콘텐츠(master/taxonomy/hero-template/truthfulness/decision) + 30 각도 프롬프트(패밀리별) + SKILL.md + 스캐폴드/문서이전.
- **무엇이**: copy-explosion-implementation-plan.md 전체 최초 생성 (§1 20 tasks, §2 위험 코드 지점 3범주, §3 롤백 전략)
- **영향범위**: 없음 (최초 생성). 알려진 gap 1건 — AC-5 한글 수사("1만") 미탐(copy_lint 아라비아 숫자만), 위험 §2 + 백로그 + 판정 에이전트 2차필터로 처리(사용자 승인).
- **연관 항목**: CH-20260719-001, CH-20260719-002

### [2026-07-19 04:59] [코드-수정] (batch: tasks 1..19)
- **id**: CH-20260719-004
- **이유**: subagent-driven wave-parallel 실행으로 copy-explosion 스킬 전체 구현 (신규 repo `/home/djchoi/deokjinlog/copy-explosion-30-angles`, 6 waves). 전체 테스트 22 passed + copy_lint CLI 스모크(지어낸 수치 감지) 확인.
- **무엇이**: `.claude-plugin/plugin.json·marketplace.json`, `skills/copy-angle-explorer/scripts/copy_lint.py`(히어로 추출·제약 + 정량 클레임 화이트리스트 + spec 로더·CLI), `references/`(master-copy-prompt·truthfulness·angle-taxonomy·hero-template·decision-framework), `references/prompts/angle-01..30`(30 각도 6패밀리), `SKILL.md`, `README.md`, `tests/`(test_manifest·hero_constraints·claims·lint_cli·hero_template·taxonomy·angle_prompts·skill_md)
- **영향범위**: 신규 repo 전체 — 기존 design-explosion 코드 무영향(repo 분리). 로컬 커밋만(push 없음).
- **위험 카테고리**: side-effect — copy_lint `claim_violations` 정량 추출 휴리스틱(한글 수사 미탐 / 라틴 고유명사 오탐). RISK 주석 부착(copy_lint.py:claim_violations), 판정 서브에이전트 2차필터로 보완.
- **task별 세부 (19건, 코드 블록은 git 조회)**:
  - Task 1: repo 스캐폴드 + git init — commit `d062bf1`
  - Task 2: 플러그인 매니페스트 — commit `c95d57c`
  - Task 3: copy_lint 히어로 추출·제약 — commit `20e6411`
  - Task 4: copy_lint 정량 클레임(+RISK) — commit `3df6acb`
  - Task 5: copy_lint spec 로더·CLI — commit `fdde592`
  - Task 6: hero-template(cx-* 계약) — commit `35c6081`
  - Task 7: master-copy-prompt — commit `dc0a351`
  - Task 8: truthfulness — commit `93e078e`
  - Task 9: angle-taxonomy(30×6) — commit `a931b54`
  - Task 10: decision-framework — commit `1e8b09d`
  - Task 11: angle-01 예시 — commit `6a7bcd9`
  - Task 12~16: 각도 02~25(패밀리 A~E) — commits `092e62c`,`bb48c59`,`37fde68`,`b583f59`,`7399612`
  - Task 17: 각도 26~30 + 30완비 게이트 — commit `ccec11c`
  - Task 18: SKILL.md — commit (wave 5)
  - Task 19: README — commit `efe34d5`
- **연관 항목**: CH-20260719-003 (본 계획서)
