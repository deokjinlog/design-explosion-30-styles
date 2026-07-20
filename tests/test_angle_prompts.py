from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
P = ROOT / "skills/copy-angle-explorer/references/prompts"

REQUIRED = ["각도명", "패밀리", "설득 구조", "헤드라인 공식", "톤", "좋은 예", "나쁜 예", "금지", "크리틱"]

def test_exactly_30_angle_files():
    files = sorted(P.glob("angle-*.md"))
    assert len(files) == 30, f"각도 파일 {len(files)}개 (30 필요)"

def test_angle01_has_all_schema_sections():
    s = (P / "angle-01-fear.md").read_text(encoding="utf-8")
    missing = [k for k in REQUIRED if k not in s]
    assert not missing, f"angle-01 누락 섹션: {missing}"

def test_all_present_angle_files_follow_schema():
    for f in P.glob("angle-*.md"):
        s = f.read_text(encoding="utf-8")
        missing = [k for k in REQUIRED if k not in s]
        assert not missing, f"{f.name} 누락 섹션: {missing}"
