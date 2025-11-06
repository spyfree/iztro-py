"""
Major stars placement for iztro-py

Functions for placing the 14 major stars (主星) into palaces.
"""

from typing import List
from iztro_py.data.types import Star, FiveElementsClass
from iztro_py.star.location import get_star_indices, get_major_star_positions


def place_major_stars(
    palaces: List[dict],
    five_elements_class: FiveElementsClass,
    lunar_day: int
) -> None:
    """
    将14颗主星安置到宫位中

    Args:
        palaces: 宫位列表
        five_elements_class: 五行局
        lunar_day: 农历日

    Note:
        直接修改palaces列表，不返回值
    """
    # 获取紫微和天府的位置
    ziwei_index, tianfu_index = get_star_indices(five_elements_class, lunar_day)

    # 获取所有主星位置
    star_positions = get_major_star_positions(ziwei_index, tianfu_index)

    # 将星曜放置到对应宫位
    for star_name, palace_index in star_positions.items():
        star = Star(
            name=star_name,
            type='major',
            scope='origin',
            brightness=None,  # 后续计算
            mutagen=None  # 后续计算
        )

        palaces[palace_index]['major_stars'].append(star)


def get_major_stars_in_palace(palace: dict) -> List[Star]:
    """
    获取指定宫位中的主星列表

    Args:
        palace: 宫位字典

    Returns:
        主星列表
    """
    return palace.get('major_stars', [])


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
