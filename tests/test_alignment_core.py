import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from iztro_py import astro  # noqa: E402


JS_PACKAGE_PATH = Path(
    os.environ.get("IZTRO_JS_PACKAGE", "/tmp/iztro-2.5.8/node_modules/iztro")
)


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
    if not JS_PACKAGE_PATH.exists():
        raise AssertionError(f"Missing JS reference package at {JS_PACKAGE_PATH}")

    script = REPO_ROOT / "scripts" / "compare_iztro_alignment.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        env={**os.environ, "IZTRO_JS_PACKAGE": str(JS_PACKAGE_PATH)},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

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
