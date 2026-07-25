#!/usr/bin/env python3
"""T3 — 토큰전용 변별력 측정.

토큰 CSS(.style-NN{--accent..--type-scale})를 파싱 → 좌표 6축으로 → 쌍거리 →
임계 이하면 "사실상 같은 그림"으로 병합 후보. 눈대중 클러스터링을 숫자로.

usage: python3 cluster.py t3-token-vectors.css
"""
import re, sys, colorsys, math

NAMES = {"03":"trendy-saas","16":"material","21":"ai-product","22":"fintech-soft",
         "24":"healthcare","25":"commerce","29":"vibrant-modern"}

def hex_hsl(h):
    h = h.lstrip('#'); r,g,b = (int(h[i:i+2],16)/255 for i in (0,2,4))
    hh,l,s = colorsys.rgb_to_hls(r,g,b)
    return hh*360, s, l   # hue(0-360), sat(0-1), light(0-1)

css = open(sys.argv[1], encoding="utf-8").read()
css = re.sub(r'/\*.*?\*/', ' ', css, flags=re.S)

styles = {}
for m in re.finditer(r'\.style-(\d+)\s*\{([^}]*)\}', css):
    nn, body = m.group(1), m.group(2)
    def g(k):
        mm = re.search(k + r'\s*:\s*([^;]+);', body)
        return mm.group(1).strip() if mm else None
    hue, sat, lit = hex_hsl(g('--accent'))
    radius = float(re.sub(r'[^0-9.]','', g('--radius')))
    space  = float(re.sub(r'[^0-9.]','', g('--space')))
    elev   = float(g('--elevation'))
    tscale = float(g('--type-scale'))
    # 좌표 6축 (0~1, hue 는 0~360 원형)
    styles[nn] = {
        "name": NAMES.get(nn, nn),
        "hue": hue,                                  # 원형
        "sat": sat,                                  # 채도
        "shape": min(radius/24, 1),                  # 형태(둥글기)
        "density": 1 - min(max(space-8,0)/12, 1),    # 밀도(작을수록 조밀)
        "ornament": elev,                            # 장식(그림자/그라디언트)
        "typec": min(max(tscale-1,0)/1.2, 1),        # 타입 대비
        "accent": g('--accent'),
    }

def dist(a, b):
    dh = abs(a["hue"]-b["hue"]); dh = min(dh, 360-dh)/180        # 원형 hue → 0~1
    W = {"hue":1.5, "sat":1.0, "shape":0.8, "density":0.8, "ornament":0.8, "typec":0.6}
    s = (W["hue"]*dh)**2
    for k in ("sat","shape","density","ornament","typec"):
        s += (W[k]*(a[k]-b[k]))**2
    return math.sqrt(s)

ids = list(styles)
THRESH = 0.42   # 이 거리 이하 = "사실상 같은 그림"

print("="*66)
print("T3 — 토큰전용 좌표 (뭉친 7개)")
print("="*66)
print(f"{'':10}{'accent':9}{'hue':>5}{'sat':>6}{'shape':>7}{'dens':>6}{'orn':>6}{'typ':>6}")
for i in ids:
    s = styles[i]
    print(f"{i} {s['name']:11}{s['accent']:9}{s['hue']:5.0f}{s['sat']:6.2f}{s['shape']:7.2f}{s['density']:6.2f}{s['ornament']:6.2f}{s['typec']:6.2f}")

print(f"\n쌍거리 (< {THRESH} = 병합 후보 ★):")
pairs = []
for a in range(len(ids)):
    for b in range(a+1, len(ids)):
        d = dist(styles[ids[a]], styles[ids[b]])
        pairs.append((d, ids[a], ids[b]))
pairs.sort()
for d, i, j in pairs:
    star = " ★" if d < THRESH else ""
    print(f"  {i}-{j}  {styles[i]['name']:14}↔ {styles[j]['name']:14} d={d:.2f}{star}")

# 단일연결 클러스터링
parent = {i:i for i in ids}
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
for d,i,j in pairs:
    if d < THRESH: parent[find(i)] = find(j)
clusters = {}
for i in ids: clusters.setdefault(find(i), []).append(i)

print(f"\n클러스터 (임계 {THRESH}):")
for k,(root,members) in enumerate(clusters.items(), 1):
    labels = [f"{m}:{styles[m]['name']}" for m in members]
    tag = "  ← 병합 검토" if len(members)>1 else "  (단독 = 진짜 다름)"
    print(f"  {k}. {', '.join(labels)}{tag}")
print(f"\n→ 7개 → 실질 {len(clusters)}개 그룹")
