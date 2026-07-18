"""
Minor stars placement for iztro-py

Functions for placing the 14 minor stars (辅星) into palaces.
"""

from typing import Any, Dict, List
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
        lunar_month: 修正后的农历月序号 (1-12)
        time_index: 时辰索引
        year_stem: 年干
        year_branch: 年支

    Note:
        直接修改palaces列表，不返回值
    """
    year_stem_index = HEAVENLY_STEMS.index(year_stem)
    year_branch_index = EARTHLY_BRANCHES.index(year_branch)

    zuofu_index = get_minor_star_position_zuofu(lunar_month)
    youbi_index = get_minor_star_position_youbi(lunar_month)
    wenchang_index = get_minor_star_position_wenchang(time_index)
    wenqu_index = get_minor_star_position_wenqu(time_index)
    kuai_index, yue_index = get_minor_star_positions_kuiyue(year_stem_index)
    huo_index, ling_index = get_minor_star_positions_huoling(year_branch_index, time_index)
    kong_index, jie_index = get_minor_star_positions_kongjie(time_index)
    lucun_index, yang_index, tuo_index, tianma_index = (
        get_minor_star_positions_lucun_yangtuo_tianma(year_stem_index, year_branch_index)
    )

    # 安星顺序与 iztro getMinorStar 的 push 顺序一致，保证同宫内星曜排列相同：
    # 左辅、右弼、文昌、文曲、天魁、天钺、禄存、天马、地空、地劫、火星、铃星、擎羊、陀罗
    placements = [
        (zuofu_index, "zuofuMin", "soft"),
        (youbi_index, "youbiMin", "soft"),
        (wenchang_index, "wenchangMin", "soft"),
        (wenqu_index, "wenquMin", "soft"),
        (kuai_index, "tiankuiMin", "soft"),
        (yue_index, "tianyueMin", "soft"),
        (lucun_index, "lucunMin", "lucun"),
        (tianma_index, "tianmaMin", "tianma"),
        (kong_index, "dikongMin", "tough"),
        (jie_index, "dijieMin", "tough"),
        (huo_index, "huoxingMin", "tough"),
        (ling_index, "lingxingMin", "tough"),
        (yang_index, "qingyangMin", "tough"),
        (tuo_index, "tuoluoMin", "tough"),
    ]
    for palace_index, star_name, star_type in placements:
        palaces[palace_index]["minor_stars"].append(
            Star(name=star_name, type=star_type, scope="origin")
        )


def get_minor_stars_in_palace(palace: dict) -> List[Star]:
    """
    获取指定宫位中的辅星列表

    Args:
        palace: 宫位字典

    Returns:
        辅星列表
    """
    result: List[Star] = palace.get("minor_stars", [])
    return result


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
