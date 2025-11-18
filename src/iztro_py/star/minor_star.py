"""
Minor stars placement for iztro-py

Functions for placing the 14 minor stars (辅星) into palaces.
"""

from typing import Any, Dict, List, Optional
from iztro_py.data.types import Star, HeavenlyStemName, EarthlyBranchName
from iztro_py.data.constants import HEAVENLY_STEMS, EARTHLY_BRANCHES
from iztro_py.star.location import (
    get_minor_star_position_zuofu,
    get_minor_star_position_youbi,
    get_minor_star_position_wenchang,
    get_minor_star_position_wenqu,
    get_minor_star_positions_kuiyue,
    get_minor_star_positions_huoling,
    get_minor_star_positions_kongjie,
    get_minor_star_positions_lucun_yangtuo_tianma,
)


def _find_palace_by_branch_index(
    palaces: List[Dict[str, Any]], branch_index: int
) -> Optional[Dict[str, Any]]:
    """
    根据地支索引查找对应的宫位

    Args:
        palaces: 宫位列表
        branch_index: 地支索引 (0-11)

    Returns:
        对应的宫位字典，如果未找到则返回None
    """
    target_branch = EARTHLY_BRANCHES[branch_index]
    for palace in palaces:
        if palace["earthly_branch"] == target_branch:
            return palace
    return None


def place_minor_stars(
    palaces: List[Dict[str, Any]],
    lunar_month: int,
    time_index: int,
    year_stem: HeavenlyStemName,
    year_branch: EarthlyBranchName,
) -> None:
    """
    将14颗辅星安置到宫位中

    Args:
        palaces: 宫位列表
        lunar_month: 农历月
        time_index: 时辰索引
        year_stem: 年干
        year_branch: 年支

    Note:
        直接修改palaces列表，不返回值
    """
    year_stem_index = HEAVENLY_STEMS.index(year_stem)
    year_branch_index = EARTHLY_BRANCHES.index(year_branch)

    # 1. 左辅、右弼（按农历月）
    zuofu_index = get_minor_star_position_zuofu(lunar_month)
    youbi_index = get_minor_star_position_youbi(lunar_month)

    zuofu_palace = _find_palace_by_branch_index(palaces, zuofu_index)
    if zuofu_palace:
        zuofu_palace["minor_stars"].append(Star(name="zuofuMin", type="soft", scope="origin"))

    youbi_palace = _find_palace_by_branch_index(palaces, youbi_index)
    if youbi_palace:
        youbi_palace["minor_stars"].append(Star(name="youbiMin", type="soft", scope="origin"))

    # 2. 文昌、文曲（按时辰）
    wenchang_index = get_minor_star_position_wenchang(time_index)
    wenqu_index = get_minor_star_position_wenqu(time_index)

    wenchang_palace = _find_palace_by_branch_index(palaces, wenchang_index)
    if wenchang_palace:
        wenchang_palace["minor_stars"].append(Star(name="wenchangMin", type="soft", scope="origin"))

    wenqu_palace = _find_palace_by_branch_index(palaces, wenqu_index)
    if wenqu_palace:
        wenqu_palace["minor_stars"].append(Star(name="wenquMin", type="soft", scope="origin"))

    # 3. 天魁、天钺（按年干）
    kuai_index, yue_index = get_minor_star_positions_kuiyue(year_stem_index)

    kuai_palace = _find_palace_by_branch_index(palaces, kuai_index)
    if kuai_palace:
        kuai_palace["minor_stars"].append(Star(name="tiankuiMin", type="soft", scope="origin"))

    yue_palace = _find_palace_by_branch_index(palaces, yue_index)
    if yue_palace:
        yue_palace["minor_stars"].append(Star(name="tianyueMin", type="soft", scope="origin"))

    # 4. 火星、铃星（按年支和时辰）
    huo_index, ling_index = get_minor_star_positions_huoling(year_branch_index, time_index)

    huo_palace = _find_palace_by_branch_index(palaces, huo_index)
    if huo_palace:
        huo_palace["minor_stars"].append(Star(name="huoxingMin", type="tough", scope="origin"))

    ling_palace = _find_palace_by_branch_index(palaces, ling_index)
    if ling_palace:
        ling_palace["minor_stars"].append(Star(name="lingxingMin", type="tough", scope="origin"))

    # 5. 地空、地劫（按时辰）
    kong_index, jie_index = get_minor_star_positions_kongjie(time_index)

    kong_palace = _find_palace_by_branch_index(palaces, kong_index)
    if kong_palace:
        kong_palace["minor_stars"].append(Star(name="dikongMin", type="tough", scope="origin"))

    jie_palace = _find_palace_by_branch_index(palaces, jie_index)
    if jie_palace:
        jie_palace["minor_stars"].append(Star(name="dijieMin", type="tough", scope="origin"))

    # 6. 禄存、擎羊、陀罗、天马（按年干支）
    lucun_index, yang_index, tuo_index, tianma_index = (
        get_minor_star_positions_lucun_yangtuo_tianma(year_stem_index, year_branch_index)
    )

    lucun_palace = _find_palace_by_branch_index(palaces, lucun_index)
    if lucun_palace:
        lucun_palace["minor_stars"].append(Star(name="lucunMin", type="lucun", scope="origin"))

    yang_palace = _find_palace_by_branch_index(palaces, yang_index)
    if yang_palace:
        yang_palace["minor_stars"].append(Star(name="qingyangMin", type="tough", scope="origin"))

    tuo_palace = _find_palace_by_branch_index(palaces, tuo_index)
    if tuo_palace:
        tuo_palace["minor_stars"].append(Star(name="tuoluoMin", type="tough", scope="origin"))

    tianma_palace = _find_palace_by_branch_index(palaces, tianma_index)
    if tianma_palace:
        tianma_palace["minor_stars"].append(Star(name="tianmaMin", type="tianma", scope="origin"))


def get_minor_stars_in_palace(palace: dict) -> List[Star]:
    """
    获取指定宫位中的辅星列表

    Args:
        palace: 宫位字典

    Returns:
        辅星列表
    """
    return palace.get("minor_stars", [])


def has_minor_star(palace: dict, star_name: str) -> bool:
    """
    判断宫位是否包含指定辅星

    Args:
        palace: 宫位字典
        star_name: 星曜名称

    Returns:
        是否包含
    """
    minor_stars = get_minor_stars_in_palace(palace)
    return any(star.name == star_name for star in minor_stars)
