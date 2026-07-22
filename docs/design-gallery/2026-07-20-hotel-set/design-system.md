# 여기묵자 디자인 시스템 — STYLE 03 · 트렌디 SaaS

역추출 대상: `screen-1-search.html`(검색 결과) · `screen-2-booking.html`(예약 폼) · `screen-3-mybookings.html`(내 예약/설정).
이 문서 하나만으로 같은 제품의 **새 화면**을 만들 수 있도록, 3개 파일에 실제로 존재하는 값만 기록한다.
원본 스타일 지시서(`references/prompts/style-03-trendy-saas.md`)의 팔레트·타이포·금지 규칙과 대조해 이탈 여부도 함께 표시했다.

---

## 1. 기술 스택 / 기본 전제

- **단일 HTML 파일** — HTML/CSS/JS 전부 인라인, 외부 의존성은 폰트 CDN 하나뿐.
- 한글 폰트: Pretendard CDN
  `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css`
  `font-family:'Pretendard',-apple-system,BlinkMacSystemFont,sans-serif;`
- **JS는 연출 전용이다.** 카운트업, 로드 스태거, 필터/정렬, 토글, 흔들림 애니메이션 — 전부 JS가 실패해도
  HTML만으로 완결된 화면이 유지되어야 한다 (단, screen-1의 카운트업은 이 원칙을 어긴 실제 반례이니 §6 참고).
- `prefers-reduced-motion: reduce` 대응 필수 — 3개 파일 모두 아래 블록을 그대로 갖고 있다:
  ```css
  @media (prefers-reduced-motion: reduce){
    *{animation:none !important;transition:none !important;}
    .reveal{opacity:1;transform:none;}
  }
  ```
  JS도 `matchMedia('(prefers-reduced-motion: reduce)').matches`를 읽어 카운트업·흔들림을 즉시 최종 상태로 스킵한다.
- **반응형 분기점: 900px** — 그리드 레이아웃이 1열로 접힌다. 보조 분기점 560px(screen-1/2) / 480px(screen-3)에서
  `.live-chip` 등 부가 텍스트를 추가로 숨긴다.
- 숫자에는 항상 `.tabnum { font-variant-numeric: tabular-nums; font-feature-settings:"tnum" 1; }`.
- 최대 폭: `max-width:1200px; margin:0 auto;` (topbar-inner, layout 공통).
- 푸터 하단에 `STYLE 03 · 트렌디 SaaS` 고정 표기.
- `*{box-sizing:border-box;}`, 기본 폰트 크기 `14px`, `line-height:1.5`, `-webkit-font-smoothing:antialiased`.

---

## 2. 디자인 토큰

### 2-1. 컬러 (3개 파일 CSS 변수 원문 그대로)

```css
:root{
  --bg:#FBFAFF;
  --violet:#7C5CFF;
  --pink:#FF8FC0;
  --mint:#5EE6C8;
  --ink:#17143A;
  --muted:#7B7897;        /* 장식용 보조색 (배지/보더 등, 텍스트 4.5:1 미보장) */
  --muted-text:#615D82;   /* 본문/캡션용 보조 텍스트 — 배경 대비 5.9:1 */
  --border:#EAE7F6;
  --surface:#FFFFFF;

  --success-bg:#E3FBF3; --success-fg:#137A56;
  --warning-bg:#FFF3DE; --warning-fg:#9A5B00;
  --neutral-bg:#EDEBFB; --neutral-fg:#4B4570;
  --danger-bg:#FDE8ED;  --danger-fg:#C81E45;

  /* screen-2-booking.html 에만 존재 — 포커스 상태 전용 */
  --info-bg:#EFEAFF;    --info-fg:#5B3DDB;
}
```

**배경·표면·텍스트 3단계**
| 단계 | 변수 | 값 | 용도 |
|---|---|---|---|
| 배경(L0) | `--bg` | `#FBFAFF` | 페이지 바탕, 블롭이 깔리는 층 |
| 표면(L1) | `--surface` | `#FFFFFF` | 카드·패널·인풋 배경 |
| 텍스트 1차 | `--ink` | `#17143A` | 제목·본문·값(value) |
| 텍스트 2차 | `--muted-text` | `#615D82` | 캡션·보조 설명·라벨 — **본문에 쓸 수 있는 유일한 회색** |
| 텍스트 금지 | `--muted` | `#7B7897` | 배지/보더 등 **장식 전용**, 텍스트로 쓰지 않는다 |

> **대비 보정 이력**: 원래 하나였던 회색 보조색을 텍스트용(`--muted-text`, 배경 대비 5.9:1)과
> 장식용(`--muted`, 대비 미보장)으로 **의도적으로 분리**했다. `--muted`를 본문·캡션에 쓰면 WCAG AA(4.5:1)를
> 못 넘길 수 있으므로, 사람이 읽는 텍스트에는 반드시 `--muted-text`만 쓴다. 이 분리를 되돌리지 말 것.

**상태 4종 (배경/텍스트 페어) + 포커스 확장(1/3 파일)**
| 상태 | 배경 | 텍스트 | 의미 | dot-pulse 적용 |
|---|---|---|---|---|
| success | `#E3FBF3` | `#137A56` | 예약가능·완료·긍정 | 아니오 |
| warning | `#FFF3DE` | `#9A5B00` | 마감임박·결제대기 (긴급/대기) | **예** |
| neutral | `#EDEBFB` | `#4B4570` | 무료취소·이용완료 (정보성/종결) | 아니오 |
| danger | `#FDE8ED` | `#C81E45` | 단독특가·취소·에러 | 아니오 |
| info (screen-2만) | `#EFEAFF` | `#5B3DDB` | 입력 필드 포커스 플래그 전용 | 아니오 |

**그라디언트**: 바이올렛→핑크 한 방향(`linear-gradient(90deg,var(--violet),var(--pink))` 또는 `135deg`)만 쓴다.
무지개·다색 그라디언트는 금지(§5). 로고 텍스트, 아바타, `.btn-primary`, 활성 페이지네이션, 슬라이더 트랙,
완료된 스텝 서클, 켜진 토글 스위치에 전부 이 한 방향 그라디언트만 재사용된다.

### 2-2. 타이포 스케일 (3개 파일에서 실사용된 값만)

| px | 용도(대표 예) | weight | letter-spacing | line-height |
|---|---|---|---|---|
| 10px | 상태 플래그(`.state-flag`) | 800 | .02em | — |
| 11px | 챕서머리 에이브로우(`.summary-eyebrow`), 배지(`.badge`), 스텝 서브라벨 | 800 | .04em (uppercase) | — |
| 12px | 캡션·위치(`.card-loc`), 필터 카운트, 배지, 빈상태 힌트 | 600–800 | — | — |
| 13px | 칩·버튼·체크박스 라벨·본문 대다수 | 600–800 | — | 1.5(기본) |
| 14px | 바디 기본, 인풋/셀렉트, 네비 아이템 | 500–700 | — | 1.5(기본), 1.6(textarea) |
| 16px | 카드명(`.card-name`), 프로필 통계 라벨, row-label | 700–800 | -0.01em | 1.35 |
| 18px | 폼 섹션 타이틀, 요약 카드 호텔명, 가격(`.card-price`) | 800 | -0.01em | 1.35 |
| 20px | 프로필 이름 | 800 | -0.02em | — |
| 24px | 로고, 결과 타이틀(`.results-title`), 통계값(`.stat-value`) | 800 | -0.02em | — |
| 28px | 총 결제 금액(`.summary-total-value`) | 800 | -0.03em | — |

- weight 팔레트는 4단계: **500(부드러운 본문/placeholder) · 600(캡션·보조 라벨) · 700(본문 강조·버튼) · 800(제목·수치·배지)**.
- letter-spacing은 큰 글자일수록 더 조인다: 16~18px대 `-0.01em` → 20~24px `-0.02em` → 28px(최대 수치) `-0.03em`.
  캡션류의 uppercase 텍스트(`.summary-eyebrow`)만 반대로 `.04em` 벌린다.
- 원본 스타일 지시(`style-03-trendy-saas.md`)는 "KPI 수치 38px 이상"을 요구하지만, 실제 3개 파일에서 가장 큰 수치는
  28px(총 결제 금액)이다 — **호텔 예약 도메인에서는 38px급 KPI가 없으므로 28px를 최댓값으로 채택**한다.
  대시보드형 화면을 새로 만들 때만 38px 규칙을 되살릴 것.

### 2-3. 스페이싱

실사용 값(gap/padding/margin, px): `4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32, 64`

**엄격한 8px 그리드가 아니다.** 4의 배수(4/8/12/16/20/24/28/32/64)가 골격이지만, 그 사이를 메우는
"4n+2" 보정값(6/10/14/18/22)이 실제로 더 자주 등장한다 — 예: `.card-body{padding:16px 18px 18px}`,
`.steps-card{padding:22px 28px}`, `.chip{padding:8px 16px}`(screen-1) vs `padding:7px 14px`(screen-2 요약 칩).
결론: **4px 단위 하프스텝 그리드**로 다루고, 8의 배수를 기본값으로 삼되 광학 보정이 필요하면 ±2px을 허용한다.

컴포넌트 크기 값(참고): 아바타 36px(topbar)/56px(프로필), 스텝 서클 34px, 인풋 높이 44px,
위시 버튼 30px, 토글 44×24px, 빈 상태 아이콘 56px.

**버튼 높이는 화면마다 다르다 — 문맥별로 채택**: screen-1 `.btn` 38px(카드 CTA, 컴팩트) /
screen-2 `.btn` 44px(결제 이동 primary, 강조) / screen-3 `.btn` 40px(페이지 액션, 중간).
단일 값으로 통일하지 말고, **밀도 높은 리스트 안 버튼은 38px, 페이지 레벨 주요 액션은 40px,
결제처럼 무게가 큰 단독 CTA는 44px**로 문맥에 맞게 고른다.

### 2-4. 라운드 · 보더 · 그림자

```css
--radius-lg:28px;  /* 카드·패널 전부 */
--radius-md:16px;  /* 인풋, 텍스트에어리어 */
--radius-sm:10px;  /* 버튼, 필터 리셋, 페이지 버튼 */
/* 999px = 완전한 pill (칩, 배지, 토글, 라이브 인디케이터) */

--border:#EAE7F6;  /* 1px solid 기본, 인풋은 1.5px, 스텝 서클은 2px, 슬라이더 썸은 3px */

--shadow-l1:0 10px 30px rgba(23,20,58,.06);   /* 정적 표면(카드 기본 상태) */
--shadow-l2:0 20px 40px rgba(124,92,255,.15); /* hover 시 "떠오름" — 컬러 틴트 필수 동반 */
--ring:0 0 0 4px rgba(124,92,255,.16);         /* screen-2만 정의 — 포커스/현재 단계 링 */
```

- 직각(0 라운드)은 이 스타일에 없다. 가장 작은 라운드도 10px.
- 그림자는 정확히 2단계뿐이다: 기본은 `shadow-l1`(중립 회색 톤, 은은함), hover/부유는 `shadow-l2`(바이올렛 틴트,
  더 진하고 넓게 퍼짐). **깊이가 바뀔 때는 반드시 색이 함께 바뀐다** — 그냥 blur만 키우지 않는다.
- 추가 발견되는 그림자 값(용도별 특수 그림자, 위 2단계와 별개):
  - 배지: `0 4px 10px rgba(23,20,58,.12)` (screen-1 배지에만 존재, screen-3 배지는 그림자 없음 — 아래 §6 참고)
  - 슬라이더 썸: `0 2px 6px rgba(23,20,58,.25)`
  - 토글 노브: `0 1px 3px rgba(23,20,58,.25)`
  - 결제 primary 버튼(screen-2): `0 10px 24px rgba(124,92,255,.28)` — 일반 primary(screen-3)는 `shadow-l1`을 쓰지만,
    **결제처럼 전환 확정 액션에는 이 바이올렛 틴트 그림자로 한 단계 더 강조**해도 된다.
  - 에러 필드 포커스 링: `0 0 0 4px rgba(200,30,69,.14)` — `--ring`과 같은 반경, 색만 danger로 치환.

---

## 3. 컴포넌트 작성 규칙

### 3-1. 버튼 (주 / 보조)

```css
.btn{
  height:38px;              /* 문맥별 38/40/44 — §2-3 참고 */
  padding:0 18px;           /* 44px 인풋과 짝지을 땐 0 20px */
  border-radius:var(--radius-sm);
  font-size:13px; font-weight:700;
  border:1px solid transparent;
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  transition:transform .2s ease, box-shadow .2s ease, background .2s ease,
             color .2s ease, border-color .2s ease;
}
.btn:focus-visible{outline:2px solid var(--violet); outline-offset:2px;}

.btn-primary{
  background:linear-gradient(90deg,var(--violet),var(--pink)); color:#fff;
  box-shadow:var(--shadow-l1);              /* 강조 CTA는 §2-4의 틴트 그림자로 교체 */
}
.btn-primary:hover{transform:translateY(-2px); box-shadow:var(--shadow-l2);}

.btn-secondary{
  background:var(--surface); color:var(--ink); border-color:var(--border);
  box-shadow:var(--shadow-l1);
}
.btn-secondary:hover{transform:translateY(-2px); box-shadow:var(--shadow-l2);
  border-color:var(--violet); color:var(--violet);}
```
- 보조 위험 버튼(`.btn-danger-ghost`, screen-3 "취소하기"): `background:transparent; color:var(--danger-fg);
  border-color:var(--danger-bg); height:36px; padding:0 16px; font-size:13px;` hover 시 `background:var(--danger-bg)`.
- 클릭 즉시 라벨을 "…중" 텍스트로 바꾸고 `disabled`, 일정 시간 뒤 원복하는 **데모 피드백 패턴**을
  실제 로딩 스피너 대신 쓴다 (예: `editBtn` "검색 수정"→"수정 중…", `cancelBtn` "취소하기"→"취소 접수됨").

### 3-2. 입력 필드 — 5상태 (screen-2 폼이 정의 원본)

```css
.input-wrap input{
  height:44px; padding:0 40px 0 16px;
  border-radius:var(--radius-md); border:1.5px solid var(--border);
  background:var(--surface); color:var(--ink);
  font-size:14px; font-weight:600;
  transition:border-color .2s ease, box-shadow .2s ease, background .2s ease;
}
```
| 상태 | 트리거 클래스 | 보더/배경 | 플래그(`.state-flag--*`) | 비고 |
|---|---|---|---|---|
| 기본 | (없음) | `1.5px solid var(--border)` / `--surface` | `--bg` bg / `--muted-text` fg, 1px 보더 | |
| 포커스 | `:focus-visible` | 보더 `--violet` + `box-shadow:var(--ring)` | `--info-bg` bg / `--violet` fg | screen-2에서 `autofocus`로 상시 시연 |
| 에러 | `.field.is-error` | 보더 `--danger-fg` / 배경 `#FFFAFB`, 포커스 시 `0 0 0 4px rgba(200,30,69,.14)` | `--danger-bg` bg / `--danger-fg` fg | `aria-invalid="true"` + `aria-describedby` 필수, 상태 아이콘 danger색 |
| 완료 | `.field.is-done` | 보더 `--success-fg` / 배경 `#F5FFFB` | `--success-bg` bg / `--success-fg` fg | **`readonly` 사용** (disabled 아님 — 값은 보이되 확정) |
| 비활성 | `.fake-input` (실제 input 아님) | `1.5px dashed var(--border)` / `--neutral-bg`, `cursor:not-allowed` | `--neutral-bg` bg / `--neutral-fg` fg | 진짜 `<input disabled>`가 아니라 안내 텍스트 박스로 대체 |

- 셀렉트는 `appearance:none` + 우측 `▾` 커스텀 caret(`.caret`, 절대 위치 right:16px).
- 도움말은 `.field-help`(12px, muted-text), 상태 메시지는 `.field-msg`(12px, 아이콘+텍스트, 에러/완료색).
- 약관 체크박스(`.terms-row`)는 인풋과 별개 패턴: 카드형 row + `is-invalid` 시 보더 danger + 1회성 `shake-once`.

### 3-3. 배지 (상태 4종)

```html
<span class="badge badge-open"><span class="bdot" aria-hidden="true"></span>예약가능</span>
```
```css
.badge{
  display:inline-flex; align-items:center; gap:6px;
  padding:5px 12px; border-radius:999px; font-size:11px; font-weight:800;
}
.badge .bdot{width:6px; height:6px; border-radius:50%;}
.badge-open{background:var(--success-bg); color:var(--success-fg);}
.badge-urgent{background:var(--warning-bg); color:var(--warning-fg);} /* bdot에 dot-pulse 추가 */
.badge-flex{background:var(--neutral-bg); color:var(--neutral-fg);}
.badge-deal{background:var(--danger-bg); color:var(--danger-fg);}
```
- 구조는 항상 `배경/텍스트 페어 + 6px 점 + 텍스트`. 점 색은 텍스트 색과 동일.
- **펄스(`dot-pulse`)는 "진행 중/대기 중" 의미의 상태에만** 붙인다 — screen-1의 `badge-urgent`(마감임박),
  screen-3의 `badge-pending`(결제대기)이 유일한 펄스 배지. `badge-open`(확정 긍정), `badge-flex`/`badge-done`(중립·종결),
  `badge-deal`/`badge-cancelled`(danger·종결)에는 펄스를 붙이지 않는다.
- screen-1의 배지는 `box-shadow:0 4px 10px rgba(23,20,58,.12)`을 갖지만 screen-3 배지는 그림자가 없다 —
  **카드 위에 얹히는 오버레이 배지(사진 위)는 그림자로 띄우고, 리스트 행 안의 배지는 그림자 없이 평평하게** 두는 것으로 채택한다.

### 3-4. 카드

```css
.item-card{
  background:var(--surface); border-radius:var(--radius-lg);
  box-shadow:var(--shadow-l1); overflow:hidden;
  display:flex; flex-direction:column;
  transition:transform .2s ease, box-shadow .2s ease;
}
.item-card:hover{transform:translateY(-4px); box-shadow:var(--shadow-l2);}
.card-thumb{
  height:132px; background:linear-gradient(135deg,var(--violet) 0%,var(--pink) 100%);
  display:flex; align-items:center; justify-content:center; position:relative;
}
.card-body{padding:16px 18px 18px; display:flex; flex-direction:column; gap:8px; flex:1;}
```
- 썸네일에 실제 이미지가 없을 때 **바이올렛→핑크 그라디언트 + 흰 선 아이콘(stroke `#fff`)** 으로 대체 — 회색 placeholder 금지.
- 배지 오버레이는 `position:absolute; top:10px; left:10px`, 위시(찜) 버튼은 `top:10px; right:10px`, 반투명 흰 원형.
- 제목은 `-webkit-line-clamp:2` + `min-height:2.7em`으로 2줄 고정(긴 제목도 카드 높이가 흔들리지 않게).
- 카드 안 CTA(`.card-cta`)는 항상 `width:100%`.

### 3-5. 상단바(identity)

```css
.topbar{border-bottom:1px solid var(--border);}
.topbar-inner{
  max-width:1200px; margin:0 auto; padding:16px 24px;
  display:flex; align-items:center; justify-content:space-between; gap:16px;
}
.logo{
  font-size:24px; font-weight:800; letter-spacing:-0.02em;
  background:linear-gradient(90deg,var(--violet),var(--pink));
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
```
- 우측 고정 구성: `.live-chip`(펄스 도트 + "실시간 …" 텍스트, pill, shadow-l1) + `.user-avatar`(36px 원형 그라디언트, 이니셜).
- 900px 이하에서 `.live-chip span:not(.dot)` 텍스트를 숨기고 점만 남기며, 560px 이하에서는 칩 자체를 숨긴다.
- 검색/예약 화면은 topbar 아래 보조 바(검색 요약 칩 줄 / 브레드크럼)를 추가로 둔다 — 이것도 `.topbar-inner`와 같은
  `max-width:1200px` 컨테이너 규칙을 공유한다.

### 3-6. 빈 상태

```css
.empty-panel{
  background:var(--surface); border-radius:var(--radius-lg); box-shadow:var(--shadow-l1);
  padding:64px 32px; text-align:center;
  display:flex; flex-direction:column; align-items:center; gap:8px;
}
.empty-icon{
  width:56px; height:56px; border-radius:50%; background:var(--neutral-bg);
  display:flex; align-items:center; justify-content:center;
}
```
- 아이콘은 56px 원형 `--neutral-bg` 배지 안에 SVG(26px, `--neutral-fg`) 또는 이모지(screen-3의 좌측 내비 전환 시 ♡/💳).
- 제목 16px/700 + 설명 13px/muted-text(`max-width:40ch`로 줄바꿈 제어) + `.btn-secondary` CTA 하나.
- `hidden` 속성으로 토글하며, 필터 결과 0건(screen-1)이든 좌측 내비 탭 전환(screen-3)이든 **같은 컴포넌트를 재사용**한다.

---

## 4. 시그니처 — "살아있는 숫자"

원본 스타일 시그니처: **카운트업 + 숨쉬는 실시간 인디케이터의 조합.** 아래는 실제 3개 파일에서 이 시그니처가
쓰인 정확한 위치와 구현 패턴이다.

**1) 카운트업 (count-up)** — 페이지의 "지금 이 순간" 핵심 수치 딱 하나에만 쓴다:
- screen-1: 검색 결과 총 개수(`#totalCount`, 700ms)
- screen-2: 총 결제 금액(`#totalAmount`, 800ms)
- screen-3: 내 예약 건수(`#bookingCount`, 600ms)

표준 구현(정답 패턴 — booking/mybookings 방식):
```js
var counter = document.getElementById('bookingCount');
var target = parseInt(counter.getAttribute('data-target-value'), 10) || 0;
if (reduced) {
  counter.textContent = target;           // 모션 축소: 최종값 그대로
} else {
  counter.textContent = 0;                // JS 정상 동작 시에만 0에서 시작
  var start = null, dur = 600;
  function step(ts){
    if (start === null) start = ts;
    var p = Math.min((ts - start) / dur, 1);
    var eased = 1 - Math.pow(1 - p, 3);    // ease-out cubic
    counter.textContent = Math.round(eased * target);
    if (p < 1) requestAnimationFrame(step);
    else counter.textContent = target;
  }
  requestAnimationFrame(step);
}
```
**HTML에는 반드시 최종값을 먼저 적어 두고**(`<span data-target-value="3">3</span>`), JS가 로드되면 그 값을
0으로 지웠다가 다시 채워 올린다. 이렇게 해야 JS가 실패해도 화면엔 정답이 남는다(§1의 원칙과 동일 근거).

**2) 숨쉬는 도트(breathing dot)** — `@keyframes breathe{0%,100%{opacity:1;scale:1} 50%{opacity:.45;scale:.8}}` 2초 주기.
"지금도 진행 중/대기 중"인 상태에만 붙인다: 상단바 실시간 칩의 점, `badge-urgent`(마감임박)와 `badge-pending`
(결제대기)의 점, 그리고 저장 상태 표시줄(screen-3 "모든 변경사항 저장됨")의 점. **확정·종결 상태(예약가능, 이용완료,
취소됨)에는 붙이지 않는다** — 숨쉬는 점은 "살아서 바뀔 수 있음"의 신호이지 장식이 아니다.

**남용 금지선**:
- 카운트업은 화면당 최대 1~2곳(핵심 총합 수치만). 모든 숫자를 카운트업하면 산만해진다.
- 펄스 점은 화면당 실시간 지표 1개 + 상태 배지 중 "대기/긴급"류에만. 정적 정보에 펄스를 붙이지 않는다.
- 로드 스태거(`.reveal`)는 페이지의 큰 리전 단위(헤더 아래 섹션들)에만 60~80ms 간격으로 걸고, 리전 내부 개별
  요소(카드 한 장 한 장)까지 스태거하지 않는다 — 원본 지시의 "총 1.2초 이내" 히어로 시퀀스를 넘기지 않는다.

---

## 5. 금지 사항

원본 스타일 지시(`style-03-trendy-saas.md` "■ 금지")와 3개 파일의 실제 구현을 종합:

1. **직각** — 모든 표면·버튼·입력의 최소 라운드는 10px(`--radius-sm`). 0 라운드 요소를 추가하지 않는다.
2. **격자 보더 테이블** — 데이터를 표(`<table>` + 셀 보더)로 나열하지 않는다. 리스트/카드/row 패턴만 쓴다.
3. **다크 배경** — 이 시스템은 전면 라이트 톤(`--bg:#FBFAFF`)이 전제다. 새 화면에 다크 섹션을 넣지 않는다.
4. **모노스페이스 폰트** — 숫자 정렬은 `tabular-nums`로 해결하지 폰트를 바꾸지 않는다.
5. **무지개/다색 그라디언트** — 바이올렛→핑크 한 방향 외의 그라디언트 조합 금지.
6. **0.3초를 넘는 개별 인터랙션 트랜지션** — hover/focus/토글 등 사용자 조작에 반응하는 트랜지션은 전부 0.15~0.2초대다
   (`.2s`가 표준). 로드 시 1회성 스태거(`.4s`)는 예외지만 그것도 화면당 한 시퀀스뿐이다.
7. **무한 회전/이동 애니메이션** — 단, `dot-pulse`(opacity+scale breathing)는 "숨쉬는 점" 시그니처로 명시 허용된
   유일한 무한 애니메이션이다. 회전(rotate)이나 위치 이동(무한 marquee 등)은 여전히 금지.
8. **`--muted`를 텍스트로 사용** — 장식(배지/보더)에만 쓴다. 사람이 읽는 문장에는 `--muted-text`.
9. **비활성 필드에 실제 `disabled` 속성만으로 처리하지 않기** — 이 시스템은 비활성을 `.fake-input`(대시보드
   텍스트 박스)으로 표현한다. `<input disabled>`를 그대로 회색 처리해 방치하지 않는다.
10. **회색 placeholder 박스로 이미지 대체** — 썸네일 자리는 브랜드 그라디언트 + 흰 아이콘으로 채운다.

---

## 6. Good / Bad 코드 예시

### 예시 1 — 카운트업의 "JS 실패 폴백"

```html
<!-- GOOD (screen-2-booking.html, screen-3-mybookings.html) -->
<!-- HTML 자체에 최종값이 이미 적혀 있다 → JS가 없거나 실패해도 정답이 보인다 -->
<span class="summary-total-value tabnum" id="totalAmount" data-target-value="400000">₩400,000</span>
```
```html
<!-- BAD (screen-1-search.html 실제 코드 — 원칙 위반 사례) -->
<!-- 초기 콘텐츠가 "0" → JS가 죽으면 사용자는 "서울 호텔 0곳"을 본다 -->
<h2 class="results-title">서울 호텔 <span class="tabnum" id="totalCount" data-target-value="128">0</span>곳</h2>
```
→ 새 화면에서는 반드시 booking/mybookings 패턴(최종값을 HTML에 먼저 적기)을 따른다. screen-1은 이 시스템
안에서 발견된 실제 반례이니 그대로 복제하지 말 것.

### 예시 2 — 펄스는 "진행 중" 상태에만

```html
<!-- GOOD: 대기/긴급 상태에만 dot-pulse -->
<span class="badge badge-urgent"><span class="bdot dot-pulse" aria-hidden="true"></span>마감임박</span>
<span class="badge badge-pending"><span class="bdot" aria-hidden="true"></span>결제 대기</span>
<!-- ↑ pending은 badge-pending .bdot 자체 CSS에 breathe가 걸려 있어 별도 클래스 불필요 -->
```
```html
<!-- BAD: 확정·종결 상태에 펄스를 붙이면 "아직도 바뀌는 중"이라는 잘못된 신호를 준다 -->
<span class="badge badge-open"><span class="bdot dot-pulse" aria-hidden="true"></span>예약가능</span>
```

### 예시 3 — 입력 필드 "완료" 상태는 disabled가 아니라 readonly

```html
<!-- GOOD (screen-2-booking.html) — 완료된 값은 보이되 확정됨을 readonly로 표현 -->
<div class="field is-done">
  <div class="input-wrap">
    <input type="text" id="fldName" value="정하람" readonly>
    <svg class="state-icon" ...><path d="M20 6 9 17l-5-5"/></svg>
  </div>
  <span class="field-msg is-done">예약자명이 확인됐어요.</span>
</div>
```
```html
<!-- BAD — disabled를 쓰면 포커스도 안 되고 스크린리더도 값을 건너뛴다 -->
<input type="text" id="fldName" value="정하람" disabled>
```

---

## 7. 출력 전 자체 체크리스트

새 화면을 만든 뒤 이 항목을 순서대로 확인한다:

- [ ] 페이지 배경이 `--bg`(#FBFAFF)이고 좌하단 민트 / 우상단 바이올렛 블롭(blur 90px) 두 개가 fixed로 깔려 있는가?
- [ ] 카드·패널의 라운드가 전부 `--radius-lg`(28px) 이상이고, 인풋/버튼은 각각 `--radius-md`/`--radius-sm`인가?
- [ ] 그림자가 기본 `shadow-l1` / hover만 `shadow-l2`(컬러 틴트 동반) 2단계로만 이루어졌는가?
- [ ] 회색 텍스트에 `--muted`가 아니라 `--muted-text`를 썼는가? (대비 4.5:1 이상 보장)
- [ ] 상태를 나타내는 모든 배지/배너가 success/warning/neutral/danger 4종 bg·fg 페어 중 하나를 그대로 쓰는가?
- [ ] 펄스(`dot-pulse`)를 진행 중/대기 상태에만 붙였는가? 확정·종결 상태에 남용하지 않았는가?
- [ ] 카운트업을 쓴다면 HTML에 최종값을 먼저 적고 JS가 0→목표로 다시 채우는 구조인가? (screen-1처럼 초기값 0 방치 금지)
- [ ] 인터랙션 트랜지션이 전부 0.3초 이내인가? (로드 스태거 1회성 제외)
- [ ] 900px 이하에서 그리드가 1열로 접히고, 부가 텍스트(라이브 칩 등)가 정리되는가?
- [ ] `prefers-reduced-motion: reduce`에서 모든 애니메이션·트랜지션이 즉시 최종 상태로 렌더되는가?
- [ ] 모든 인터랙티브 요소에 `:focus-visible{outline:2px solid var(--violet); outline-offset:2px;}`가 있는가?
- [ ] JS를 전부 끄고 열어도 화면이 완결된 상태로 보이는가? (에러 배너·배지·수치 전부 최종값)
- [ ] 직각·격자 테이블·다크 배경·모노스페이스·무지개 그라디언트가 하나도 없는가?
- [ ] 숫자에 `.tabnum`이 빠짐없이 붙어 있는가?
- [ ] 빈 상태를 만들었다면 56px 원형 아이콘 + 제목(16px/700) + 설명(13px/muted-text, 40ch) + 보조 버튼 구조를 따르는가?
