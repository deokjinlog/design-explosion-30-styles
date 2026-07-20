import subprocess, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/design-style-explorer/scripts/archetype-lint.py"

DASHBOARD = """<html><body>
<div class="kpi-card">전주 대비 +12%</div>
<div>구성비 도넛</div><div>목표 달성률 65%</div>
</body></html>"""

CHAT = """<html><body>
<div class="chat-log"><div class="bubble">기다림이 힘든 건가요?</div></div>
<p>%s</p></body></html>""" % ("이야기 본문입니다. " * 30)


def _run(path, code):
    r = subprocess.run([sys.executable, str(SCRIPT), str(path), "--archetype", code],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def test_dashboard_content_fails_conversational_archetype(tmp_path):
    f = tmp_path / "style-01-x.html"
    f.write_text(DASHBOARD, encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 1, out
    assert "KPI" in out and "이식" in out


def test_dashboard_content_passes_dashboard_archetype(tmp_path):
    f = tmp_path / "style-01-x.html"
    f.write_text(DASHBOARD, encoding="utf-8")
    rc, out = _run(f, "A")
    assert rc == 0, out


def test_chat_content_passes_conversational_archetype(tmp_path):
    f = tmp_path / "style-01-x.html"
    f.write_text(CHAT, encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 0, out


def test_reads_archetype_from_spec_json(tmp_path):
    (tmp_path / "_spec.json").write_text(json.dumps({"archetype": "B"}), encoding="utf-8")
    (tmp_path / "style-01-x.html").write_text(DASHBOARD, encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 1
    assert "대화형" in r.stdout
