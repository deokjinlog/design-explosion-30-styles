#!/usr/bin/env python3
"""pytest 없이도 tests/ 를 돌린다.

테스트는 pytest 스타일(맨 함수 `test_*`)이라 `unittest discover` 로는 0건이 나온다.
기여자 머신에 pytest 가 없다는 이유로 게이트를 건너뛰게 두지 않으려고 둔 최소 러너다.

    python3 tests/run.py
"""
import importlib.util
import inspect
import sys
import tempfile
import traceback
from pathlib import Path

TESTS = Path(__file__).resolve().parent


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    passed, failed = 0, []
    for f in sorted(TESTS.glob("test_*.py")):
        mod = load(f)
        for name in sorted(n for n in dir(mod) if n.startswith("test_")):
            fn = getattr(mod, name)
            if not callable(fn):
                continue
            # pytest 의 tmp_path 픽스처만 흉내 낸다 (이 레포가 쓰는 유일한 픽스처)
            args = list(inspect.signature(fn).parameters)
            unknown = [a for a in args if a != "tmp_path"]
            if unknown:
                failed.append((f.name, name, f"지원하지 않는 픽스처: {unknown} — pytest 로 돌리세요\n"))
                continue
            try:
                if args:
                    with tempfile.TemporaryDirectory() as d:
                        fn(Path(d))
                else:
                    fn()
                passed += 1
            except Exception:
                failed.append((f.name, name, traceback.format_exc()))
    for fname, name, tb in failed:
        print(f"\n[FAIL] {fname}::{name}\n{tb}")
    print(f"\n{passed} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
