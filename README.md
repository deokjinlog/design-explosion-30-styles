<div align="center">

# 🎨 design-kit

### 도메인 하나로, 같은 화면을 **30가지 디자인 스타일**로 — 한 번에.

AI로 디자인 시안을 뽑으면 매번 비슷하게 생기죠.
design-kit 은 **하나의 화면을 30가지 확실히 다른 시각 언어**로 병렬 생성해,
갤러리에서 나란히 비교하며 방향을 정하게 해줍니다.

<br/>

<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-ec4899?style=for-the-badge&labelColor=0d1117">
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude%20Code-Plugin-a78bfa?style=for-the-badge&labelColor=0d1117">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge&labelColor=0d1117">
  <img alt="Language" src="https://img.shields.io/badge/lang-한국어-3b82f6?style=for-the-badge&labelColor=0d1117">
</p>

<p>
  <img alt="Styles" src="https://img.shields.io/badge/styles-30-ec4899?style=flat-square&labelColor=0d1117">
  <img alt="Skill" src="https://img.shields.io/badge/skill-design--style--explorer-06b6d4?style=flat-square&labelColor=0d1117">
  <img alt="Zero deps" src="https://img.shields.io/badge/dependencies-zero-22c55e?style=flat-square&labelColor=0d1117">
</p>

**[▶ 라이브 데모 — 30 스타일 갤러리 보기](https://deokjinlog.github.io/design-kit/)**

</div>

<br/>

---

## 한눈에

- **입력** — 도메인 하나 (예: *"이커머스 셀러 대시보드"*)
- **출력** — 같은 화면 × 30 디자인 스타일 = 30 HTML 시안 + 비교 갤러리
- **핵심** — 콘텐츠는 고정, **시각 언어만 30가지**. 순수하게 디자인만 비교돼요.

<br/>

## 1 분이면 시작

**설치** — Claude Code 안에서:

```
/plugin marketplace add deokjinlog/design-kit
/plugin install design-kit@design-kit
```

**사용** — 말로 부르면 떠요:

```
이커머스 셀러 대시보드 디자인 30개 스타일로 뽑아줘
```

*"디자인 시안 뽑아줘"* · *"30개 스타일로 보여줘"* · *"○○ 도메인 디자인 보여줘"* — 뜻만 통하면 발동. 100% 확실히 하려면 `/design-style-explorer` 로 직접 부르면 돼요.

<sub>산출물은 <code>docs/design-gallery/&lt;날짜&gt;-&lt;도메인&gt;/</code> 에 <code>.html</code> 시안 + 비교 갤러리로 쌓여요.</sub>

<br/>

## 왜 매번 비슷하지 않은가

<table>
<tr>
<td width="50%" valign="top">

**🎨 30개 전용 프롬프트**

각 스타일이 매력 축 · 팔레트(hex) · 타이포 · 시그니처 · **금지 목록** · 크리틱 루프까지 튜닝돼 있어요. 무작위가 아니라 스타일마다 확실히 달라집니다.

</td>
<td width="50%" valign="top">

**⚙️ 실무 품질 자동 보장**

- **린트 게이트** — 스타일별 금지 규칙 자동 검사 (브루탈리즘에 그라디언트 있으면 FAIL → 수정 → 재린트)
- **실무 그라운딩** — 8px 그리드 · 컴포넌트 상태(hover/focus) · CSS 변수 (Linear/Stripe 마감)
- **콘텐츠 견고성** — 큰 숫자 · 긴 제목 · 결측 · 빈 상태로 스트레스 테스트

</td>
</tr>
</table>

<br/>

## 워크플로

```
도메인 → 대표 화면 × 30 스타일 병렬 생성 → 갤러리 비교로 방향 결정
      → 그 방향으로 화면 세트 일관 생성 → 디자인 시스템 역추출
```

30개를 **병렬로 한 번에** 뽑고, iframe 갤러리로 한눈에 비교해요. 방향을 정하면 그 스타일로 나머지 화면을 일관되게 이어가고, 마지막에 디자인 시스템(토큰·규칙)을 역추출합니다.

<br/>

## 30 스타일

**실무 다빈도 (15)** — 트렌디 SaaS · 머티리얼 · 벤토 · 컬러풀 모던 · AI 프로덕트 · 엔터프라이즈 B2B · 핀테크 소프트 · 헬스케어 · 접근성 · 다크 대시보드 · 다크 미니멀 · 데이터 리치 · 공공포털 · 커머스 · 웜 프로

**창조 · 개성 (15)** — SF HUD · 브루탈리즘 · 글래스 · 뉴모 · 클레이 · 오로라 · 럭셔리 다크 · 에디토리얼 · 네이처 · 미니멀 모노 · 스위스 · 맥시멀 · Y2K · 레트로 픽셀 · 터미널

<sub>스타일마다 <code>skills/design-style-explorer/references/prompts/style-NN-*.md</code> 에 전용 프롬프트가 있어요. 무작위가 아니라 각각 튜닝된 지시서예요.</sub>

<br/>

## dj-superkit 과의 관계

design-kit 은 [dj-superkit](https://github.com/deokjinlog/dj-superkit)(프로덕션 코드 워크플로 플러그인) 에서 갈라져 나온 **독립 디자인 도구**예요. 코드를 안전하게 만드는 일과 디자인 방향을 탐색하는 일은 서로 다른 작업이라, 각자의 저장소로 나눴습니다. 둘은 서로 의존하지 않으니 필요한 것만 설치해 쓰면 돼요.

<br/>

---

<div align="center">

**MIT**

<br/>

<sub>버그 / 제안: <a href="https://github.com/deokjinlog/design-kit/issues">GitHub Issues</a></sub>

</div>
