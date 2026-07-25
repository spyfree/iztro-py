"""
Star brightness (星耀亮度) data and calculations

Contains brightness information for stars based on their palace positions.
"""

from typing import Any, Dict, List, Optional

from iztro_py.data.constants import EARTHLY_BRANCHES
from iztro_py.data.types import Brightness, EarthlyBranchName, StarName

# ============================================================================
# Brightness Data (与 iztro lib/data/stars.js 的 STARS_INFO.brightness 逐行对齐)
# ============================================================================
# 亮度顺序：寅卯辰巳午未申酉戌亥子丑（以寅宫为索引 0，与宫位索引一致）
# Brightness levels: 庙(miao)、旺(wang)、得(de)、利(li)、平(ping)、不(bu)、陷(xian)
# None 表示该位置不标亮度（如擎羊在四马地、陀罗在四败地不标）

STAR_BRIGHTNESS: Dict[StarName, List[Optional[Brightness]]] = {
    # 紫微
    "ziweiMaj": ["旺", "旺", "得", "旺", "庙", "庙", "旺", "旺", "得", "旺", "平", "庙"],
    # 天机
    "tianjiMaj": ["得", "旺", "利", "平", "庙", "陷", "得", "旺", "利", "平", "庙", "陷"],
    # 太阳
    "taiyangMaj": ["旺", "庙", "旺", "旺", "旺", "得", "得", "陷", "不", "陷", "陷", "不"],
    # 武曲
    "wuquMaj": ["得", "利", "庙", "平", "旺", "庙", "得", "利", "庙", "平", "旺", "庙"],
    # 天同
    "tiantongMaj": ["利", "平", "平", "庙", "陷", "不", "旺", "平", "平", "庙", "旺", "不"],
    # 廉贞
    "lianzhenMaj": ["庙", "平", "利", "陷", "平", "利", "庙", "平", "利", "陷", "平", "利"],
    # 天府
    "tianfuMaj": ["庙", "得", "庙", "得", "旺", "庙", "得", "旺", "庙", "得", "庙", "庙"],
    # 太阴
    "taiyinMaj": ["旺", "陷", "陷", "陷", "不", "不", "利", "不", "旺", "庙", "庙", "庙"],
    # 贪狼
    "tanlangMaj": ["平", "利", "庙", "陷", "旺", "庙", "平", "利", "庙", "陷", "旺", "庙"],
    # 巨门
    "jumenMaj": ["庙", "庙", "陷", "旺", "旺", "不", "庙", "庙", "陷", "旺", "旺", "不"],
    # 天相
    "tianxiangMaj": ["庙", "陷", "得", "得", "庙", "得", "庙", "陷", "得", "得", "庙", "庙"],
    # 天梁
    "tianliangMaj": ["庙", "庙", "庙", "陷", "庙", "旺", "陷", "得", "庙", "陷", "庙", "旺"],
    # 七杀
    "qishaMaj": ["庙", "旺", "庙", "平", "旺", "庙", "庙", "庙", "庙", "平", "旺", "庙"],
    # 破军
    "pojunMaj": ["得", "陷", "旺", "平", "庙", "旺", "得", "陷", "旺", "平", "庙", "旺"],
    # 文昌
    "wenchangMin": ["陷", "利", "得", "庙", "陷", "利", "得", "庙", "陷", "利", "得", "庙"],
    # 文曲
    "wenquMin": ["平", "旺", "得", "庙", "陷", "旺", "得", "庙", "陷", "旺", "得", "庙"],
    # 火星
    "huoxingMin": ["庙", "利", "陷", "得", "庙", "利", "陷", "得", "庙", "利", "陷", "得"],
    # 铃星
    "lingxingMin": ["庙", "利", "陷", "得", "庙", "利", "陷", "得", "庙", "利", "陷", "得"],
    # 擎羊
    "qingyangMin": [None, "陷", "庙", None, "陷", "庙", None, "陷", "庙", None, "陷", "庙"],
    # 陀罗
    "tuoluoMin": ["陷", None, "庙", "陷", None, "庙", "陷", None, "庙", "陷", None, "庙"],
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

    # 地支索引（子=0）转换为亮度表索引（寅=0）
    brightness_index = (EARTHLY_BRANCHES.index(palace_branch) - 2) % 12

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

        # 主星与有亮度表的辅星（文昌、文曲、火星、铃星、擎羊、陀罗）都赋亮度
        for star in palace["major_stars"] + palace["minor_stars"]:
            brightness = get_star_brightness(star.name, palace_branch)
            if brightness:
                star.brightness = brightness


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
