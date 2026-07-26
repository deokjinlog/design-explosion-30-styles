# 3층 파이프라인 — 스타일 생성 방식 (Zen Garden)

> **HTML 통짜 생성은 폐기.** 이제 DOM(스켈레톤)을 고정하고 **CSS 3층만** 만든다.
> 콘텐츠 동일성은 스켈레톤이 구조적으로 보장(프롬프트로 부탁 안 함). 게이트는 `coverage-lint` 하나.

## 자산 (이미 있음)

```
references/
  skeletons/archetype-{A,B,D}.v1.html   원형별 고정 DOM 계약(훅 포함). 절대 수정 금지.
  base/archetype-{A,B,D}.css            원형별 공용 컴포넌트(전부 var(--토큰))
  tokens/style-01..30.css               스타일 변수(12개). ★원형 무관 = 전 원형 재사용
  signature/style-NN--X.css             구조가 강한 스타일만(뭉친 것은 불필요)
  assemble.py                           스켈레톤 + CSS층 → 자립 HTML
  coverage-lint.py                      게이트(환각 셀렉터·누락 영역)
```

## 스타일 1개 만들기 (원형 X, 스타일 NN)

1. **tokens** `tokens/style-NN.css` — `:root{}` 안에 12변수(색·radius·space·font·elevation·type-scale). 스타일의 미감을 이 값으로.
2. **signature** `signature/style-NN--X.css` — **토큰으로 표현 안 되는 구조적 특징만**(예: 터미널=버블제거+프리픽스, 스위스=지그재그 격자). 색·형태는 tokens 몫이니 넣지 마라. **뭉친/색깔변주 스타일은 이 파일 없음.** 판단 기준: `map.py` 좌표에서 고립도 높고 구조가 특이하면 signature, 아니면 토큰전용.
3. **조립**: `python3 references/assemble.py references/skeletons/archetype-X.v1.html OUT/style-NN.html references/base/archetype-X.css references/tokens/style-NN.css [references/signature/style-NN--X.css]`
4. **게이트**: 조립물의 `<style>`을 뽑아 `coverage-lint.py OUT/style-NN.html <css>` → **PASS 필수**(환각 셀렉터 0·누락 영역 0).

## 갤러리 1개 (원형 X, 30 스타일)

- 위를 NN=01..30 반복 조립 → `docs/design-gallery/<날짜>-<도메인>-zen/style-NN.html`.
- **검증**: coverage 30/30 · 30장 **body 바이트 동일**(조립이 보장 — 다르면 스켈레톤이 안 고정된 것) · 콘텐츠 마커.
- 갤러리 HTML은 평면 30그리드(iframe).

## 새 원형 추가

- `skeletons/archetype-X.v1.html`(고정 DOM·훅) + `base/archetype-X.css`(토큰 먹음) **2개만** 저작. **tokens 30은 그대로 재사용**(원형 무관).
- 원형당 스켈레톤 ~1개면 충분(T2). 영역 개수가 다른 스타일만 스켈레톤 변형.

## 새 스타일 추가 / 재샘플

- `map.py`로 좌표 지도 → **빈 코너**(예: 웜·각진·플랫)를 채우는 tokens를 새로 뽑으면 겹침 없이 다양성↑.
- 스타일 하나 추가 = tokens 파일 하나(+구조적이면 signature) → **세 원형 전부에 즉시 적용**.

## 폐기된 것

- `archetype-lint` → `coverage-lint`로 교체(가능한 실패 전 집합 커버). `style-lint`는 스타일 금칙 검사로 축소 존치.
- "같은 콘텐츠 지켜라" 프롬프트 지시 → 불필요(스켈레톤 고정).
- HTML 통짜 생성 → 금지.
