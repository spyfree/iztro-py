"""
Major stars placement for iztro-py

Functions for placing the 14 major stars (主星) into palaces.
"""

from typing import Any, Dict, List
from iztro_py.data.types import Star, FiveElementsClass
from iztro_py.star.location import get_major_star_positions


def place_major_stars(
    palaces: List[Dict[str, Any]],
    arg1,
    arg2,
) -> None:
    """
    将14颗主星安置到宫位中

    Args:
        palaces: 宫位列表
        arg1: 兼容两种调用方式：
              - (FiveElementsClass, lunar_day)
              - (ziwei_index: int, tianfu_index: int)
        arg2: 同上

    Note:
        直接修改palaces列表，不返回值
    """
    from iztro_py.data.constants import EARTHLY_BRANCHES

    # 兼容旧API：如果第一个参数是 FiveElementsClass，则按旧算法计算索引
    if isinstance(arg1, FiveElementsClass):
        from iztro_py.star.location import get_ziwei_index, get_tianfu_index

        five_class: FiveElementsClass = arg1
        lunar_day: int = arg2
        ziwei_index = get_ziwei_index(five_class, lunar_day)
        tianfu_index = get_tianfu_index(ziwei_index)
    else:
        ziwei_index = int(arg1)
        tianfu_index = int(arg2)

    # 获取所有主星位置（地支索引）
    star_positions = get_major_star_positions(ziwei_index, tianfu_index)

    # 将星曜放置到对应宫位
    # 注意：star_positions 中的索引是地支索引，需要转换为宫位索引
    for star_name, earthly_branch_index in star_positions.items():
        star = Star(
            name=star_name,
            type="major",
            scope="origin",
            brightness=None,  # 后续计算
            mutagen=None,  # 后续计算
        )

        # 查找具有该地支的宫位
        target_branch = EARTHLY_BRANCHES[earthly_branch_index]
        for palace in palaces:
            if palace["earthly_branch"] == target_branch:
                palace["major_stars"].append(star)
                break


def get_major_stars_in_palace(palace: dict) -> List[Star]:
    """
    获取指定宫位中的主星列表

    Args:
        palace: 宫位字典

    Returns:
        主星列表
    """
    return palace.get("major_stars", [])


def has_major_star(palace: dict, star_name: str) -> bool:
    """
    判断宫位是否包含指定主星

    Args:
        palace: 宫位字典
        star_name: 星曜名称

    Returns:
        是否包含
    """
    major_stars = get_major_stars_in_palace(palace)
    return any(star.name == star_name for star in major_stars)
