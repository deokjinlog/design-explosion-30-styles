<p align="center">
  <img src="https://raw.githubusercontent.com/deokjinlog/design-explosion-30-styles/main/docs/banner.svg" alt="design-explosion — 도메인 맞춤형 디자인 30가지 스타일" width="100%">
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.3.0-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Plugin-a78bfa?style=flat-square&labelColor=0d1117">
  <img alt="Styles" src="https://img.shields.io/badge/styles-30-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Zero deps" src="https://img.shields.io/badge/dependencies-zero-22c55e?style=flat-square&labelColor=0d1117">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square&labelColor=0d1117">
</p>

<p align="center">
  <b><a href="https://deokjinlog.github.io/design-explosion-30-styles/">라이브 데모 — 갤러리 열어보기</a></b>
</p>

<br/>

> ## 막연한 "예쁘게 해줘"를, 도메인 맞춤형 30가지 방향으로
>
> 업종을 고르면 그 도메인에 맞는 **화면(원형)**을 잡고, **같은 화면을 30가지 디자인 스타일**로 펼칩니다.
> 콘텐츠·구조는 고정하고 **스타일만 변수** — 그래서 갤러리에서 눈에 보이는 차이는 오직 디자인입니다.

---

## 완성 데모 — 도메인이 바뀌면 원형이 바뀐다

세 데모 모두 **30 스타일 · 콘텐츠 한 글자도 동일 · 두 게이트 전수 통과**. 차트·아바타·타이핑까지 전부 순수 CSS·SVG(라이브러리 0).

| 데모 (열어보기) | 도메인 | 원형 | archetype-lint 판정 |
|---|---|---|---|
| [**패션 쇼핑몰**](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-22-fashion-demo/gallery.html) | Shopping › Fashion | **D 컬렉션형** | KPI·차트·목표 **금지** |
| [**핀테크 정산 대시보드**](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-23-fintech-demo/gallery.html) | Info › Finance | **A 대시보드형** | 그 셋이 **필수** |
| [**연서 대화형 AI**](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-24-yeonseo-chat-demo/gallery.html) | 대화형 AI 제품 | **B 대화형** | KPI·차트 **금지** |

**같은 게이트, 다른 판정.** 패션 D·연서 B에선 KPI 하나만 나와도 FAIL, 핀테크 A에선 없으면 FAIL — 원형이 화면 종류를 진짜로 구분한다는 증거입니다.

---

## 어떻게 되나 — 곱셈 3층 (도메인 × 원형 × 스타일)

| 층 | 뜻 | 갤러리에서 |
|---|---|---|
| **도메인** | 업종 | 무슨 콘텐츠·숫자가 채워지나 (**고정**) |
| **원형** | 화면 종류 11개 | 어떤 뼈대(KPI·표 vs 카드 그리드 vs 대화)인가 (**고정**) |
| **스타일** | 디자인 느낌 | 30갈래 (**← 이것만 변함**) |

**한 갤러리 = 원형 1개 고정 + 스타일 30개.** 콘텐츠·원형을 고정하니 비교가 사과 대 사과가 됩니다. 두 자동 게이트가 품질을 지킵니다:
- `style-lint` — 그 스타일의 금지를 어겼나 (브루탈리즘인데 그라디언트?)
- `archetype-lint` — **이 도메인의 화면이 맞나** (대화 제품에 KPI·도넛이 박히는 사고를 잡습니다)

<sub>원형·도메인 매핑은 감이 아니라 공개 데이터 근거입니다 — <a href="https://osu-nlp-group.github.io/Mind2Web/">Mind2Web</a>(136 사이트·2,022 태스크, 도메인 프리셋) + <a href="https://github.com/luileito/enrico">Enrico</a>(1,460 UI, 원형 11종 검증). 집계 원본을 repo에 넣어 재현 가능합니다.</sub>

---

## 원형 11종 — "이 화면에서 사용자가 하는 단 하나의 행동은?"

| 원형 | 행동 | 주인공 |
|---|---|---|
| A 대시보드 | 훑어본다 | KPI·차트·표 |
| B 대화 | 주고받는다 | 말풍선·입력창 |
| C 읽기 | 읽는다 | 긴 본문 타이포 |
| D 컬렉션 | 고른다 | 카드 그리드·필터 |
| E 폼 | 채워넣는다 | 입력 필드·단계 |
| F 피드 | 흘려본다 | 시간순 스트림 |
| G 에디터 | 만든다 | 편집 영역·툴바 |
| H 검색 | 찾는다 | 검색어·결과 |
| I 온보딩 | 처음 익힌다 | 슬라이드·진행 |
| J 인증 | 들어간다 | 단일 카드 |
| K 프로필·설정 | 관리한다 | 행 밀도·토글 |

이 답이 **원형**을 정하고, 원형이 화면 구성을 정합니다. (프로젝트 폴더를 주면 요구사항·코드를 읽어 자동 역산합니다.)

---

## 3단계로 시작

**1. 설치** — Claude Code 안에서:
```
/plugin marketplace add deokjinlog/design-explosion-30-styles
/plugin install design-explosion-30-styles@design-explosion-30-styles
```

**2. 도메인 던지기** — 아래로 갈수록 정확합니다:
```
핀테크 정산 대시보드 디자인 30개 스타일로 뽑아줘        ← 도메인만
연서, 대화형 원형으로 30 스타일 뽑아줘                  ← 원형 직접 지정
/home/me/myproject 기준으로 디자인 시안 뽑아줘          ← ⭐ 프로젝트 폴더(제일 정확)
```

**3. 갤러리에서 고르기** — 나란히 훑고 마음에 드는 번호를 고르면 끝.

<sub>산출물은 <code>docs/design-gallery/&lt;날짜&gt;-&lt;도메인&gt;/</code> 에 <code>.html</code> 시안 + 비교 갤러리로 쌓입니다.</sub>

---

## 생성 엔진 — Zen Garden 3층 (구축됨)

HTML을 스타일마다 통짜 생성하던 걸 → **DOM 하나 고정(스켈레톤) + CSS 3층**(base·tokens·signature)만 만들어 조립합니다. 콘텐츠 동일성이 **구조적으로 보장**되고(프롬프트로 부탁 안 함), `archetype-lint`는 `coverage-lint`(환각 셀렉터·누락 영역)로 교체됐습니다.

- **tokens 30개는 원형 무관** — A 대시보드·B 대화·D 컬렉션이 같은 파일을 공유. 원형별로 다른 건 스켈레톤·base 각 1개뿐.
- **스타일 1개 추가 = CSS ~2KB** (tokens + 구조적이면 signature), 세 원형 즉시 적용. 클린룸 검증 완료.
- 새 파이프라인 갤러리: [핀테크(A)](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fintech-zen/gallery.html) · [연서(B)](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-yeonseo-zen/gallery.html) · [패션(D)](https://deokjinlog.github.io/design-explosion-30-styles/design-gallery/2026-07-26-fashion-zen/gallery.html)
- 방법서 [`references/3-layer-pipeline.md`](skills/design-style-explorer/references/3-layer-pipeline.md) · 결정·검증 기록 [`docs/design/2026-07-26-zen-garden.md`](docs/design/2026-07-26-zen-garden.md)

**📈 전체 진행 여정 한눈에 보기** → [`docs/progress.html`](https://deokjinlog.github.io/design-explosion-30-styles/progress.html) (세 데모 · 재설계 · 검증 3종 · 3층 구축 · 클린룸 · 커밋 타임라인)

---

## 라이선스

MIT
