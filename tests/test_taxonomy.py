import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "skills/copy-angle-explorer/references/angle-taxonomy.md"

def test_taxonomy_has_30_numbered_angles():
    nums = set(re.findall(r"\b(0[1-9]|[12]\d|30)\b", T.read_text(encoding="utf-8")))
    assert len(nums) == 30, f"각도 번호 {len(nums)}개 (30 필요)"

def test_taxonomy_names_six_families():
    s = T.read_text(encoding="utf-8")
    for fam in ("감정", "논리", "사회적", "서사", "인지", "구조"):
        assert fam in s
