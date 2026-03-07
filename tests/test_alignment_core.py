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


EXPECTED_JS_VERSION = "2.5.8"


def _resolve_js_package_path() -> Path:
    candidate_paths = []
    env_path = os.environ.get("IZTRO_JS_PACKAGE")
    if env_path:
        candidate_paths.append(Path(env_path))
    candidate_paths.extend(
        [
            Path(f"/tmp/iztro-{EXPECTED_JS_VERSION}/node_modules/iztro"),
            REPO_ROOT / "node_modules" / "iztro",
        ]
    )

    problems = []
    for path in candidate_paths:
        package_json = path / "package.json"
        if not package_json.exists():
            problems.append(f"{path} (missing package.json)")
            continue
        package = json.loads(package_json.read_text(encoding="utf-8"))
        version = package.get("version")
        if version == EXPECTED_JS_VERSION:
            return path
        problems.append(f"{path} (found {version}, expected {EXPECTED_JS_VERSION})")

    searched = "\n".join(f"- {problem}" for problem in problems) or "- <no candidates>"
    raise AssertionError(
        "Missing iztro JS reference package.\n"
        f"Expected version: {EXPECTED_JS_VERSION}\n"
        "Searched:\n"
        f"{searched}\n"
        "Install iztro or set IZTRO_JS_PACKAGE explicitly."
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
    js_package_path = _resolve_js_package_path()
    script = REPO_ROOT / "scripts" / "compare_iztro_alignment.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        env={**os.environ, "IZTRO_JS_PACKAGE": str(js_package_path)},
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
