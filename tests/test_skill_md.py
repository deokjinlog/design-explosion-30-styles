from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "skills/copy-angle-explorer/SKILL.md"

def test_frontmatter_has_name_and_description():
    s = S.read_text(encoding="utf-8")
    assert s.startswith("---")
    assert "name: copy-angle-explorer" in s
    assert "description:" in s

def test_workflow_covers_lint_and_gallery():
    s = S.read_text(encoding="utf-8")
    assert "copy_lint.py" in s
    assert "gallery.html" in s
