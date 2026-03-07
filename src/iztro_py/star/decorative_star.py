"""
Decorative 12-god assignments for iztro-py.

These fields are stored directly on each palace, following iztro@2.5.8 birth
chart output for the default algorithm.
"""

from typing import Any, Dict, List

from iztro_py.data.types import EarthlyBranchName, FiveElementsClass, GenderName, HeavenlyStemName
from iztro_py.i18n import t
from iztro_py.star.location import (
    get_minor_star_positions_lucun_yangtuo_tianma,
)
from iztro_py.utils.helpers import fix_earthly_branch_index
from iztro_py.data.constants import EARTHLY_BRANCHES, HEAVENLY_STEMS, fix_index


def _same_yinyang(gender: GenderName, year_branch: EarthlyBranchName) -> bool:
    return (gender == "男" and EARTHLY_BRANCHES.index(year_branch) % 2 == 0) or (
        gender == "女" and EARTHLY_BRANCHES.index(year_branch) % 2 == 1
    )


def get_changsheng12(
    five_elements_class: FiveElementsClass,
    gender: GenderName,
    year_branch: EarthlyBranchName,
) -> List[str]:
    """Return 长生 12 神 from 寅宫=0 order."""
    starts = {
        FiveElementsClass.WATER_2: fix_earthly_branch_index("shenEarthly"),
        FiveElementsClass.WOOD_3: fix_earthly_branch_index("haiEarthly"),
        FiveElementsClass.METAL_4: fix_earthly_branch_index("siEarthly"),
        FiveElementsClass.EARTH_5: fix_earthly_branch_index("shenEarthly"),
        FiveElementsClass.FIRE_6: fix_earthly_branch_index("yinEarthly"),
    }
    names = [
        "changsheng",
        "muyu",
        "guandai",
        "linguan",
        "diwang",
        "shuai",
        "bing",
        "si",
        "mu",
        "jue",
        "tai",
        "yang",
    ]
    start = starts[five_elements_class]
    forward = _same_yinyang(gender, year_branch)
    result = [""] * 12
    for i, name in enumerate(names):
        index = fix_index(start + i) if forward else fix_index(start - i)
        result[index] = t(name)
    return result


def get_boshi12(
    year_stem: HeavenlyStemName,
    year_branch: EarthlyBranchName,
    gender: GenderName,
) -> List[str]:
    """Return 博士 12 神 from 寅宫=0 order."""
    names = [
        "boshi",
        "lishi",
        "qinglong",
        "xiaohao",
        "jiangjun",
        "zhoushu",
        "faylian",
        "xishen",
        "bingfu",
        "dahao",
        "fubing",
        "guanfu",
    ]
    lu_index, _, _, _ = get_minor_star_positions_lucun_yangtuo_tianma(
        HEAVENLY_STEMS.index(year_stem),
        EARTHLY_BRANCHES.index(year_branch),
    )
    forward = _same_yinyang(gender, year_branch)
    result = [""] * 12
    for i, name in enumerate(names):
        index = fix_index(lu_index + i) if forward else fix_index(lu_index - i)
        result[index] = t(name)
    return result


def get_jiangqian12(year_branch: EarthlyBranchName) -> List[str]:
    """Return 将前 12 神 from 寅宫=0 order."""
    if year_branch in ["yinEarthly", "wuEarthly", "xuEarthly"]:
        start = fix_earthly_branch_index("wuEarthly")
    elif year_branch in ["shenEarthly", "ziEarthly", "chenEarthly"]:
        start = fix_earthly_branch_index("ziEarthly")
    elif year_branch in ["siEarthly", "youEarthly", "chouEarthly"]:
        start = fix_earthly_branch_index("youEarthly")
    else:
        start = fix_earthly_branch_index("maoEarthly")

    names = [
        "jiangxing",
        "panan",
        "suiyi",
        "xishenJiang",
        "huagai",
        "jiesha",
        "zhaisha",
        "tiansha",
        "zhibei",
        "xianchi",
        "yuesha",
        "wangshen",
    ]
    result = [""] * 12
    for i, name in enumerate(names):
        result[fix_index(start + i)] = t(name)
    return result


def get_suiqian12(year_branch: EarthlyBranchName) -> List[str]:
    """Return 岁前 12 神 from 寅宫=0 order."""
    names = [
        "suijian",
        "huiqi",
        "sangmen",
        "guansuo",
        "gwanfu",
        "xiaohao",
        "dahao",
        "longde",
        "baihu",
        "tiande",
        "diaoke",
        "bingfu",
    ]
    start = fix_earthly_branch_index(year_branch)
    result = [""] * 12
    for i, name in enumerate(names):
        result[fix_index(start + i)] = t(name)
    return result


def apply_decorative_stars(
    palaces: List[Dict[str, Any]],
    five_elements_class: FiveElementsClass,
    gender: GenderName,
    year_stem: HeavenlyStemName,
    year_branch: EarthlyBranchName,
) -> None:
    """Populate changsheng12 / boshi12 / jiangqian12 / suiqian12 on palaces."""
    changsheng12 = get_changsheng12(five_elements_class, gender, year_branch)
    boshi12 = get_boshi12(year_stem, year_branch, gender)
    jiangqian12 = get_jiangqian12(year_branch)
    suiqian12 = get_suiqian12(year_branch)

    for i, palace in enumerate(palaces):
        palace["changsheng12"] = changsheng12[i]
        palace["boshi12"] = boshi12[i]
        palace["jiangqian12"] = jiangqian12[i]
        palace["suiqian12"] = suiqian12[i]
