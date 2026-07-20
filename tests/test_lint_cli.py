import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills/copy-angle-explorer/scripts"))
import copy_lint as cl

def _write_case(tmp_path, headline, facts):
    (tmp_path / "spec.json").write_text(json.dumps({"facts": facts, "language": "ko"}), encoding="utf-8")
    html = f'<h1 class="cx-headline">{headline}</h1><p class="cx-sub">서브</p><a class="cx-cta" href="#">A</a>'
    p = tmp_path / "angle-01-fear.html"
    p.write_text(html, encoding="utf-8")
    return p

def test_lint_flags_invented_number(tmp_path):
    p = _write_case(tmp_path, "고객 9999명 돌파", facts=["무료 체험"])
    fails, warns = cl.lint(p, cl.load_spec(tmp_path))
    assert any("9999" in f for f in fails)

def test_lint_clean_passes(tmp_path):
    p = _write_case(tmp_path, "지금 무료로 시작하세요", facts=["무료 체험"])
    fails, warns = cl.lint(p, cl.load_spec(tmp_path))
    assert fails == []

def test_load_spec_missing_returns_empty_facts(tmp_path):
    assert cl.load_spec(tmp_path) == {"facts": [], "language": "ko"}
