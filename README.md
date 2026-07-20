<p align="center">
  <img src="https://raw.githubusercontent.com/deokjinlog/design-explosion-30-styles/main/docs/banner.svg" alt="design-explosion — 하나의 화면을 30가지 디자인 스타일로" width="100%">
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-1.1.0-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Plugin-a78bfa?style=flat-square&labelColor=0d1117">
  <img alt="Styles" src="https://img.shields.io/badge/styles-30-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22c55e?style=flat-square&labelColor=0d1117">
  <img alt="Zero deps" src="https://img.shields.io/badge/dependencies-zero-22c55e?style=flat-square&labelColor=0d1117">
</p>

<p align="center">
  <b><a href="https://deokjinlog.github.io/design-explosion-30-styles/">라이브 데모 — 30 스타일 갤러리 열어보기</a></b>
</p>

<br/>

> ## 막연한 "예쁘게 해줘"를, 30가지 확실히 다른 방향으로
>
> 도메인 하나만 던지면 **같은 화면을 30가지 디자인 스타일로 폭발**시킵니다.
> 콘텐츠는 고정하고 **시각 언어만 30갈래**로 벌려서, 갤러리에서 나란히 보고 방향을 고릅니다.
>
> <sub><i>Turns a vague "make it nice" into 30 concrete design directions — same content, 30 visual languages, side by side.</i></sub>

---

## 두 개의 축 — 스타일 × 메시지

이 플러그인에는 **스킬 두 개**가 들어 있습니다. 랜딩 하나를 만들려면 결정이 둘이거든요.

| 스킬 | 축 | 무엇을 30갈래로 | 언제 |
|---|---|---|---|
| **design-style-explorer** | 어떻게 **보이나** | 30가지 디자인 스타일 | 비주얼 방향이 안 정해질 때 |
| **copy-angle-explorer** | 뭐라고 **말하나** | 30가지 메시지 각도 (6패밀리) | "뭐라고 소개할지" 막힐 때 |

> **스타일 × 메시지 = 랜딩 완성.** 카피를 먼저 고르고 스타일을 입히거나, 반대로 해도 됩니다.

두 스킬 모두 같은 규율을 씁니다 — **한 변수만 바꾼다.** 스타일 탐색에선 콘텐츠를 고정하고, 카피 탐색에선 제품 사실을 고정합니다. 그래야 비교가 정직합니다.

그리고 각각 **자동 게이트**가 붙어 있습니다:

- `style-lint` — 그 스타일의 금지를 어겼나
- `archetype-lint` — **이 도메인의 화면이 맞나** (대화형 제품에 KPI·도넛이 박히는 사고를 잡습니다)
- `copy-lint` — 제품 사실에 없는 수치·최상급을 지어냈나

---

## 이런 적 있죠?

새 화면 디자인 방향을 잡아야 하는데 —

- AI에게 "예쁘게 디자인해줘" 하면 **매번 비슷한 톤** 한두 개만 나오고,
- "다른 느낌으로" 몇 번 더 시켜도 결국 **거기서 거기**,
- 좋은 방향인지 아닌지는 **머릿속으로 상상**해서 비교해야 하고,
- 막상 뽑아보면 큰 숫자 · 긴 제목 들어가는 순간 **레이아웃이 무너지고** …

이 도구는 그걸 **30갈래로 강제로 벌려놓고 눈으로 비교**하게 만듭니다.

---

## 뭐가 다른가요?

| | 그냥 AI에게 "디자인 해줘" | design-explosion |
|---|---|---|
| **결과** | 매번 비슷한 톤 1~2개 | 확실히 다른 **30가지** |
| **비교** | 머릿속으로 상상 | **갤러리에서 나란히** |
| **일관성** | 스타일마다 될 때도 안 될 때도 | **린트 게이트**로 매번 규칙 준수 |
| **콘텐츠** | 예쁜 더미데이터만 | 큰 숫자 · 긴 제목 · 빈 상태 **스트레스 테스트** |
| **다음 단계** | 마음에 안 들면 처음부터 | 방향 골라 **세트 생성 → 디자인 시스템** |

---

## 3단계로 시작

**1. 설치** — Claude Code 안에서:

```
/plugin marketplace add deokjinlog/design-explosion-30-styles
/plugin install design-explosion-30-styles@design-explosion-30-styles
```

**2. 도메인 던지기** — 말로 부르면 떠요:

```
이커머스 셀러 대시보드 디자인 30개 스타일로 뽑아줘
```

**3. 갤러리에서 고르기** — 30개가 한 번에 나오면, 나란히 훑고 마음에 드는 번호를 고르면 끝.

<sub>스크린샷이 아니라 살아있는 화면이에요. 시안마다 따로 렌더해서 서로 CSS가 안 섞이고, 실제 데스크톱 크기 그대로 비교됩니다.</sub>

> *"디자인 시안 뽑아줘"* · *"30개 스타일로 보여줘"* · *"○○ 도메인 디자인 보여줘"* — 뜻만 통하면 발동해요. 100% 확실히 하려면 `/design-style-explorer` 로 직접 부르면 됩니다.

<sub>산출물은 <code>docs/design-gallery/&lt;날짜&gt;-&lt;도메인&gt;/</code> 에 <code>.html</code> 시안 + 비교 갤러리로 쌓여요.</sub>

---

## 왜 30개가 다 다른가 (무작위가 아니에요)

AI는 그냥 두면 자기가 편한 톤으로 수렴해요. 이 도구는 스타일마다 **각본**을 박아둡니다.

- **스타일당 전용 프롬프트** — 매력 축 · 팔레트(hex) · 타이포 · 시그니처 · 금지 목록 · 크리틱 루프까지. 무작위가 아니라 각각 튜닝된 지시서예요.
- **린트 게이트** — "브루탈리즘인데 그라디언트?" 같은 반칙을 코드가 자동으로 잡아서 FAIL → 수정 → 다시 그려요. 30개를 사람이 일일이 눈으로 검수하지 않아도 됩니다.
- **실무 마감** — 8px 그리드 · hover/focus 상태 · CSS 변수. Linear · Stripe 볼 때 그 촘촘한 느낌.
- **최악 콘텐츠 테스트** — 긴 제목 · 큰 숫자 · 결측 · 빈 상태를 넣어도 안 무너지게. 템플릿은 베스트 케이스를 팔지만, 실제로 쓸 땐 최악 콘텐츠가 들어오니까요.

<sub>린트는 "이 스타일이 맞나"(3초 무드)를, 최악 콘텐츠 테스트는 "오래 써도 안 무너지나"(견고성)를 봅니다. 둘은 직교하는 두 축이라, 둘 다 통과해야 진짜 쓸 만한 시안이에요.</sub>

---

## 이렇게 흘러가요

```
도메인 → 대표 화면 × 30 스타일 (병렬 생성) → 갤러리에서 방향 결정
      → 그 방향으로 나머지 화면 일관 생성 → 디자인 시스템(토큰 · 규칙) 역추출
```

먼저 **한 화면을 30가지로** 뽑아 방향을 정하고, 정해지면 그 스타일로 나머지 화면을 이어가요.
마지막엔 색 · 간격 · 컴포넌트 규칙을 **디자인 시스템으로 역추출**해서, 이후 화면은 그 규칙대로 찍어냅니다.

---

## 30가지 스타일

**실무 다빈도 (15)**
트렌디 SaaS · 머티리얼 · 벤토 · 컬러풀 모던 · AI 프로덕트 · 엔터프라이즈 B2B · 핀테크 소프트 · 헬스케어 · 접근성 · 다크 대시보드 · 다크 미니멀 · 데이터 리치 · 공공포털 · 커머스 · 웜 프로

**창조 · 개성 (15)**
SF HUD · 브루탈리즘 · 글래스 · 뉴모 · 클레이 · 오로라 · 럭셔리 다크 · 에디토리얼 · 네이처 · 미니멀 모노 · 스위스 · 맥시멀 · Y2K · 레트로 픽셀 · 터미널

<sub>스타일마다 <code>skills/design-style-explorer/references/prompts/style-NN-*.md</code> 에 전용 프롬프트가 있어요.</sub>
