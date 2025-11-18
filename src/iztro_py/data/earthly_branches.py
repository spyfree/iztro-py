"""
Earthly Branches (地支) data and properties

Contains detailed information about the twelve earthly branches including
yin-yang, five elements, clashes, soul/body stars, and health associations.
"""

from typing import Dict
from iztro_py.data.types import EarthlyBranchName, YinYang, FiveElements, StarName


class EarthlyBranch:
    """地支数据类"""

    def __init__(
        self,
        yin_yang: YinYang,
        five_elements: FiveElements,
        crash: EarthlyBranchName,
        soul: StarName,  # 命主
        body: StarName,  # 身主
        inside: str,  # 内脏
        outside: str,  # 外部
        health_tip: str,  # 健康提示
    ):
        self.yin_yang = yin_yang
        self.five_elements = five_elements
        self.crash = crash  # 相冲的地支
        self.soul = soul  # 命主星
        self.body = body  # 身主星
        self.inside = inside
        self.outside = outside
        self.health_tip = health_tip


# ============================================================================
# Earthly Branches Configuration
# ============================================================================

EARTHLY_BRANCHES_CONFIG: Dict[EarthlyBranchName, EarthlyBranch] = {
    # 子地支
    "ziEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="水",
        crash="wuEarthly",
        soul="tanlangMaj",  # 贪狼
        body="huoxingMin",  # 火星
        inside="胆",
        outside="下体",
        health_tip="生殖系统、膀胱、尿道之疾病",
    ),
    # 丑地支
    "chouEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="土",
        crash="weiEarthly",
        soul="jumenMaj",  # 巨门
        body="tianxiangMaj",  # 天相
        inside="肚",
        outside="手足",
        health_tip="脾胃、肠道之疾病",
    ),
    # 寅地支
    "yinEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="木",
        crash="shenEarthly",
        soul="lucunMin",  # 禄存
        body="tianliangMaj",  # 天梁
        inside="肝",
        outside="四肢",
        health_tip="肝胆、四肢筋骨之疾病",
    ),
    # 卯地支
    "maoEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="木",
        crash="youEarthly",
        soul="wenquMin",  # 文曲（与 iztro 保持一致）
        body="tiantongMaj",  # 天同
        inside="肝",
        outside="胸背",
        health_tip="肝胆、神经系统之疾病",
    ),
    # 辰地支
    "chenEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="土",
        crash="xuEarthly",
        soul="lianzhenMaj",  # 廉贞
        body="wenchangMin",  # 文昌
        inside="胸",
        outside="头面",
        health_tip="脾胃、胸部、皮肤之疾病",
    ),
    # 巳地支
    "siEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="火",
        crash="haiEarthly",
        soul="wuquMaj",  # 武曲
        body="tianjiMaj",  # 天机
        inside="心",
        outside="面部",
        health_tip="心脏、血液循环之疾病",
    ),
    # 午地支
    "wuEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="火",
        crash="ziEarthly",
        soul="pojunMaj",  # 破军
        body="huoxingMin",  # 火星
        inside="心",
        outside="眼目",
        health_tip="心脏、眼睛、血压之疾病",
    ),
    # 未地支
    "weiEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="土",
        crash="chouEarthly",
        soul="wuquMaj",  # 武曲
        body="tianxiangMaj",  # 天相
        inside="脾胃",
        outside="颈项",
        health_tip="脾胃、颈部之疾病",
    ),
    # 申地支
    "shenEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="金",
        crash="yinEarthly",
        soul="lianzhenMaj",  # 廉贞
        body="tianliangMaj",  # 天梁
        inside="肺",
        outside="脊柱",
        health_tip="呼吸系统、脊柱之疾病",
    ),
    # 酉地支
    "youEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="金",
        crash="maoEarthly",
        soul="wenquMin",  # 文曲
        body="tiantongMaj",  # 天同
        inside="肺",
        outside="咽喉",
        health_tip="呼吸系统、咽喉之疾病",
    ),
    # 戌地支
    "xuEarthly": EarthlyBranch(
        yin_yang="阳",
        five_elements="土",
        crash="chenEarthly",
        soul="lucunMin",  # 禄存
        body="wenchangMin",  # 文昌
        inside="命门",
        outside="腿足",
        health_tip="胃部、腿足、关节之疾病",
    ),
    # 亥地支
    "haiEarthly": EarthlyBranch(
        yin_yang="阴",
        five_elements="水",
        crash="siEarthly",
        soul="jumenMaj",  # 巨门
        body="tianjiMaj",  # 天机
        inside="肾",
        outside="头面",
        health_tip="肾脏、泌尿系统之疾病",
    ),
}


# ============================================================================
# Helper Functions
# ============================================================================


def get_soul_star(earthly_branch: EarthlyBranchName) -> StarName:
    """
    获取地支对应的命主星

    Args:
        earthly_branch: 地支名称

    Returns:
        命主星名称
    """
    return EARTHLY_BRANCHES_CONFIG[earthly_branch].soul


def get_body_star(earthly_branch: EarthlyBranchName) -> StarName:
    """
    获取地支对应的身主星

    Args:
        earthly_branch: 地支名称

    Returns:
        身主星名称
    """
    return EARTHLY_BRANCHES_CONFIG[earthly_branch].body


def get_yin_yang(earthly_branch: EarthlyBranchName) -> YinYang:
    """
    获取地支的阴阳属性

    Args:
        earthly_branch: 地支名称

    Returns:
        阴阳属性
    """
    return EARTHLY_BRANCHES_CONFIG[earthly_branch].yin_yang


def get_five_elements(earthly_branch: EarthlyBranchName) -> FiveElements:
    """
    获取地支的五行属性

    Args:
        earthly_branch: 地支名称

    Returns:
        五行属性
    """
    return EARTHLY_BRANCHES_CONFIG[earthly_branch].five_elements


def get_crash(earthly_branch: EarthlyBranchName) -> EarthlyBranchName:
    """
    获取相冲的地支

    Args:
        earthly_branch: 地支名称

    Returns:
        相冲的地支名称
    """
    return EARTHLY_BRANCHES_CONFIG[earthly_branch].crash


def get_health_info(earthly_branch: EarthlyBranchName) -> Dict[str, str]:
    """
    获取地支相关的健康信息

    Args:
        earthly_branch: 地支名称

    Returns:
        包含 inside, outside, health_tip 的字典
    """
    config = EARTHLY_BRANCHES_CONFIG[earthly_branch]
    return {"inside": config.inside, "outside": config.outside, "health_tip": config.health_tip}
