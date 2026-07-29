# 30 스타일 정본 재접지 — 출처·서체·차별화 축

> **문제**: 갤러리 30장 중 ~18장이 "그냥 흰 배경"으로 뭉개져 보임.
> **진단**: 세 축이 동시에 붕괴 — ① 웹폰트 미로드로 28종이 시스템 폴백 **한 서체**로 렌더 ② 절반이 *디자인 언어*가 아니라 *산업 라벨*(헬스케어·핀테크·엔터프라이즈…)이라 참조할 규칙이 없어 기본값(흰 배경+둥근 카드+인디고+Inter)으로 수렴 ③ 변화 준 두 축(라운드·색)이 하필 변별력 최하위.
> **처방**: 서체 전면 교체(제일 싸고 8할) + 산업 라벨 10종을 출처 있는 디자인 언어/시스템으로 교체 + 타입스케일·배경 틴트 다변화 + 구조 시그니처.

날짜: 2026-07-26 · 관련 [Zen Garden 3층 전환](2026-07-26-zen-garden.md)

---

## 차별화가 갈리는 축 (변별력 순)

| 축 | 흰 배경 변별력 | 재접지 전 | 재접지 후 |
|---|---|---|---|
| **서체** | ★★★★★ | 시스템 폴백 1~2종(웹폰트 미로드) | **22종 실로드** |
| **타입스케일** | ★★★★★ | 거의 균일 | 11종(1.125~1.618) |
| **배경 틴트** | ★★★★☆ | 거의 #fff | 어두움 8·중간 1·밝음 22(창백흰색은 대폭 축소) |
| **보더 처리** | ★★★★☆ | 1px 회색 | 0px 하드~4px 격자~검정 블록 |
| **밀도** | ★★★★☆ | 8px 고정 | 밀집(Ant/Carbon)~여백형(Braun) |
| 엘리베이션 | ★★★☆☆ | 소프트 섀도 | 하드섀도·토널·뉴모 이중섀도 |
| 그리드 | ★★★☆☆ | 대칭 | 비대칭(스위스)·격자(De Stijl) |
| 라운드 | ★★☆☆☆ | ✅ 변화 | 유지 |
| 액센트 색 | ★☆☆☆☆ | ✅ 변화 | 유지 |

---

## 두 계열의 출처

**A. 실제 스펙이 공개된 디자인 시스템** — 토큰·그리드·타이포가 문서화돼 있어 그대로 접지 가능.

- IBM Carbon — radius 0 · IBM Plex · 2px 하드 그리드 · <https://carbondesignsystem.com/>
- Material Design 3 — 토널 팔레트 · radius 16~28 · 엘리베이션 5단 · Roboto · <https://m3.material.io/styles/typography/>
- GOV.UK — Public Sans · 노란 포커스링 · radius 0 · 검정 · <https://design-system.service.gov.uk/styles/>
- Ant Design — 초고밀도 · #1677ff · 작은 폰트 · radius 2 · <https://ant.design/>
- Shopify Polaris — 회색 계단 · radius 8 · 카드 보더 · #008060 · <https://polaris.shopify.com/>
- shadcn/ui — zinc 중립 · radius 8 · Inter · <https://ui.shadcn.com/>
- 카탈로그 88종 · <https://www.designsystems.one/>

**B. 디자인 운동** (규칙이 문서화 → 흰 배경에서도 구분).

- International Typographic Style(스위스) — Helvetica/Akzidenz-Grotesk · 비대칭 그리드 · 좌측정렬 우측흘림 · <https://en.wikipedia.org/wiki/International_Typographic_Style>
- Bauhaus — 원/삼각/사각 · 빨강·노랑·파랑 원색 · radius 0 · <https://en.wikipedia.org/wiki/Bauhaus>
- De Stijl / 몬드리안 — 검은 굵은 격자선 + 원색 블록 · <https://en.wikipedia.org/wiki/De_Stijl>
- Memphis — 충돌 색 · 지그재그 · 테라조 · <https://aesthetics.fandom.com/wiki/Memphis_Design>
- Neubrutalism — 굵은 검은 보더 + 오프셋 하드섀도 · <https://www.nngroup.com/articles/neobrutalism/>
- Editorial — 큰 디도네 세리프(Playfair) · 2단 · 드롭캡
- Risograph — 한정 스팟컬러 2~3 · mix-blend multiply · 미스레지스트레이션

**C. 실물 갤러리** — [CSS Zen Garden](http://www.csszengarden.com/)(하나의 HTML로 218 디자인, 이 파이프라인의 원조) · [Typewolf](https://www.typewolf.com/)(실사이트 폰트 조합) · [Fonts In Use](https://fontsinuse.com/) · Awwwards/Godly/Land-book.

---

## 30 스타일 최종 스펙 (재접지)

산업 라벨 → 출처 있는 이름으로 바뀐 10종은 **★** 표시. 서체는 전부 Google Fonts 실로드(GitHub Pages 렌더 확인).

| # | 이름 | 계열/출처 | 본문 서체 | 타입스케일 | 배경 | 라운드 |
|---|---|---|---|---|---|---|
| 01 | SF HUD | Sci-fi HUD | Rajdhani/Orbitron | 1.3 | #050810 다크 | 0 |
| 02 ★ | GOV.UK 공공 | GOV.UK Design System | Public Sans | 1.2 | #FFFFFF | 0 |
| 03 ★ | shadcn/ui | shadcn/ui | Inter | 1.2 | #FFFFFF zinc | 8 |
| 04 | 밀집 터미널 | 터미널/등폭 | IBM Plex Mono | 1.15 | #0A0C10 다크 | 0 |
| 05 ★ | Neubrutalism | Neubrutalism(NN/g) | Space Mono/Archivo Black | 1.4 | #FFFFFF+검정 | 0 |
| 06 | 글래스모피즘 | Glassmorphism | Poppins | 1.25 | #7C3AED | 22 |
| 07 ★ | Braun 미니멀 | Dieter Rams | Archivo | 1.5 | #F4F4F2 | 0 |
| 08 | 럭셔리 다크 | 고대비 세리프 | Cormorant Garamond | 1.6 | #0E0D0B 다크 | 6 |
| 09 | 레트로 픽셀 | VT320 비트맵 | VT323/DungGeunMo | 1.2 | #1A1C2C 다크 | 0 |
| 10 | 에디토리얼 | 매거진 디도네 | Playfair Display | 1.618 | #FAF7F2 크림 | 0 |
| 11 | 네이처 오가닉 | 옵티컬 세리프 | Fraunces | 1.4 | #F4F1E8 세이지 | 28 |
| 12 | 뉴모피즘 | Neumorphism | Nunito | 1.25 | #E4E9F2 회색 | 18 |
| 13 | 오로라 | 그라디언트 다크 | Space Grotesk | 1.3 | #0A0A12 다크 | 18 |
| 14 | 벤토 | 벤토 그리드 | Sora | 1.25 | #F4F4F5 | 22 |
| 15 | 클레이모피즘 | Claymorphism | Fredoka/Jua | 1.3 | #F4F1FF 라일락 | 32 |
| 16 ★ | Material 3 | Material Design 3 | Roboto | 1.25 | #FEF7FF 토널 | 16 |
| 17 | Y2K | Memphis/Y2K | Chakra Petch | 1.35 | #1A0B2E 다크 | 14 |
| 18 | 스위스 | Int'l Typographic Style | Archivo/Helvetica | 1.5 | #FFFFFF+빨강 | 0 |
| 19 | 맥시멀리즘 | 라우드 디스플레이 | Space Grotesk/Bungee | 1.5 | #FFF8E7 | 20 |
| 20 | 다크 애널리틱스 | 데이터 대시보드 | IBM Plex Sans | 1.15 | #0d1117 다크 | 6 |
| 21 ★ | Riso 인쇄 | Risograph | Work Sans/Syne | 1.3 | #F3EEE6 뉴스프린트 | 0 |
| 22 ★ | De Stijl | De Stijl/몬드리안 | Archivo | 1.4 | #F5F2E9+검정격자 | 0 |
| 23 ★ | IBM Carbon | IBM Carbon | IBM Plex Sans | 1.2 | #FFFFFF 하드 | 0 |
| 24 ★ | Bauhaus | Bauhaus | Poppins/Bungee | 1.45 | #F2EFE6+원색 | 0 |
| 25 ★ | Shopify Polaris | Shopify Polaris | Inter | 1.2 | #F6F6F7 회색계단 | 8 |
| 26 | 다크 미니멀 | 정갈 그로테스크 | Inter | 1.4 | #0E0E11 다크 | 10 |
| 27 | 웜 프로 | 옵티컬 세리프 | Newsreader | 1.5 | #FAF6F0 웜크림 | 14 |
| 28 | 접근성 | Atkinson Hyperlegible | Atkinson Hyperlegible | 1.3 | #FFFFFF 고대비 | 8 |
| 29 ★ | Memphis | Memphis 80s | Fredoka/Righteous | 1.35 | #FDF3E7+충돌색 | 12 |
| 30 ★ | Ant Design 밀집 | Ant Design | Inter 소형 | 1.125 | #FFFFFF 밀집 | 2 |

---

## 구조 시그니처 계획 (기계 검사 가능한 규칙)

서체·스케일·틴트로 살아난 뒤에도 "흰 배경 계열"이 구조로 갈리려면 원형별 signature(구조 override)가 필요. 각 스타일은 **시그니처 3~5개 + forbidden(금지)** 로 정의:

| 스타일 | signature (필수) | forbidden (금지) |
|---|---|---|
| IBM Carbon | `border-radius:0` 예외없음 · IBM Plex · 2px 하드 보더 | 둥근 모서리 · 소프트 SaaS 섀도 |
| Ant 밀집 | 폰트 12~13px · 행높이 32px · radius:2 | 넉넉한 여백 · 큰 폰트 |
| Material 3 | radius 16~28 · 토널 서피스 틴트 · 엘리베이션 5단 | 하드 엣지 · 보더만으로 구분 |
| De Stijl | 검은 4px 격자선 + 빨강/노랑/파랑 블록 | 회색 보더 · 파스텔 |
| Bauhaus | 원·삼각·사각 도형 · 원색 3 · radius:0 | 그라디언트 · 둥근 카드 |
| Memphis | 충돌 4색 · 지그재그/테라조 · 회전 | 정렬된 대칭 그리드 |
| Neubrutalism | `border:3px solid #000` · `box-shadow:6px 6px 0 #000` | 1px 회색 보더 · blur 섀도 |
| Riso | 스팟 2색 · `mix-blend-mode:multiply` · 오프셋 | 풀컬러 사진 · 그라디언트 |
| 에디토리얼 | Playfair 디스플레이 대형 · 2단 · 드롭캡 | 산세리프 본문 |

**진행 상태**: 서체·스케일·틴트·팔레트 재접지 = **완료**. 원형 D 구조 signature = **21/30 완료** — 01·02·04·05·06·09·10·12·14·15·16·17·18·19·21·22·23·24·28·29·30 (SF HUD·GOV.UK·터미널·Neubrutal·글래스·픽셀·에디토리얼·뉴모·벤토·클레이·Material 3·Y2K·스위스·맥시멀·Riso·De Stijl·Carbon·Bauhaus·접근성·Memphis·Ant). 나머지 9종(03 shadcn·07 Braun·08 럭셔리·11 오가닉·13 오로라·20 다크애널·25 Polaris·26 다크미니멀·27 웜프로)은 토큰전용 — 원래 저구조(미니멀·다크서브틀·세리프웜) 사조라 서체·팔레트·스케일로 충분히 차별. 산업 라벨 12종 prompt MD엔 정체성 갱신 노트 삽입(정본=tokens+signature+본 문서).

**원형 확장(2026-07-27)**: D(21/30)에 이어 A(대시보드)·B(대화)에도 구조 signature 저작 —
- **A 6종**(fintech-zen): IBM Carbon(1px 하드그리드로 KPI/차트 봉합)·Material 3(토널4단·엘리베이션5단)·Ant(밀집)·Neubrutal(하드섀도 KPI)·Swiss(1px헤어라인 12열·비대칭 6·2·2·2·빨강1점)·De Stijl(검은 격자·원색블록).
- **B 12종**(yeonseo-zen): 기존 04·05·07·09·10·18 + 신규 06 Glass(프로스티드 버블)·12 Neu(볼록/함몰 버블)·15 Clay(통통 버블)·16 Material 3(me=primary container)·23 Carbon(각진 2px 버블)·30 Ant(밀집).
- Material 3·Carbon·Ant는 D·A·B 3원형에 **같은 토큰 어휘**(m3-surf/elevation, 1px 하드그리드, 밀집)로 일관 저작 — 한 사조가 원형 넘어 정체성 유지.

## 검증

- Google Fonts 실로드: 4개 갤러리 × 30장 = **120/120** `<link>` 주입 확인.
- coverage-lint: **120/120 PASS**(환각 셀렉터 0).
- body 바이트 동일: 갤러리별 30/30 유지(폰트 `<link>`는 head, DOM 불변).
- 회색조 테스트: 헤드리스 렌더러 부재로 토큰 휘도 프록시로 대체 — 서체 22종은 desaturate에도 살아남는 축.
