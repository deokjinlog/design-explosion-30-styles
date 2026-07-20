import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def _html(headline, sub, ctas=1):
    cta = '<a class="cx-cta" href="#">시작하기</a>' * ctas
    return f'<h1 class="cx-headline">{headline}</h1><p class="cx-sub">{sub}</p>{cta}'

def test_extract_hero_pulls_headline_sub_and_ctas():
    hero = cl.extract_hero(_html("헤드라인", "서브카피", ctas=1))
    assert hero["headline"] == "헤드라인"
    assert hero["sub"] == "서브카피"
    assert len(hero["ctas"]) == 1

def test_headline_over_limit_is_fail():
    long_headline = "가" * 61
    fails = cl.hero_violations(cl.extract_hero(_html(long_headline, "짧은 서브")))
    assert any("헤드라인" in f for f in fails)

def test_two_ctas_is_fail():
    fails = cl.hero_violations(cl.extract_hero(_html("헤드라인", "서브", ctas=2)))
    assert any("CTA" in f for f in fails)

def test_clean_hero_has_no_violation():
    fails = cl.hero_violations(cl.extract_hero(_html("적당한 헤드라인", "적당한 서브카피")))
    assert fails == []
