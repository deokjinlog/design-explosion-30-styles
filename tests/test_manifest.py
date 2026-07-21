import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def test_plugin_manifest_valid():
    data = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert data["name"] == "design-explosion-30-styles"
    assert "claude-code-plugin" in data["keywords"]

def test_marketplace_lists_plugin():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    names = [p["name"] for p in data["plugins"]]
    assert "design-explosion-30-styles" in names

def test_design_skill_present():
    assert (ROOT / "skills/design-style-explorer/SKILL.md").exists()
