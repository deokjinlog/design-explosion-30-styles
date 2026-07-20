# 히어로 템플릿 (중립 스타일 — 30개 각도 전체 공유, 결정4)

이 파일은 30개 각도 시안이 **공유하는 단 하나의 히어로 골격**이다. 각 각도 에이전트는
아래 HTML을 **그대로 복사**해서 카피 슬롯 `{{HEADLINE}}` / `{{SUB}}` / `{{CTA}}` 와
푸터의 `{n}` / `{각도명}` / `{패밀리}` 만 채운다. **색·폰트·여백·클래스명·태그 구조는
절대 바꾸지 않는다** — 병렬로 생성되는 30개 에이전트가 서로의 결과물을 보지 못해도
동일한 스타일이 나오도록, 값은 여기 이미 고정돼 있다.

> **왜 중립인가**: 스타일이 변수가 되면 메시지 비교가 오염된다(FR-8). 눈에 보이는
> 차이가 카피뿐이어야 30개 각도를 정직하게 비교할 수 있다. 스타일을 결합하는 것은
> 각도가 확정된 뒤 design-explosion 핸드오프의 몫이다(결정4).

## 히어로 한도 (결정5 — 기계적으로 검사됨)

- 헤드라인(`cx-headline`) **≤ 60자**
- 서브카피(`cx-sub`) **≤ 140자**
- CTA(`cx-cta`) **정확히 1개**
- 히어로는 스크롤 없이 **1 뷰포트 안에서 완결**

## 계약 클래스 — copy_lint.py 가 파싱하는 전부

`scripts/copy_lint.py` 는 정규식으로 아래 세 클래스만 읽는다. 클래스명이나
태그(`<h1>`/`<p>`/`<a>`)를 바꾸면 린터가 아무것도 못 읽고 오탐/누락이 난다.

| 클래스 | 태그 | 개수 |
|---|---|---|
| `cx-headline` | `<h1>` | 정확히 1개 |
| `cx-sub` | `<p>` | 정확히 1개 |
| `cx-cta` | `<a>` | **정확히 1개** (2개 이상이면 FAIL) |

## 골격 (그대로 복사)

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{HEADLINE}}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
  :root {
    /* 모노크롬 + 단일 액센트 — 30개 시안 전체 공통, 값 고정 (바꾸지 말 것) */
    --ink: #14171a;
    --sub-ink: #52585f;
    --bg: #fafafa;
    --surface: #ffffff;
    --border: #e6e8eb;
    --accent: #2554f0;
    --accent-ink: #ffffff;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; height: 100%; }
  body {
    background: var(--bg);
    color: var(--ink);
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .cx-hero {
    min-height: 100vh;
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 8vh 24px 64px;
    gap: 22px;
  }
  .cx-headline {
    font-size: clamp(28px, 5vw, 44px);
    font-weight: 800;
    line-height: 1.3;
    max-width: 720px;
    margin: 0;
    color: var(--ink);
  }
  .cx-sub {
    font-size: clamp(16px, 2vw, 19px);
    line-height: 1.6;
    max-width: 560px;
    margin: 0;
    color: var(--sub-ink);
  }
  .cx-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-top: 6px;
    padding: 14px 32px;
    border-radius: 8px;
    background: var(--accent);
    color: var(--accent-ink);
    font-size: 16px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .cx-cta:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
  }
  /* 선택 요소(FR-7 보조): 신뢰 배지·마이크로카피 — 없어도 히어로는 완결됨 */
  .cx-trust {
    font-size: 13px;
    color: var(--sub-ink);
    opacity: 0.8;
    margin: 0;
  }
  .cx-footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 10px 16px;
    text-align: center;
    font-size: 12px;
    color: var(--sub-ink);
    background: var(--surface);
    border-top: 1px solid var(--border);
  }
  /* NFR-3: JS는 연출 전용 — 꺼져도 카피는 온전히 읽힌다. 아래는 그 연출을 끄는 규칙 */
  @media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
  }
  @media (max-width: 480px) {
    .cx-hero { padding: 6vh 20px 64px; }
  }
</style>
</head>
<body>
  <main class="cx-hero">
    <h1 class="cx-headline">{{HEADLINE}}</h1>
    <p class="cx-sub">{{SUB}}</p>
    <a class="cx-cta" href="#">{{CTA}}</a>
    <!-- 선택: 신뢰 배지·마이크로카피가 있으면 아래 한 줄만 채워 넣는다 (없으면 통째로 삭제)
    <p class="cx-trust">{{TRUST_MICROCOPY}}</p>
    -->
  </main>
  <footer class="cx-footer">ANGLE {n} · {각도명} · {패밀리}</footer>
  <script>
    // 연출 전용(NFR-3) — 이 스크립트가 없거나 실패해도 위 HTML만으로 히어로는 완전하다.
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.querySelectorAll('.cx-hero > *').forEach(function (el, i) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(8px)';
        el.style.transition = 'opacity .4s ease ' + (i * 0.08) + 's, transform .4s ease ' + (i * 0.08) + 's';
        requestAnimationFrame(function () {
          requestAnimationFrame(function () {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
          });
        });
      });
    }
  </script>
</body>
</html>
```

## 사용 방법 (요약)

1. 위 골격을 `angle-NN-<slug>.html` 로 그대로 복사한다.
2. `{{HEADLINE}}`(≤60자) / `{{SUB}}`(≤140자) / `{{CTA}}` 세 슬롯만 각도별 카피로 채운다.
3. 푸터의 `{n}`(각도 번호, 01~30) / `{각도명}` / `{패밀리}`(A~F 풀네임)를 채운다.
4. `<style>` 블록과 `cx-*` 클래스, 태그 구조는 한 글자도 바꾸지 않는다.
5. `.cx-trust` 보조 요소는 선택이다 — 안 쓰면 주석째 지운다(빈 클래스만 남기지 않는다).
