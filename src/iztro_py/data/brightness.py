"""
Star brightness (星耀亮度) data and calculations

Contains brightness information for stars based on their palace positions.
"""

from typing import Any, Dict, List, Optional
from iztro_py.data.types import StarName, Brightness, EarthlyBranchName
from iztro_py.data.constants import EARTHLY_BRANCHES


# ============================================================================
# Brightness Data for Major Stars
# ============================================================================
# 亮度顺序：寅卯辰巳午未申酉戌亥子丑
# Brightness levels: 庙(miao)、旺(wang)、得(de)、利(li)、平(ping)、不(bu)、陷(xian)

STAR_BRIGHTNESS: Dict[StarName, List[Optional[Brightness]]] = {
    # 紫微星
    "ziweiMaj": ["旺", "旺", "得", "旺", "庙", "庙", "旺", "旺", "得", "旺", "平", "庙"],
    # 天机星
    "tianjiMaj": ["旺", "旺", "平", "陷", "平", "平", "平", "平", "平", "平", "庙", "庙"],
    # 太阳星
    "taiyangMaj": ["庙", "庙", "庙", "庙", "旺", "利", "平", "陷", "陷", "陷", "陷", "得"],
    # 武曲星
    "wuquMaj": ["平", "陷", "得", "利", "陷", "旺", "旺", "旺", "庙", "庙", "得", "得"],
    # 天同星
    "tiantongMaj": ["得", "陷", "陷", "得", "利", "旺", "得", "得", "利", "旺", "庙", "庙"],
    # 廉贞星
    "lianzhenMaj": ["陷", "陷", "陷", "庙", "旺", "利", "平", "平", "平", "平", "庙", "旺"],
    # 天府星
    "tianfuMaj": ["庙", "庙", "庙", "庙", "庙", "庙", "庙", "庙", "庙", "庙", "庙", "庙"],
    # 太阴星
    "taiyinMaj": ["得", "得", "平", "陷", "旺", "庙", "平", "得", "平", "陷", "庙", "庙"],
    # 贪狼星
    "tanlangMaj": ["旺", "旺", "陷", "陷", "利", "得", "庙", "旺", "庙", "旺", "陷", "得"],
    # 巨门星
    "jumenMaj": ["得", "得", "陷", "陷", "陷", "平", "庙", "旺", "平", "得", "旺", "得"],
    # 天相星
    "tianxiangMaj": ["旺", "旺", "平", "平", "庙", "庙", "旺", "旺", "平", "平", "庙", "庙"],
    # 天梁星
    "tianliangMaj": ["庙", "庙", "平", "平", "旺", "旺", "平", "平", "利", "利", "得", "得"],
    # 七杀星
    "qishaMaj": ["庙", "庙", "平", "平", "陷", "陷", "旺", "旺", "得", "得", "利", "利"],
    # 破军星
    "pojunMaj": ["得", "得", "陷", "旺", "庙", "平", "陷", "平", "旺", "庙", "陷", "得"],
    # 辅星的亮度通常不标注，这里可以留空或使用默认值
}


def get_star_brightness(
    star_name: StarName, palace_branch: EarthlyBranchName
) -> Optional[Brightness]:
    """
    根据星曜名称和宫位地支获取星曜亮度

    Args:
        star_name: 星曜名称
        palace_branch: 宫位地支

    Returns:
        亮度等级，如果没有定义则返回None
    """
    if star_name not in STAR_BRIGHTNESS:
        return None

    brightness_list = STAR_BRIGHTNESS[star_name]

    # 地支索引：子丑寅卯辰巳午未申酉戌亥 (0-11)
    # 亮度列表索引：寅卯辰巳午未申酉戌亥子丑 (0-11)
    # 需要转换索引
    branch_index = EARTHLY_BRANCHES.index(palace_branch)

    # 转换索引：子(0)->10, 丑(1)->11, 寅(2)->0, ...
    brightness_index_map = {
        0: 10,  # 子
        1: 11,  # 丑
        2: 0,  # 寅
        3: 1,  # 卯
        4: 2,  # 辰
        5: 3,  # 巳
        6: 4,  # 午
        7: 5,  # 未
        8: 6,  # 申
        9: 7,  # 酉
        10: 8,  # 戌
        11: 9,  # 亥
    }

    brightness_index = brightness_index_map[branch_index]

    return brightness_list[brightness_index]


def apply_brightness_to_palaces(palaces: List[Dict[str, Any]]) -> None:
    """
    为所有宫位中的星曜添加亮度属性

    Args:
        palaces: 宫位列表

    Note:
        直接修改palaces列表，不返回值
    """
    for palace in palaces:
        palace_branch = palace["earthly_branch"]

        # 为主星添加亮度
        for star in palace["major_stars"]:
            brightness = get_star_brightness(star.name, palace_branch)
            if brightness:
                star.brightness = brightness

        # 辅星通常不标注亮度，但可以预留接口
        # for star in palace['minor_stars']:
        #     brightness = get_star_brightness(star.name, palace_branch)
        #     if brightness:
        #         star.brightness = brightness


def get_brightness_score(brightness: Optional[Brightness]) -> int:
    """
    获取亮度的数值评分（用于比较）

    Args:
        brightness: 亮度等级

    Returns:
        数值评分 (0-6)，庙最高，陷最低
    """
    scores = {"庙": 6, "旺": 5, "得": 4, "利": 3, "平": 2, "不": 1, "陷": 0, None: 0}

    return scores.get(brightness, 0)


def is_bright(brightness: Optional[Brightness]) -> bool:
    """
    判断星曜是否处于庙旺状态

    Args:
        brightness: 亮度等级

    Returns:
        是否为庙或旺
    """
    return brightness in ["庙", "旺"]


def is_weak(brightness: Optional[Brightness]) -> bool:
    """
    判断星曜是否处于陷弱状态

    Args:
        brightness: 亮度等级

    Returns:
        是否为陷
    """
    return brightness == "陷"
