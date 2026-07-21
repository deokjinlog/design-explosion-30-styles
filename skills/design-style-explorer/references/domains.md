# 도메인 프리셋 — "무슨 업종이냐"를 화면 원형으로 옮기는 자리

이 파일은 1단계 콘텐츠 인터뷰의 **출발점**을 준다. 사용자가 "호텔 예약 사이트" 라고 하면 → `Travel > Hotel` 칸에 꽂고 → 그 칸의 **원형 조합·화면 흐름·견고성 포인트**를 초안으로 채운다. `archetypes.md`(원형 11종)의 **위층**이다.

## 이 파일이 주는 것 / 안 주는 것

- **주는 것**: ① 분류 메뉴판(업종 → 칸) ② 그 칸의 원형 조합 추천 ③ 대표 화면 흐름 ④ 도메인 어휘·견고성 포인트
- **안 주는 것**: 화면 자체. **데이터는 "왜 이 원형인가"의 근거일 뿐, 화면은 우리가 HTML 시안으로 만든다.**

## ⚠️ 우선순위 — 프리셋은 출발점이지 정답이 아니다

원형을 정하는 소스는 셋이고, **위가 아래를 이긴다:**

| 순위 | 소스 | 정확도 |
|---|---|---|
| 1 | **repo 역산** (실제 요구사항·코드 `docs/features/**/*requirements.md`, `src/`) | 가장 정확 |
| 2 | **도메인 프리셋** (이 파일) | 출발점 — **덮어쓸 수 있음** |
| 3 | 4문항 인터뷰 (`archetypes.md`) | 프리셋도 없을 때 |

> **프리셋이 원형을 강제하면 안 된다.** "핀테크는 항상 대시보드" 로 굳으면, 대화형이 주인 핀테크 제품이 왔을 때 [원형 오이식 사고](archetypes.md)를 반복한다. 프리셋을 보여준 뒤 **"이 원형 맞나요?"** 를 1단계 인터뷰로 반드시 확인한다.

## 출처와 검증 (근거 있는 프리셋)

아래 §1 표는 임의 분류가 아니라 **[Mind2Web](https://osu-nlp-group.github.io/Mind2Web/)** (NeurIPS'23, CC BY 4.0) 데이터에서 직접 집계했다.

- 웹 에이전트 벤치마크. **136개 실제 사이트**(SimilarWeb 미국 인기순위 상위) × **2,022개 사람 주석 태스크** × 평균 **7.0 액션 스텝**.
- 분류체계: **5 상위 × 31 (상위,하위) 쌍** (`General` 이 Travel·Shopping 양쪽에 있어 하위 이름은 30개). 논문의 31과 일치.
- 추출: `osunlp/Multimodal-Mind2Web` 4 split(train/test_domain/test_task/test_website)의 parquet 메타 컬럼만 읽음(전체 22GB 중 수 MB). **Information·Service 도 test_domain split 에 공개**돼 있어 전량 확보 — 별도 암호 zip 불필요.
- **원형 시퀀스 = `confirmed_task` 텍스트의 행동 동사 분포**(선두 "Find/Search" 관행어는 편향 보정으로 제거). 각도 신호이지 절대 빈도가 아니다.

## §1. 데이터 근거 프리셋 (31칸) — Mind2Web 집계

원형 시퀀스 코드: **H** 검색·결과 · **D** 컬렉션 · **E** 폼·입력 · **C** 읽기 · **K** 프로필·설정 · **F** 피드 · **A** 대시보드 (→ `archetypes.md` A~K).
"화면 수" 는 평균 스텝(≈7)에서 도출한 프리셋 규모 추정치.

| 상위 | 하위 | 원형 흐름(주→보조) | 화면 | 태스크 | 사이트 | 대표 사이트 |
|---|---|---|---|---|---|---|
| Travel | **Other**(주차·투어·공원) | D → E → K | ~4 | 132 | 8 | spothero, recreation.gov, viator, sixflags |
| Travel | **Airlines** | E → D → A | ~6 | 131 | 7 | aa, united, delta, jetblue, kayak |
| Travel | **Restaurant** | D → E → K | ~5 | 91 | 5 | resy, yelp, tripadvisor, exploretock |
| Travel | **Ground**(기차·버스) | E → C → D | ~5 | 84 | 5 | amtrak, thetrainline, megabus, mbta |
| Travel | **General**(OTA) | D → E → C | ~6 | 64 | 5 | booking, expedia, agoda, trip |
| Travel | **Car rental** | E → D → C | ~6 | 55 | 3 | enterprise, budget, rentalcars |
| Travel | **Hotel** | D → E → A | ~6 | 41 | 3 | marriott, airbnb, koa |
| Shopping | **Speciality**(약국·가구·서점) | D → E → K | ~5 | 111 | 7 | cvs, ikea, rei, cabelas, gamestop |
| Shopping | **Auto**(차 거래) | D → E → K | ~6 | 79 | 5 | cargurus, carmax, tesla, kbb |
| Shopping | **General**(종합몰) | D → E → K | ~5 | 72 | 5 | amazon, ebay, target, instacart |
| Shopping | **Digital**(전자제품) | D → K → E | ~5 | 52 | 3 | apple, bestbuy, newegg |
| Shopping | **Fashion** | D → E → C | ~5 | 35 | 2 | uniqlo, underarmour |
| Shopping | **Department**(백화점) | D → K → E | ~4 | 31 | 2 | macys, kohls |
| Service | **Health** | D → C → K | ~4 | 112 | 8 | webmd, zocdoc, mayoclinic, healthline |
| Service | **Government** | C → E → D | ~3 | 75 | 5 | gov.uk, ca.gov, dmv.virginia.gov |
| Service | **Home service** | D → E → C | ~4 | 44 | 3 | thumbtack, craigslist, bbb.org |
| Service | **Pet**(입양) | D → C → F | ~5 | 42 | 3 | petfinder, adoptapet, akc.org |
| Service | **Shipping** | E → A → F | ~4 | 34 | 3 | ups, usps, fedex |
| Service | **Moving** | E → D | ~5 | 23 | 2 | uhaul, extraspace |
| Info | **Social media** | F → D → K | ~3 | 64 | 5 | linkedin, reddit, twitter, pinterest |
| Info | **Job** | E → D → C | ~4 | 64 | 5 | indeed, glassdoor, careers.walmart |
| Info | **Housing**(부동산) | D → E → A | ~5 | 62 | 5 | redfin, apartments, movoto, landwatch |
| Info | **Education** | D → C → E | ~3 | 56 | 5 | coursera, udemy, osu.edu, usnews |
| Info | **Finance** | A → F → D | ~3 | 52 | 3 | finance.yahoo, coinmarketcap |
| Info | **Weather** | A → C | ~3 | 35 | 3 | accuweather, weather, theweathernetwork |
| Info | **Cooking**(레시피) | C → F → D | ~3 | 31 | 3 | allrecipes, cookpad, epicurious |
| Entertainment | **Event**(티켓) | D → E → C | ~4 | 79 | 5 | seatgeek, stubhub, eventbrite |
| Entertainment | **Music** | D → A → F | ~4 | 76 | 5 | last.fm, soundcloud, discogs |
| Entertainment | **Sports** | E → D → A | ~3 | 75 | 5 | espn, foxsports, nfl, nba |
| Entertainment | **Movie** | D → E → K | ~3 | 74 | 5 | imdb, rottentomatoes, amctheatres |
| Entertainment | **Game** | D → K → C | ~3 | 46 | 3 | store.steampowered, ign, boardgamegeek |

**읽는 법 — 큰 패턴 셋:**
- **거래형**(Travel·Shopping 대부분, Service 예약): `H 검색 → D 컬렉션(결과·필터) → E 폼(예약·결제)`. 이 셋의 원형이 **화면 흐름**을 만든다.
- **정보형**(Cooking·Education·Weather·Government): `C 읽기`·`D 컬렉션` 이 주. 차트·KPI가 아니라 **본문·목록 타이포**가 승부처.
- **소셜·금융**(Social media·Finance): `F 피드`·`A 대시보드`. 거래형과 완전히 다른 화면.

## §2. 갭 — 데이터에 없어 수동으로 정의 (근거 없음, 커버리지용)

Mind2Web 은 **로그인 없이 접근 가능한 공개 소비자 웹**만 담는다. 그래서 아래는 **데이터 근거가 없다** — 우리 지식으로 정의하되 그 사실을 명시한다. (사용자가 이 업종이면, 프리셋을 약하게 제시하고 1단계 인터뷰에 더 기댄다.)

| 도메인(수동) | 대표 원형 | 왜 데이터에 없나 |
|---|---|---|
| **B2B SaaS / 분석·백오피스** | A 대시보드 (주) + K 설정 + E 폼 | 로그인 뒤 업무 화면이라 크롤 불가 |
| **개발자 도구** | G 에디터·캔버스 + A 대시보드 | 콘솔·IDE, 공개 태스크 없음 |
| **금융 백오피스 / 뱅킹** | A 대시보드 + E 폼 + K 설정 | 인증 벽 안 |
| **대화형 AI 제품** | B 대화형 (주) + C 읽기 | 벤치마크 대상 아님 (이 스킬의 원형 오이식 사고가 난 그 유형) |
| **협업 문서·노트** | G 에디터·캔버스 + F 피드 | 로그인 뒤 |
| **온보딩·인증** | I 온보딩 / J 인증 | Mind2Web 은 태스크 중간 화면이라 첫 진입·로그인 흐름이 드묾 (단 [Enrico](https://github.com/luileito/enrico) 에서 Tutorial·Login 이 2·3위라 원형 근거는 있음 — `archetypes.md` 참조) |

## §3. 시각 레퍼런스 (내부 참고용, 사용자 노출 금지)

`osunlp/Multimodal-Mind2Web` 에 각 태스크 페이지의 **실제 사이트 스크린샷**이 정렬돼 있다(train 7,775 액션). "이 도메인 화면이 실제로 어떻게 생겼나" 를 원형 설계 시 **내부 참고**로만 본다 — 저작권·품질 때문에 사용자에게 그대로 보여주지 않는다.

## §4. 한계 (정직하게)

- Mind2Web 목적은 *웹 에이전트 학습*이지 디자인 카탈로그가 아니다. 원형 시퀀스는 태스크 텍스트에서 역산한 **근거**지 화면 명세가 아니다.
- **B2C 공개 웹 편향** — §2 의 업무용·인증 뒤 화면은 통째로 없다.
- 스크린샷은 저작권물 — 참고만.
- 프리셋 화면 수(~3~6)는 평균 7 스텝에서 도출한 추정치. 실제 화면 수는 1단계에서 확정한다.
