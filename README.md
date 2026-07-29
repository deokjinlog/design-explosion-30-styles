<p align="center">
  <img src="https://raw.githubusercontent.com/deokjinlog/design-explosion-30-styles/main/docs/banner.svg" alt="design-explosion — 도메인 맞춤형 디자인 30가지 스타일" width="100%">
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.5.0-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Plugin-a78bfa?style=flat-square&labelColor=0d1117">
  <img alt="Styles" src="https://img.shields.io/badge/styles-30-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Zero deps" src="https://img.shields.io/badge/dependencies-zero-22c55e?style=flat-square&labelColor=0d1117">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square&labelColor=0d1117">
</p>

<p align="center">
  <b><a href="https://deokjinlog.github.io/design-explosion-30-styles/">라이브 데모 — 갤러리 열어보기</a></b>
</p>

<br/>

> ## 막연한 "예쁘게 해줘"를, 도메인 맞춤 30가지 방향으로
>
> 업종을 던지면 그 도메인의 **대표 화면(원형)**을 잡고, 같은 화면을 **30가지 디자인**으로 펼칩니다.
> 콘텐츠·구조는 고정하고 **스타일만 변수** — 갤러리에서 보이는 차이는 오직 디자인입니다.

---

## 핵심 모델 — 곱셈 3축

| 축 | 뜻 | 정하는 것 | 노동 |
|---|---|---|---|
| **도메인** | 업종 | 무슨 콘텐츠·숫자가 채워지나 (**고정**) | 입력만 |
| **원형** | 화면 종류 11개 | 어떤 뼈대 HTML인가 (**고정**) | 고르기 |
| **스타일** | 디자인 언어 30개 | ← **이것만 변함** | 재사용 |

```
도메인 입력  "중고거래 마켓"
   │
   ├─① 원형 결정         repo 역산 > Mind2Web 프리셋 > 4문항 인터뷰
   │    "이 화면에서 하는 단 하나의 행동은? → 고른다" → 원형 D
   │
   ├─② 스켈레톤 1개 저작  ★ 프로젝트마다 새로 만드는 유일한 것
   │    원형 D 컴포넌트에 도메인 콘텐츠를 박은 고정 DOM
   │
   ├─③ 30 스타일 조립     기존 라이브러리(base·tokens·signature) 재사용
   │    assemble.py 가 스켈레톤에 30벌 CSS 입힘 → 30장
   │
   └─④ coverage 게이트    환각 셀렉터 0 · 누락 영역 0
```

**매번 손으로 만드는 건 ②의 스켈레톤 1개뿐.** 스타일 30벌·게이트·조립기는 전부 재사용 — 같은 원형이면 새 도메인도 30 스타일 라이브러리를 그대로 갖다 씁니다.

---

## 생성 엔진 — Zen Garden 3층

[CSS Zen Garden](http://www.csszengarden.com/)의 계보(하나의 markup, N개 CSS)를 파이프라인으로. 스타일 1개 = **CSS 3층**을 스켈레톤에 입힌 것 — 세 층은 재사용 범위가 다릅니다:

| 층 | 맡는 것 | 재사용 범위 |
|---|---|---|
| **base** | 원형의 부품 조립(형태·배치, 값은 `var()`로 비움) | 원형당 1개 — 30 스타일 공유 |
| **tokens/NN** | 스타일의 값 12개(색·폰트·radius·스케일) | 스타일당 1개 — 원형·도메인 무관 |
| **signature/NN** | 값으론 안 되는 구조(도형·격자·하드섀도…) | 구조형 스타일만(D 21·A 10·B 17) |

`assemble.py`(스크립트, LLM 토큰 0)가 셋을 스켈레톤에 인라인 → **30장 자립 HTML, `<body>`는 바이트까지 동일하고 `<style>`만 다릅니다.** 콘텐츠 동일성을 AI에게 부탁하지 않고 구조로 보장하는 것 — 30장을 나란히 놓으면 다른 건 오직 스타일입니다.

품질은 두 겹: **화면 틀림은 스켈레톤이 구조로 예방**(원형 D엔 대시보드를 넣을 수 없음 — 사후 린트가 아니라 애초에 사고가 안 남), **CSS 배선은 `coverage-lint`가 검사**(환각 셀렉터·누락 영역 0).

---

## 원형 11종 — "이 화면에서 사용자가 하는 단 하나의 행동은?"

| 원형 | 행동 | 주인공 |  | 원형 | 행동 | 주인공 |
|---|---|---|---|---|---|---|
| **A** 대시보드 | 훑어본다 | KPI·차트·표 | | **G** 에디터 | 만든다 | 편집영역·툴바 |
| **B** 대화 | 주고받는다 | 말풍선·입력창 | | **H** 검색 | 찾는다 | 검색어·결과 |
| **C** 읽기 | 읽는다 | 긴 본문 | | **I** 온보딩 | 익힌다 | 슬라이드·진행 |
| **D** 컬렉션 | 고른다 | 카드그리드·필터 | | **J** 인증 | 들어간다 | 단일 카드 |
| **E** 폼 | 채운다 | 입력·단계 | | **K** 프로필·설정 | 관리한다 | 행 밀도·토글 |
| **F** 피드 | 흘려본다 | 시간순 스트림 | | | | |

<sub>임의 분류가 아니라 <a href="https://github.com/luileito/enrico">Enrico</a>(RICO 72k 모바일 UI에서 추린 1,460 UI·사람 20토픽 분류)로 겹침 검증 + 누락 보완(온보딩·인증·설정). A 대시보드는 웹·SaaS 핵심이라 우리가 추가. 도메인→원형 프리셋은 <a href="https://osu-nlp-group.github.io/Mind2Web/">Mind2Web</a>(136 사이트·2,022 태스크) 근거.</sub>

---

## 스타일 30 — 산업 라벨이 아니라 고수의 출처로

"헬스케어·핀테크"는 시각 규칙이 없어 기본값(흰 배경+둥근 카드+Inter)으로 수렴합니다. 그래서 **문서화된 디자인 언어**로 접지했습니다:

- **디자인 시스템**: IBM Carbon · Material 3 · Ant Design · Shopify Polaris · GOV.UK · shadcn/ui
- **디자인 운동**: Swiss · Bauhaus · De Stijl · Memphis · Neubrutalism · Editorial · Riso
- **모프/시대**: Glassmorphism · Neumorphism · Claymorphism · Y2K · SF HUD · 레트로 픽셀

**정본 서체 22종을 실제 웹폰트로 로드**(Playfair·Cormorant·IBM Plex·Space Mono·VT323·Roboto·Atkinson…)하고, 세 원형에 **구조 시그니처**(D 21·A 10·B 17)를 저작해 회색조에서도 구조로 갈리게 했습니다 — Material 3·Carbon·Ant·SF HUD는 세 원형에 같은 토큰 어휘로 일관 저작. 출처·서체·차별화 축 전체 → [`docs/design/2026-07-26-type-and-source-grounding.md`](docs/design/2026-07-26-type-and-source-grounding.md).

---

## 갤러리 (라이브)

**원형이 바뀌면 화면이 바뀐다** — 같은 도구, 다른 원형:

| [핀테크 · A 대시보드](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fintech-zen/gallery.html) | [연서 · B 대화](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-yeonseo-zen/gallery.html) | [패션 · D 컬렉션](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fashion-zen/gallery.html) |
|---|---|---|

**같은 원형, 새 도메인** — [중고거래 마켓 · D](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-market-zen/gallery.html)는 패션과 구조가 같고(둘 다 D), base·tokens·signature를 그대로 재사용 — 새로 짠 건 스켈레톤 1개뿐. **도메인 무관성**의 증거입니다.

📈 [진행 여정 한눈에 보기](https://deokjinlog.github.io/design-explosion-30-styles/progress.html) — 세 데모 · 3층 재설계 · 검증 · 타임라인

---

## 시작 3단계

**1. 설치** — Claude Code 안에서:
```
/plugin marketplace add deokjinlog/design-explosion-30-styles
/plugin install design-explosion-30-styles@design-explosion-30-styles
```

**2. 도메인 던지기** — 아래로 갈수록 정확합니다:
```
핀테크 정산 대시보드 디자인 30개 뽑아줘            ← 도메인만
연서, 대화형 원형으로 30 스타일 뽑아줘             ← 원형 직접 지정
/home/me/myproject 기준으로 디자인 시안 뽑아줘     ← ⭐ 프로젝트 폴더(제일 정확)
```

**3. 갤러리에서 고르기** — 나란히 훑고 마음에 드는 번호를 고르면 끝.

<sub>산출물은 <code>docs/design-gallery/&lt;날짜&gt;-&lt;도메인&gt;/</code> 에 <code>.html</code> 시안 + 비교 갤러리로 쌓입니다.</sub>

---

## 라이선스

MIT
