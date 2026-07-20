from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "skills/copy-angle-explorer/references/hero-template.md"

def test_template_defines_contract_classes():
    s = T.read_text(encoding="utf-8")
    for cls in ("cx-headline", "cx-sub", "cx-cta"):
        assert cls in s, f"{cls} 누락 — copy-lint 파싱 계약"

def test_template_footer_slot_present():
    assert "ANGLE" in T.read_text(encoding="utf-8")
