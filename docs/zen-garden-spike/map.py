#!/usr/bin/env python3
"""map.py — 30 토큰 파일 → 디자인 공간 좌표 지도.

T3(7개)를 30개로 확장. 세 가지를 뱉는다:
  1) 좌표 테이블 (측정에서 나온 지도)
  2) 뭉친 쌍 (거리 < 임계 = 낭비 슬롯 = 병합/재샘플 후보)
  3) 빈 코너 (hue×shape×ornament 격자에서 비어있는 셀 = 재샘플 타겟)

usage: python3 map.py all-tokens/
"""
import re, sys, os, glob, colorsys, math

d = sys.argv[1] if len(sys.argv) > 1 else "all-tokens"
files = sorted(glob.glob(os.path.join(d, "style-*.css")))

def hex_hsl(h):
    h = re.sub(r'[^0-9A-Fa-f]', '', h)[:6]
    if len(h) < 6: return 0.0, 0.0, 0.5
    r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hh*360, s, l

def numf(s):
    m = re.search(r'-?\d+\.?\d*', s or "")
    return float(m.group(0)) if m else 0.0

styles = {}
for f in files:
    nn = re.search(r'style-(\d+)', f).group(1)
    css = open(f, encoding="utf-8").read()
    def g(k):
        m = re.search(re.escape(k) + r'\s*:\s*([^;]+);', css)
        return m.group(1).strip() if m else None
    if not g('--accent'):
        print(f"  ⚠ {nn}: --accent 없음, 건너뜀"); continue
    hue, sat, _ = hex_hsl(g('--accent'))
    _, _, bglit = hex_hsl(g('--bg') or "#ffffff")
    radius = numf(g('--radius')); space = numf(g('--space'))
    elev = numf(g('--elevation')); ts = numf(g('--type-scale'))
    styles[nn] = {
        "hue": hue, "sat": sat, "bglit": bglit,
        "shape": min(radius/24, 1),
        "density": 1 - min(max(space-8, 0)/12, 1),
        "ornament": min(max(elev, 0), 1),
        "typec": min(max(ts-1, 0)/1.2, 1),
        "accent": (g('--accent') or "").strip(),
    }

ids = sorted(styles)
def dist(a, b):
    dh = abs(a["hue"]-b["hue"]); dh = min(dh, 360-dh)/180
    W = {"hue":1.5, "sat":1.0, "shape":0.9, "density":0.8, "ornament":0.9, "typec":0.6, "bglit":1.1}
    s = (W["hue"]*dh)**2
    for k in ("sat","shape","density","ornament","typec","bglit"):
        s += (W[k]*(a[k]-b[k]))**2
    return math.sqrt(s)

print("="*74)
print(f"디자인 공간 지도 — {len(ids)} 스타일 (토큰에서 측정)")
print("="*74)
print(f"{'':4}{'accent':9}{'bg':>5}{'hue':>5}{'sat':>6}{'shape':>7}{'dens':>6}{'orn':>6}{'typ':>6}")
for i in ids:
    s = styles[i]
    print(f"{i}  {s['accent']:9}{s['bglit']:5.2f}{s['hue']:5.0f}{s['sat']:6.2f}{s['shape']:7.2f}{s['density']:6.2f}{s['ornament']:6.2f}{s['typec']:6.2f}")

# --- 2) 뭉친 쌍 ---
TH = 0.40
pairs = sorted((dist(styles[ids[a]], styles[ids[b]]), ids[a], ids[b])
               for a in range(len(ids)) for b in range(a+1, len(ids)))
crowd = [(d,i,j) for d,i,j in pairs if d < TH]
print(f"\n■ 뭉친 쌍 (거리 < {TH} = 낭비 슬롯 / 재샘플 후보) — {len(crowd)}쌍")
for d,i,j in crowd:
    print(f"    {i}↔{j}  d={d:.2f}")
# 각 스타일의 최근접거리(고립도)
print("\n■ 고립도 (최근접 이웃 거리 — 클수록 고유, 작을수록 뭉침)")
nn = {i: min(dist(styles[i], styles[j]) for j in ids if j != i) for i in ids}
for i in sorted(ids, key=lambda x: nn[x]):
    bar = "█"*int(nn[i]*20)
    flag = "  ← 뭉침" if nn[i] < 0.30 else ("  ← 고유" if nn[i] > 0.7 else "")
    print(f"    {i}  {nn[i]:.2f} {bar}{flag}")

# --- 3) 빈 코너 (hue-family × shape × ornament) ---
def hue_fam(h):
    fams = [("빨강",0,20),("웜/주황",20,50),("노랑",50,70),("초록",70,160),
            ("청록",160,200),("파랑",200,250),("보라",250,292),("핑크",292,340),("빨강",340,360)]
    for name,a,b in fams:
        if a <= h < b: return name
    return "빨강"
def bin3(v, lo, hi): return "낮음" if v < lo else ("높음" if v > hi else "중간")

grid = {}
for i in ids:
    s = styles[i]
    cell = (hue_fam(s["hue"]), bin3(s["shape"],.25,.6), bin3(s["ornament"],.35,.65))
    grid.setdefault(cell, []).append(i)

print("\n■ 격자 점유 (hue-family × 형태 × 장식) — 뭉친 셀")
for cell, mem in sorted(grid.items(), key=lambda x:-len(x[1])):
    if len(mem) >= 2:
        print(f"    {cell[0]:6}·{cell[1]:4}형태·{cell[2]:4}장식  →  {len(mem)}개 {mem}")
occupied = set(grid)
hue_fams = ["빨강","웜/주황","노랑","초록","청록","파랑","보라","핑크"]
empty = [(h,sh,o) for h in hue_fams for sh in ("낮음","중간","높음") for o in ("낮음","중간","높음")
         if (h,sh,o) not in occupied]
print(f"\n■ 빈 코너 = 재샘플 타겟 ({len(empty)}/{8*3*3} 셀 비어있음) — 예:")
# 대표적으로 '웜·각진·플랫' 같은 눈에 띄는 빈 조합 몇 개
picks = [c for c in empty if c[0] in ("웜/주황","빨강","노랑","초록") ][:8]
for h,sh,o in picks:
    print(f"    {h}·{sh}형태·{o}장식")
print(f"\n→ 30개가 점유한 셀 {len(occupied)}개 / 낭비쌍 {len(crowd)}개 → 낭비 슬롯을 빈 코너로 옮기면 고르게 퍼짐")
