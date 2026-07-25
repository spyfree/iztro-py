import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from iztro_py import astro  # noqa: E402


EXPECTED_JS_VERSION = "2.5.8"

# The JS reference is an optional local dev dependency (`npm install`), so a
# developer without it gets a skip rather than a spurious failure. CI sets
# IZTRO_REQUIRE_JS_REFERENCE=1 so a missing reference is a hard error there and
# the alignment suite can never silently stop running.
_REQUIRE_JS_REFERENCE = os.environ.get("IZTRO_REQUIRE_JS_REFERENCE") == "1"

_ALIGNMENT_SCRIPT = REPO_ROOT / "scripts" / "compare_iztro_alignment.py"


def _unavailable(reason: str):
    """Fail in CI, skip elsewhere."""
    if _REQUIRE_JS_REFERENCE:
        pytest.fail(f"{reason}\n(IZTRO_REQUIRE_JS_REFERENCE=1 turns this skip into a failure)")
    pytest.skip(reason)


def _resolve_js_package_path() -> Path:
    if shutil.which("node") is None:
        _unavailable("node is not installed; cannot run the iztro JS reference.")

    # Reuse the script's resolver so the search paths and the "is it actually
    # requireable" check can never drift between the test and the script.
    spec = importlib.util.spec_from_file_location("_iztro_alignment_script", _ALIGNMENT_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError as exc:
        _unavailable(str(exc))
    return module.JS_PACKAGE_PATH


def _summarize(chart):
    return {
        "five_elements_class": chart.five_elements_class,
        "chinese_date": chart.chinese_date,
        "soul_index": chart.get_soul_palace().index,
        "body_index": chart.get_body_palace().index,
        "palaces": [
            {
                "index": palace.index,
                "major": [star.name for star in palace.major_stars],
                "minor": [star.name for star in palace.minor_stars],
                "decadal": list(palace.decadal.range) if palace.decadal else None,
                "ages": list(palace.ages),
            }
            for palace in chart.palaces
        ],
    }


def test_core_alignment_against_js_snapshot():
    js_package_path = _resolve_js_package_path()
    result = subprocess.run(
        [sys.executable, str(_ALIGNMENT_SCRIPT)],
        cwd=REPO_ROOT,
        env={**os.environ, "IZTRO_JS_PACKAGE": str(js_package_path)},
        capture_output=True,
        text=True,
    )
    # stderr first: on a harness failure (bad node, broken package) stdout is
    # empty and the traceback is what actually matters.
    assert result.returncode == 0, f"stderr:\n{result.stderr}\nstdout:\n{result.stdout}"

    payload = json.loads(result.stdout)
    assert payload, "alignment script should emit case results"
    assert all(not case["blocking_diffs"] for case in payload)


def test_by_solar_hour_maps_boundary_hours_correctly():
    base_shen = _summarize(astro.by_solar("1990-10-21", 8, "女"))
    assert _summarize(astro.by_solar_hour("1990-10-21", 15, "女")) == base_shen
    assert _summarize(astro.by_solar_hour("1990-10-21", 16, "女")) == base_shen

    early_rat = _summarize(astro.by_solar("1990-10-21", 0, "女"))
    late_rat = _summarize(astro.by_solar("1990-10-21", 12, "女"))
    assert _summarize(astro.by_solar_hour("1990-10-21", 0, "女")) == early_rat
    assert _summarize(astro.by_solar_hour("1990-10-21", 23, "女")) == late_rat
