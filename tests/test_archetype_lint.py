import subprocess, sys, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills/design-style-explorer/scripts/archetype-lint.py"

DASHBOARD = """<html><body>
<div class="kpi-card">전주 대비 +12%</div>
<div>구성비 도넛</div><div>목표 달성률 65%</div><table><tbody></tbody></table>
</body></html>"""

CHAT_ATTR = """<html><body>
<section data-region="conversation"><div>기다림이 힘든 건가요?</div></section>
<div data-region="composer"><textarea></textarea></div>
</body></html>"""

CHAT_LEGACY = """<html><body>
<div class="chat-log"><div class="bubble">기다림이 힘든 건가요?</div></div>
<textarea placeholder="보내기"></textarea></body></html>"""


def _run(path, code=None):
    cmd = [sys.executable, str(SCRIPT), str(path)]
    if code:
        cmd += ["--archetype", code]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout


def test_dashboard_content_fails_conversational(tmp_path):
    f = tmp_path / "style-01-x.html"; f.write_text(DASHBOARD, encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 1 and "KPI" in out


def test_dashboard_content_passes_dashboard(tmp_path):
    f = tmp_path / "style-01-x.html"; f.write_text(DASHBOARD, encoding="utf-8")
    assert _run(f, "A")[0] == 0


def test_attribute_mode_is_deterministic(tmp_path):
    f = tmp_path / "style-01-x.html"; f.write_text(CHAT_ATTR, encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 0 and "속성 모드" in out


def test_keyword_fallback_for_legacy_files(tmp_path):
    f = tmp_path / "style-01-x.html"; f.write_text(CHAT_LEGACY, encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 0 and "키워드추측 모드" in out


def test_html_comment_does_not_false_positive(tmp_path):
    """설계 주석에 'KPI' 라고 써도 걸리면 안 된다 (실제 겪은 오탐)."""
    f = tmp_path / "style-01-x.html"
    f.write_text(CHAT_ATTR.replace("<body>", "<body><!-- KPI·도넛·달성률 넣지 말 것 -->"), encoding="utf-8")
    assert _run(f, "B")[0] == 0


def test_forbidden_region_attribute_is_caught(tmp_path):
    """data-region 으로 대놓고 박은 금지 영역도 잡는다."""
    f = tmp_path / "style-01-x.html"
    f.write_text(CHAT_ATTR.replace("</body>", '<div data-region="kpi">지표</div></body>'), encoding="utf-8")
    rc, out = _run(f, "B")
    assert rc == 1 and 'data-region="kpi"' in out


def test_new_archetypes_exist(tmp_path):
    """Enrico 로 보완한 신규 원형 I·J·K 가 동작한다."""
    f = tmp_path / "x.html"
    f.write_text('<html><body><div data-region="auth-form">로그인</div><div data-region="brand">로고</div></body></html>', encoding="utf-8")
    assert _run(f, "J")[0] == 0


def test_reads_archetype_from_spec_json(tmp_path):
    (tmp_path / "_spec.json").write_text(json.dumps({"archetype": "B"}), encoding="utf-8")
    (tmp_path / "style-01-x.html").write_text(DASHBOARD, encoding="utf-8")
    rc, out = _run(tmp_path)
    assert rc == 1 and "대화형" in out


def test_required_region_absence_fails_in_attribute_mode(tmp_path):
    """속성 모드에선 필수 영역 부재도 FAIL — 폼(E)을 피드(F)라 우기면 잡혀야."""
    f = tmp_path / "style-01-x.html"
    f.write_text('<html><body><form data-region="form"><input></form></body></html>', encoding="utf-8")
    rc, out = _run(f, "F")   # F 필수: feed·feed-item — 둘 다 없음
    assert rc == 1 and ("feed" in out or "피드" in out)
