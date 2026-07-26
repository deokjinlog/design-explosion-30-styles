# -*- coding: utf-8 -*-
"""정본 재접지 패치 — 30 토큰의 --font/--font-ui/--type-scale 전면 교체 +
   @gfont 로딩 지시자 주입 + 산업라벨 10종 팔레트/라운드 재접지.
   출처: 실제 디자인 시스템(Carbon/Material3/Polaris/Ant/GOV.UK) + 디자인 운동(Swiss/Bauhaus/DeStijl/Memphis/Neubrutal/Editorial/Riso).
   폰트는 전부 Google Fonts 로딩 가능(GitHub Pages 실렌더)."""
import re, os

REF = "/home/djchoi/deokjinlog/design-explosion-30-styles/skills/design-style-explorer/references"
TOK = REF + "/tokens"

# NN: name, source, url, body, ui, [gfonts], typescale
FONT = {
 "01":("SF HUD","Sci-fi HUD 각진 테크","https://fonts.google.com/specimen/Rajdhani",
       "'Rajdhani','Noto Sans KR',sans-serif","'Orbitron','Rajdhani',sans-serif",
       ["Rajdhani:wght@500;600;700","Orbitron:wght@700;900","Noto+Sans+KR:wght@400;500;700"],"1.3"),
 "02":("GOV.UK 공공","GOV.UK Design System","https://design-system.service.gov.uk/styles/",
       "'Public Sans','Noto Sans KR',sans-serif","'Public Sans','Noto Sans KR',sans-serif",
       ["Public+Sans:wght@400;600;700","Noto+Sans+KR:wght@400;500;700"],"1.2"),
 "03":("shadcn/ui","shadcn/ui (Radix+Tailwind)","https://ui.shadcn.com/",
       "'Inter','Noto Sans KR',sans-serif","'Inter','Noto Sans KR',sans-serif",
       ["Inter:wght@400;500;600;700","Noto+Sans+KR:wght@400;500;700"],"1.2"),
 "04":("밀집 터미널","터미널/등폭(IBM Plex Mono)","https://fonts.google.com/specimen/IBM+Plex+Mono",
       "'IBM Plex Mono','Nanum Gothic Coding',monospace","'IBM Plex Mono','Nanum Gothic Coding',monospace",
       ["IBM+Plex+Mono:wght@400;500;600","Nanum+Gothic+Coding:wght@400;700"],"1.15"),
 "05":("Neubrutalism","Neubrutalism (NN/g)","https://www.nngroup.com/articles/neobrutalism/",
       "'Space Mono','Noto Sans KR',monospace","'Archivo Black','Space Mono',sans-serif",
       ["Space+Mono:wght@400;700","Archivo+Black","Noto+Sans+KR:wght@400;700"],"1.4"),
 "06":("글래스모피즘","Glassmorphism","https://fonts.google.com/specimen/Poppins",
       "'Poppins','Noto Sans KR',sans-serif","'Poppins','Noto Sans KR',sans-serif",
       ["Poppins:wght@400;500;600","Noto+Sans+KR:wght@400;500;700"],"1.25"),
 "07":("Braun 미니멀","Dieter Rams/Braun 미니멀리즘","https://en.wikipedia.org/wiki/Dieter_Rams",
       "'Archivo','Noto Sans KR',sans-serif","'Archivo','Noto Sans KR',sans-serif",
       ["Archivo:wght@400;500;600;700","Noto+Sans+KR:wght@400;500;700"],"1.5"),
 "08":("럭셔리 다크","고대비 개러몬드 세리프","https://fonts.google.com/specimen/Cormorant+Garamond",
       "'Cormorant Garamond','Nanum Myeongjo',serif","'Cormorant Garamond','Nanum Myeongjo',serif",
       ["Cormorant+Garamond:wght@500;600;700","Nanum+Myeongjo:wght@400;700;800"],"1.6"),
 "09":("레트로 픽셀","DEC VT320 비트맵(VT323)","https://fonts.google.com/specimen/VT323",
       "'DungGeunMo','VT323',monospace","'VT323','DungGeunMo',monospace",
       ["VT323","Press+Start+2P"],"1.2"),
 "10":("에디토리얼","매거진 디도네(Playfair)","https://fonts.google.com/specimen/Playfair+Display",
       "'Noto Serif KR','Playfair Display',serif","'Playfair Display','Noto Serif KR',serif",
       ["Playfair+Display:wght@500;700;900","Noto+Serif+KR:wght@400;600;900"],"1.618"),
 "11":("네이처 오가닉","가변 옵티컬 세리프(Fraunces)","https://fonts.google.com/specimen/Fraunces",
       "'Fraunces','Gowun Batang',serif","'Fraunces','Gowun Batang',serif",
       ["Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700","Gowun+Batang:wght@400;700"],"1.4"),
 "12":("뉴모피즘","Neumorphism 소프트 라운드(Nunito)","https://fonts.google.com/specimen/Nunito",
       "'Nunito','Noto Sans KR',sans-serif","'Nunito','Noto Sans KR',sans-serif",
       ["Nunito:wght@400;600;700;800","Noto+Sans+KR:wght@400;500;700"],"1.25"),
 "13":("오로라","그라디언트 다크(Space Grotesk)","https://fonts.google.com/specimen/Space+Grotesk",
       "'Space Grotesk','Noto Sans KR',sans-serif","'Space Grotesk','Noto Sans KR',sans-serif",
       ["Space+Grotesk:wght@400;500;700","Noto+Sans+KR:wght@400;500;700"],"1.3"),
 "14":("벤토","벤토 그리드 지오메트릭(Sora)","https://fonts.google.com/specimen/Sora",
       "'Sora','Noto Sans KR',sans-serif","'Sora','Noto Sans KR',sans-serif",
       ["Sora:wght@400;500;600;700","Noto+Sans+KR:wght@400;500;700"],"1.25"),
 "15":("클레이모피즘","Claymorphism 통통 라운드(Fredoka)","https://fonts.google.com/specimen/Fredoka",
       "'Fredoka','Jua',sans-serif","'Fredoka','Jua',sans-serif",
       ["Fredoka:wght@400;500;600;700","Jua"],"1.3"),
 "16":("Material 3","Material Design 3 (Roboto)","https://m3.material.io/styles/typography/",
       "'Roboto','Noto Sans KR',sans-serif","'Roboto','Noto Sans KR',sans-serif",
       ["Roboto:wght@400;500;700","Noto+Sans+KR:wght@400;500;700"],"1.25"),
 "17":("Y2K","Memphis/Y2K 테크노(Chakra Petch)","https://fonts.google.com/specimen/Chakra+Petch",
       "'Chakra Petch','Black Han Sans',sans-serif","'Chakra Petch','Black Han Sans',sans-serif",
       ["Chakra+Petch:wght@500;600;700","Black+Han+Sans"],"1.35"),
 "18":("스위스","International Typographic Style","https://en.wikipedia.org/wiki/International_Typographic_Style",
       "'Archivo','Helvetica Neue','Noto Sans KR',sans-serif","'Archivo','Helvetica Neue',sans-serif",
       ["Archivo:wght@400;500;600;700;800;900","Noto+Sans+KR:wght@400;500;700"],"1.5"),
 "19":("맥시멀리즘","맥시멀 라우드 디스플레이(Bungee)","https://fonts.google.com/specimen/Bungee",
       "'Space Grotesk','Black Han Sans',sans-serif","'Bungee','Black Han Sans',sans-serif",
       ["Bungee","Space+Grotesk:wght@400;500;700","Black+Han+Sans"],"1.5"),
 "20":("다크 애널리틱스","데이터 대시보드(IBM Plex Sans)","https://fonts.google.com/specimen/IBM+Plex+Sans",
       "'IBM Plex Sans','Noto Sans KR',sans-serif","'IBM Plex Sans','Noto Sans KR',sans-serif",
       ["IBM+Plex+Sans:wght@400;500;600","IBM+Plex+Mono:wght@400;500","Noto+Sans+KR:wght@400;500;700"],"1.15"),
 "21":("Riso 인쇄","Risograph 스팟 인쇄","https://fonts.google.com/specimen/Syne",
       "'Work Sans','Noto Sans KR',sans-serif","'Syne','Work Sans',sans-serif",
       ["Work+Sans:wght@400;500;600","Syne:wght@600;700;800","Noto+Sans+KR:wght@400;500;700"],"1.3"),
 "22":("De Stijl","De Stijl / 몬드리안","https://en.wikipedia.org/wiki/De_Stijl",
       "'Archivo','Noto Sans KR',sans-serif","'Archivo','Noto Sans KR',sans-serif",
       ["Archivo:wght@500;700;800;900","Noto+Sans+KR:wght@500;700;900"],"1.4"),
 "23":("IBM Carbon","IBM Carbon Design System","https://carbondesignsystem.com/",
       "'IBM Plex Sans','Noto Sans KR',sans-serif","'IBM Plex Sans','Noto Sans KR',sans-serif",
       ["IBM+Plex+Sans:wght@400;500;600","Noto+Sans+KR:wght@400;500;700"],"1.2"),
 "24":("Bauhaus","Bauhaus 기하 원색","https://en.wikipedia.org/wiki/Bauhaus",
       "'Poppins','Black Han Sans',sans-serif","'Bungee','Poppins',sans-serif",
       ["Poppins:wght@500;600;700","Bungee","Black+Han+Sans"],"1.45"),
 "25":("Shopify Polaris","Shopify Polaris","https://polaris.shopify.com/",
       "'Inter','Noto Sans KR',sans-serif","'Inter','Noto Sans KR',sans-serif",
       ["Inter:wght@400;500;600;700","Noto+Sans+KR:wght@400;500;700"],"1.2"),
 "26":("다크 미니멀","정갈 그로테스크 다크(Inter)","https://fonts.google.com/specimen/Inter",
       "'Inter','Noto Sans KR',sans-serif","'Inter','Noto Sans KR',sans-serif",
       ["Inter:wght@300;400;500;600","Noto+Sans+KR:wght@300;400;500"],"1.4"),
 "27":("웜 프로","따뜻한 옵티컬 세리프(Newsreader)","https://fonts.google.com/specimen/Newsreader",
       "'Newsreader','Gowun Batang',serif","'Newsreader','Gowun Batang',serif",
       ["Newsreader:opsz,wght@6..72,400;6..72,600;6..72,700","Gowun+Batang:wght@400;700"],"1.5"),
 "28":("접근성","Atkinson Hyperlegible(저시력 설계)","https://fonts.google.com/specimen/Atkinson+Hyperlegible",
       "'Atkinson Hyperlegible','Noto Sans KR',sans-serif","'Atkinson Hyperlegible','Noto Sans KR',sans-serif",
       ["Atkinson+Hyperlegible:wght@400;700","Noto+Sans+KR:wght@400;500;700"],"1.3"),
 "29":("Memphis","Memphis 디자인 80s","https://aesthetics.fandom.com/wiki/Memphis_Design",
       "'Fredoka','Jua',sans-serif","'Righteous','Fredoka',sans-serif",
       ["Fredoka:wght@500;600;700","Righteous","Jua"],"1.35"),
 "30":("Ant Design 밀집","Ant Design (고밀도)","https://ant.design/",
       "'Inter','Noto Sans KR',sans-serif","'Inter','Noto Sans KR',sans-serif",
       ["Inter:wght@400;500;600","Noto+Sans+KR:wght@400;500;700"],"1.125"),
 "31":("명조 웜","한국형 명조 세리프","https://fonts.google.com/specimen/Nanum+Myeongjo",
       "'Nanum Myeongjo',serif","'Nanum Myeongjo',serif",
       ["Nanum+Myeongjo:wght@400;700;800"],"1.5"),
}

# 산업라벨/약한 라이트 스타일 팔레트 재접지(출처값). key→{var:value}
OVER = {
 "02":{"--bg":"#FFFFFF","--surface":"#FFFFFF","--ink":"#0B0C0C","--muted":"#505A5F","--accent":"#1D70B8","--border":"#B1B4B6","--radius":"0px"},
 "03":{"--bg":"#FFFFFF","--surface":"#FFFFFF","--ink":"#09090B","--muted":"#71717A","--accent":"#18181B","--border":"#E4E4E7","--radius":"8px"},
 "05":{"--bg":"#FFFFFF","--surface":"#FFFFFF","--ink":"#000000","--muted":"#000000","--accent":"#FF5227","--border":"#000000","--radius":"0px"},
 "07":{"--bg":"#F4F4F2","--surface":"#FFFFFF","--ink":"#1A1A1A","--muted":"#7A7A78","--accent":"#E8500E","--border":"#DCDCD8","--radius":"0px"},
 "16":{"--bg":"#FEF7FF","--surface":"#FFFFFF","--ink":"#1D1B20","--muted":"#49454F","--accent":"#6750A4","--border":"#CAC4D0","--radius":"16px"},
 "21":{"--bg":"#F3EEE6","--surface":"#F3EEE6","--ink":"#1A1A2E","--muted":"#5B5B7A","--accent":"#FF4D6D","--border":"#1A1A2E","--radius":"0px"},
 "22":{"--bg":"#F5F2E9","--surface":"#FFFFFF","--ink":"#0A0A0A","--muted":"#333333","--accent":"#D8000C","--border":"#0A0A0A","--radius":"0px"},
 "23":{"--bg":"#FFFFFF","--surface":"#F4F4F4","--ink":"#161616","--muted":"#525252","--accent":"#0F62FE","--border":"#E0E0E0","--radius":"0px"},
 "24":{"--bg":"#F2EFE6","--surface":"#FFFFFF","--ink":"#1A1A1A","--muted":"#555555","--accent":"#E30613","--border":"#1A1A1A","--radius":"0px"},
 "25":{"--bg":"#F6F6F7","--surface":"#FFFFFF","--ink":"#202223","--muted":"#6D7175","--accent":"#008060","--border":"#E1E3E5","--radius":"8px"},
 "29":{"--bg":"#FDF3E7","--surface":"#FFFFFF","--ink":"#1B1B3A","--muted":"#6A6A8A","--accent":"#FF3D7F","--border":"#1B1B3A","--radius":"12px"},
 "30":{"--bg":"#FFFFFF","--surface":"#FAFAFA","--ink":"#1F1F1F","--muted":"#8C8C8C","--accent":"#1677FF","--border":"#F0F0F0","--radius":"2px"},
}

def patch(nn):
    p = f"{TOK}/style-{nn}.css"
    if not os.path.exists(p): return None
    s = open(p, encoding="utf-8").read()
    name, src, url, body, ui, gf, ts = FONT[nn]
    # 기존 @gfont 헤더 제거 후 새로 주입
    s = re.sub(r'/\* @gfont [^\n]*\*/\n', '', s)
    header = "".join(f"/* @gfont {g} */\n" for g in gf)
    # 파일 최상단(첫 주석 다음)에 gfont 헤더 삽입
    s = re.sub(r'(\A/\*[^\n]*\*/\n)', r'\1' + header, s, count=1)
    # 폰트/스케일 교체
    s = re.sub(r'--font:\s*[^;]+;', f"--font:{body};", s)
    s = re.sub(r'--font-ui:\s*[^;]+;', f"--font-ui:{ui};", s)
    if '--font-ui' not in s:
        s = s.replace(f"--font:{body};", f"--font:{body};\n  --font-ui:{ui};")
    s = re.sub(r'--type-scale:\s*[^;]+;', f"--type-scale:{ts};", s)
    # 팔레트 재접지(해당되면)
    for var, val in OVER.get(nn, {}).items():
        if re.search(rf'{var}:\s*[^;]+;', s):
            s = re.sub(rf'{re.escape(var)}:\s*[^;]+;', f"{var}:{val};", s)
    open(p, "w", encoding="utf-8").write(s)
    return name

done = []
for nn in sorted(FONT):
    n = patch(nn)
    if n: done.append((nn, n))
print(f"패치 {len(done)}개:")
for nn, n in done:
    print(f"  {nn} {n}")
