"""
Adjective, flower, and helper star placement for iztro-py.

The placement order follows iztro@2.5.8 `getAdjectiveStar()` exactly for the
default algorithm, and all generated stars are attached to `adjective_stars`.
"""

from typing import Any, Dict, List

from iztro_py.data.types import GenderName, Star
from iztro_py.utils.calendar import get_heavenly_stem_and_earthly_branch_date, parse_solar_date
from iztro_py.star.location import (
    get_daily_star_indices,
    get_timely_star_indices,
    get_luan_xi_indices,
    get_monthly_star_indices,
    get_yearly_star_indices,
)


def _append(palaces: List[Dict[str, Any]], index: int, name: str, star_type: str) -> None:
    palaces[index]["adjective_stars"].append(Star(name=name, type=star_type, scope="origin"))


def place_adjective_stars(
    palaces: List[Dict[str, Any]],
    solar_date: str,
    time_index: int,
    gender: GenderName,
    fix_leap: bool,
    soul_index: int,
    body_index: int,
) -> None:
    """Place adjective/flower/helper stars using JS-aligned formulas."""
    stems_and_branches = get_heavenly_stem_and_earthly_branch_date(
        *parse_solar_date(solar_date),
        time_index,
    )
    yearly = get_yearly_star_indices(
        solar_date,
        time_index,
        gender,
        fix_leap,
        soul_index,
        body_index,
    )
    monthly = get_monthly_star_indices(solar_date, time_index, fix_leap)
    daily = get_daily_star_indices(solar_date, time_index, fix_leap)
    timely = get_timely_star_indices(time_index)
    luan_xi = get_luan_xi_indices(stems_and_branches.year_branch)

    # 红鸾、天喜、天姚、咸池、解神
    _append(palaces, luan_xi["hongluan_index"], "hongluan", "flower")
    _append(palaces, luan_xi["tianxi_index"], "tianxi", "flower")
    _append(palaces, monthly["tianyao_index"], "tianyao", "flower")
    _append(palaces, yearly["xianchi_index"], "xianchi", "flower")
    _append(palaces, monthly["yuejie_index"], "jieshen", "helper")

    # 日系杂曜
    _append(palaces, daily["santai_index"], "santai", "adjective")
    _append(palaces, daily["bazuo_index"], "bazuo", "adjective")
    _append(palaces, daily["enguang_index"], "enguang", "adjective")
    _append(palaces, daily["tiangui_index"], "tiangui", "adjective")

    # 年系杂曜
    _append(palaces, yearly["longchi_index"], "longchi", "adjective")
    _append(palaces, yearly["fengge_index"], "fengge", "adjective")
    _append(palaces, yearly["tiancai_index"], "tiancai", "adjective")
    _append(palaces, yearly["tianshou_index"], "tianshou", "adjective")

    # 时系杂曜
    _append(palaces, timely["taifu_index"], "taifu", "adjective")
    _append(palaces, timely["fenggao_index"], "fenggao", "adjective")

    # 月系杂曜
    _append(palaces, monthly["tianwu_index"], "tianwu", "adjective")

    # 继续按 JS push 顺序插入
    _append(palaces, yearly["huagai_index"], "huagai", "adjective")
    _append(palaces, yearly["tianguan_index"], "tianguan", "adjective")
    _append(palaces, yearly["tianfu_index"], "tianfuAdj", "adjective")
    _append(palaces, yearly["tianchu_index"], "tianchu", "adjective")
    _append(palaces, monthly["tianyue_index"], "tianyue", "adjective")
    _append(palaces, yearly["tiande_index"], "tiande", "adjective")
    _append(palaces, yearly["yuede_index"], "yuede", "adjective")
    _append(palaces, yearly["tiankong_index"], "tiankong", "adjective")
    _append(palaces, yearly["xunkong_index"], "xunkong", "adjective")
    _append(palaces, yearly["jielu_index"], "jielu", "adjective")
    _append(palaces, yearly["kongwang_index"], "kongwang", "adjective")
    _append(palaces, yearly["guchen_index"], "guchen", "adjective")
    _append(palaces, yearly["guasu_index"], "guasu", "adjective")
    _append(palaces, yearly["feilian_index"], "feilian", "adjective")
    _append(palaces, yearly["posui_index"], "posui", "adjective")
    _append(palaces, monthly["tianxing_index"], "tianxing", "adjective")
    _append(palaces, monthly["yinsha_index"], "yinsha", "adjective")
    _append(palaces, yearly["tianku_index"], "tianku", "adjective")
    _append(palaces, yearly["tianxu_index"], "tianxu", "adjective")
    _append(palaces, yearly["tianshi_index"], "tianshi", "adjective")
    _append(palaces, yearly["tianshang_index"], "tianshang", "adjective")

    # 生年年解
    _append(palaces, yearly["nianjie_index"], "nianjie", "helper")
