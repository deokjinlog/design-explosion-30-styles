import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def test_number_not_in_whitelist_is_fail():
    fails, warns = cl.claim_violations("가입 고객 10000명 돌파", facts=["무료 체험 제공"])
    assert any("10000" in f for f in fails)

def test_number_in_whitelist_passes():
    fails, warns = cl.claim_violations("가입 고객 10000명 돌파", facts=["가입 고객 10000명"])
    assert fails == []

def test_superlative_not_in_whitelist_is_fail():
    fails, warns = cl.claim_violations("업계 1위 솔루션", facts=["빠른 처리 속도"])
    assert any("1위" in f or "업계" in f for f in fails)

def test_latin_propernoun_is_warn_not_fail():
    fails, warns = cl.claim_violations("Samsung 도 쓰는 도구", facts=["누구나 쓴다"])
    assert fails == []
    assert any("Samsung" in w for w in warns)
