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

## 어떻게 설계됐나 — 곱셈 3축

| 축 | 뜻 | 정하는 것 | 노동 |
|---|---|---|---|
| **도메인** | 업종(주제) | 무슨 콘텐츠·숫자가 채워지나 | 입력만 |
| **원형** | 화면 종류 11개 | 어떤 뼈대 HTML인가 | 고르기 |
| **스타일** | 디자인 언어 30개 | ← **이것만 변함** | 재사용 |

```
도메인 "중고거래 마켓"
   │
   ├─▶ 원형 결정        도메인 → D 컬렉션        "이 화면에서 하는 단 하나의 행동은?"
   │
   ├─▶ 콘텐츠 채우기      도메인 + 원형 슬롯       "아이폰 ₩780,000"을 item-card에
   │        └──────────▶ 스켈레톤 1개(고정 HTML)   ★ 프로젝트마다 새로 만드는 유일한 것
   │
   └─▶ CSS 30벌 조립     base + tokens/NN + signature/NN   → assemble.py → style-01~30.html
```

**매번 손으로 만드는 건 스켈레톤 1개뿐.** 스타일 30벌·조립기·게이트는 전부 재사용 — 같은 원형이면 새 도메인도 CSS 라이브러리를 그대로 갖다 씁니다.

---

## 어떻게 만들어지나 — Zen Garden 3층

[CSS Zen Garden](http://www.csszengarden.com/)의 계보(HTML 한 장 고정 + CSS만 N벌). 스타일 1개 = **CSS 3층**을 스켈레톤에 입힌 것 — 세 층은 **재사용 범위**가 다릅니다:

| 층 | 맡는 것 | 재사용 범위 | 누가 저작 |
|---|---|---|---|
| **base** | 원형의 부품 조립(형태·배치, 값은 `var()`로 비움) | 원형당 1개 — 30 스타일 공유 | 손 |
| **tokens/NN** | 스타일의 값 12개(색·폰트·radius·스케일) | 스타일당 1개 — 원형·도메인 무관 | 손·스크립트 |
| **signature/NN** | 값으론 안 되는 구조(도형·격자·하드섀도…) | 구조형 스타일만 (D 21·A 10·B 17) | LLM(디자인 판단) |

**저작은 한 번, 이후 고정 라이브러리.** `assemble.py`(스크립트, **LLM 토큰 0**)가 세 층을 스켈레톤에 인라인 → 30장 자립 HTML. 갤러리를 100번 뽑아도 조립은 스크립트라 토큰이 안 듭니다.

이 구조가 주는 세 가지:

- **콘텐츠 동일성 (구조 보장)** — 30장이 `<body>` 바이트까지 동일. AI에게 "똑같이 해줘"라고 부탁하지 않고 스켈레톤 하나를 공유해 강제. 나란히 놓으면 다른 건 오직 스타일.
- **잘못된 화면 원천 차단** — CSS는 스켈레톤에 **있는 요소만** 꾸밉니다. D 스켈레톤엔 KPI·차트 요소가 0개라, 어떤 스타일을 입혀도 대시보드가 될 수 없음. (사후 린트가 아니라 애초에 사고가 안 남 — `coverage-lint`는 화면 종류가 아니라 CSS 배선만 검사.)
- **저비용 재사용** — 새 스타일 = 값 12개(+구조형이면 signature 1개), 한 번. 세 원형에 즉시 적용되고, 한 번 고치면 전 갤러리에 반영.

---

## 근거 — 감이 아니라 공개 데이터에 접지

| 축 | 출처 | 왜 |
|---|---|---|
| **구조(1 HTML·N CSS)** | [CSS Zen Garden](http://www.csszengarden.com/) — 한 HTML을 CSS만으로 218 디자인 | "내용 고정·표현만 변수"를 증명한 원조 |
| **원형 11종** | [Enrico](https://github.com/luileito/enrico) — RICO 72k → 1,460 UI를 사람이 20토픽 분류 | 화면 종류를 감이 아닌 실데이터로 검증·보완(A 대시보드는 추가) |
| **도메인 프리셋** | [Mind2Web](https://osu-nlp-group.github.io/Mind2Web/) — 136 사이트·2,022 태스크 | 업종→원형 매핑의 근거(덮어쓰기 가능한 기본값) |
| **스타일 30** | 디자인 시스템·운동 — [출처 문서](docs/design/2026-07-26-type-and-source-grounding.md) | 산업 라벨 대신 문서화된 디자인 언어로 접지 |

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

<sub>행동은 화면 고유 성질 — 도메인과 <b>직교</b>합니다. 패션몰도 중고거래도 "고른다"라 둘 다 D(콘텐츠만 다름). 화면을 바꾸려면 원형을 바꿔야 합니다.</sub>

---

## 스타일 30 — 산업 라벨이 아니라 고수의 출처로

"헬스케어·핀테크"는 시각 규칙이 없어 기본값(흰 배경+둥근 카드+Inter)으로 수렴합니다. 그래서 **문서화된 디자인 언어**로 접지했습니다:

- **디자인 시스템** — IBM Carbon · Material 3 · Ant Design · Shopify Polaris · GOV.UK · shadcn/ui
- **디자인 운동** — Swiss · Bauhaus · De Stijl · Memphis · Neubrutalism · Editorial · Riso
- **모프/시대** — Glassmorphism · Neumorphism · Claymorphism · Y2K · SF HUD · 레트로 픽셀

**정본 서체 22종을 실제 웹폰트로 로드**(Playfair·Cormorant·IBM Plex·Space Mono·VT323·Roboto·Atkinson…)하고, 세 원형에 **구조 시그니처**(D 21 · A 10 · B 17)를 저작해 회색조에서도 구조로 갈리게 했습니다 — Material 3·Carbon·Ant·SF HUD는 세 원형에 같은 토큰 어휘로 일관 저작.

---

## 갤러리 (라이브)

**원형이 바뀌면 화면이 바뀐다** — 같은 도구, 다른 원형:

| [핀테크 · A 대시보드](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fintech-zen/gallery.html) | [연서 · B 대화](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-yeonseo-zen/gallery.html) | [패션 · D 컬렉션](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fashion-zen/gallery.html) |
|---|---|---|

**같은 원형, 새 도메인** — [중고거래 마켓 · D](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-market-zen/gallery.html)는 패션과 같은 D. base·tokens·signature를 그대로 재사용하고 새로 짠 건 **스켈레톤 1개**뿐 — 도메인 무관성의 증거입니다.

📈 [진행 여정 한눈에 보기](https://deokjinlog.github.io/design-explosion-30-styles/progress.html)

---

## 시작 3단계

**1. 설치** — Claude Code 안에서:
```
/plugin marketplace add deokjinlog/design-explosion-30-styles
/plugin install design-explosion-30-styles@design-explosion-30-styles
```

**2. 도메인 던지기** — 아래로 갈수록 정확합니다:
```
핀테크 정산 대시보드 디자인 30개 뽑아줘            ← 도메인만 (원형은 툴이 추론)
연서, 대화형 원형으로 30 스타일 뽑아줘             ← 원형 직접 지정
/home/me/myproject 기준으로 디자인 시안 뽑아줘     ← ⭐ 프로젝트 폴더(제일 정확)
```

**3. 갤러리에서 고르기** — 나란히 훑고 마음에 드는 번호를 고르면 끝.

<sub>산출물은 <code>docs/design-gallery/&lt;날짜&gt;-&lt;도메인&gt;/</code> 에 <code>.html</code> 시안 + 비교 갤러리로 쌓입니다.</sub>

---

## 라이선스

MIT
