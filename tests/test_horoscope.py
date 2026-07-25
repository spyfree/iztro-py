"""
Test horoscope (运势) system.

所有期望值均取自 iztro@2.5.8 默认配置。

注意：本文件此前四个测试全部只有 print、没有任何断言，只要不抛异常就算通过，
却在末尾无条件打印「测试通过」。运势系统实际上处于零覆盖状态。
"""

import pytest

from iztro_py import astro

# (出生日, 时辰, 性别, 查询日, 查询时辰) -> 期望值
CASES = [
    (
        ("2000-8-16", 6, "男", "2024-1-1", 6),
        {
            "nominal_age": 24,
            "indices": {
                "decadal": 1,
                "age": 7,
                "yearly": 1,
                "monthly": 11,
                "daily": 6,
                "hourly": 0,
            },
            "decadal_ganzhi": ("jiHeavenly", "maoEarthly"),
            "yearly_ganzhi": ("guiHeavenly", "maoEarthly"),
            "decadal_mutagen": ["wuquMaj", "tanlangMaj", "tianliangMaj", "wenquMin"],
            "yearly_mutagen": ["pojunMaj", "jumenMaj", "taiyinMaj", "tanlangMaj"],
        },
    ),
    (
        ("2000-8-16", 6, "男", "2024-6-15", 6),
        {
            "nominal_age": 25,
            "indices": {"decadal": 2, "age": 8, "yearly": 2, "monthly": 6, "daily": 3, "hourly": 9},
            "decadal_ganzhi": ("gengHeavenly", "chenEarthly"),
            "yearly_ganzhi": ("jiaHeavenly", "chenEarthly"),
            "decadal_mutagen": ["taiyangMaj", "wuquMaj", "taiyinMaj", "tiantongMaj"],
            "yearly_mutagen": ["lianzhenMaj", "pojunMaj", "wuquMaj", "taiyangMaj"],
        },
    ),
    (
        ("1990-1-1", 0, "女", "2020-1-1", 0),
        {
            "nominal_age": 31,
            "indices": {
                "decadal": 1,
                "age": 11,
                "yearly": 9,
                "monthly": 9,
                "daily": 3,
                "hourly": 3,
            },
            "decadal_ganzhi": ("dingHeavenly", "maoEarthly"),
            "yearly_ganzhi": ("jiHeavenly", "haiEarthly"),
            "decadal_mutagen": ["taiyinMaj", "tiantongMaj", "tianjiMaj", "jumenMaj"],
            "yearly_mutagen": ["wuquMaj", "tanlangMaj", "tianliangMaj", "wenquMin"],
        },
    ),
    (
        ("1990-1-1", 0, "女", "2024-1-1", 0),
        {
            "nominal_age": 35,
            "indices": {"decadal": 2, "age": 7, "yearly": 1, "monthly": 0, "daily": 7, "hourly": 7},
            "decadal_ganzhi": ("wuHeavenly", "chenEarthly"),
            "yearly_ganzhi": ("guiHeavenly", "maoEarthly"),
            "decadal_mutagen": ["tanlangMaj", "taiyinMaj", "youbiMin", "tianjiMaj"],
            "yearly_mutagen": ["pojunMaj", "jumenMaj", "taiyinMaj", "tanlangMaj"],
        },
    ),
]

IDS = [f"{c[0][0]}-ti{c[0][1]}-{c[0][2]}->{c[0][3]}" for c in CASES]


def _horoscope(params):
    birth_date, birth_time, gender, query_date, query_time = params
    chart = astro.by_solar(birth_date, birth_time, gender)
    return chart.horoscope(query_date, query_time)


@pytest.mark.parametrize("params,expected", CASES, ids=IDS)
def test_nominal_age(params, expected):
    assert _horoscope(params).nominal_age == expected["nominal_age"]


@pytest.mark.parametrize("params,expected", CASES, ids=IDS)
def test_all_six_scopes_land_on_the_expected_palace(params, expected):
    horoscope = _horoscope(params)
    actual = {
        scope: getattr(horoscope, scope).index
        for scope in ("decadal", "age", "yearly", "monthly", "daily", "hourly")
    }
    assert actual == expected["indices"]


@pytest.mark.parametrize("params,expected", CASES, ids=IDS)
def test_decadal_and_yearly_ganzhi(params, expected):
    horoscope = _horoscope(params)
    assert (horoscope.decadal.heavenly_stem, horoscope.decadal.earthly_branch) == expected[
        "decadal_ganzhi"
    ]
    assert (horoscope.yearly.heavenly_stem, horoscope.yearly.earthly_branch) == expected[
        "yearly_ganzhi"
    ]


@pytest.mark.parametrize("params,expected", CASES, ids=IDS)
def test_decadal_and_yearly_mutagen(params, expected):
    horoscope = _horoscope(params)
    assert horoscope.decadal.mutagen == expected["decadal_mutagen"]
    assert horoscope.yearly.mutagen == expected["yearly_mutagen"]


@pytest.mark.parametrize("params,expected", CASES, ids=IDS)
def test_palace_names_rotate_from_the_item_index(params, expected):
    """每个运限项的 palace_names 以该项落宫为命宫重排十二宫。"""
    horoscope = _horoscope(params)
    for scope in ("decadal", "age", "yearly", "monthly", "daily", "hourly"):
        item = getattr(horoscope, scope)
        assert len(item.palace_names) == 12
        assert len(set(item.palace_names)) == 12
        assert item.palace_names[item.index] == "soulPalace"


def test_male_and_female_decadals_run_in_opposite_directions():
    """同一天出生的男女命，大限顺逆不同，落宫应不同。"""
    male = astro.by_solar("2000-8-16", 6, "男").horoscope("2024-1-1", 6)
    female = astro.by_solar("2000-8-16", 6, "女").horoscope("2024-1-1", 6)

    assert male.nominal_age == female.nominal_age == 24
    assert male.decadal.index == 1
    assert female.decadal.index == 11
    assert male.age.index == 7
    assert female.age.index == 9
    # 流年只看流年干支，与性别无关
    assert male.yearly.index == female.yearly.index == 1


def test_decadal_advances_by_one_palace_every_ten_years():
    chart = astro.by_solar("2000-8-16", 6, "男")
    seen = [chart.horoscope(f"{year}-6-1", 6).decadal.index for year in (2024, 2034, 2044)]
    assert seen == [2, 3, 4]


def test_horoscope_indices_address_real_palaces():
    """运限索引必须能在星盘上取到宫位，且三方四正可用。"""
    chart = astro.by_solar("2000-8-16", 6, "男")
    horoscope = chart.horoscope("2024-6-15", 6)

    for scope in ("decadal", "age", "yearly", "monthly", "daily", "hourly"):
        index = getattr(horoscope, scope).index
        palace = chart.palace(index)
        assert palace is not None, scope
        assert palace.index == index

    surrounded = chart.surrounded_palaces(horoscope.yearly.index)
    assert surrounded is not None
    assert [p.index for p in surrounded.all_palaces()] == [2, 8, 10, 6]


def test_reported_lunar_date_matches_the_query_date():
    chart = astro.by_solar("2000-8-16", 6, "男")
    horoscope = chart.horoscope("2024-6-15", 6)
    assert horoscope.solar_date == "2024-6-15"
    assert horoscope.lunar_date == "二〇二四年五月初十"
