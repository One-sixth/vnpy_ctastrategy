"""
Defines constants and objects used in CtaStrategy App.
"""

import random
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Literal

from vnpy.trader.constant import Direction, Offset, Interval
from .locale import _

APP_NAME = "CtaStrategy"
STOPORDER_PREFIX = "STOP"


class StopOrderStatus(Enum):
    WAITING = _("等待中")
    CANCELLED = _("已撤销")
    TRIGGERED = _("已触发")


class EngineType(Enum):
    LIVE = _("实盘")
    BACKTESTING = _("回测")


class BacktestingMode(Enum):
    BAR = 1
    TICK = 2


@dataclass
class StopOrder:
    vt_symbol: str
    direction: Direction
    offset: Offset
    price: float
    volume: float
    stop_orderid: str
    strategy_name: str
    datetime: datetime
    lock: bool = False
    net: bool = False
    vt_orderids: list = field(default_factory=list)
    status: StopOrderStatus = StopOrderStatus.WAITING

    def is_active(self) -> bool:
        """
        Check if the order is active.
        """
        return self.status in [StopOrderStatus.WAITING]


EVENT_CTA_LOG = "eCtaLog"
EVENT_CTA_STRATEGY = "eCtaStrategy"
EVENT_CTA_STOPORDER = "eCtaStopOrder"

INTERVAL_DELTA_MAP: Dict[Interval, timedelta] = {
    Interval.TICK: timedelta(milliseconds=1),
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta(days=1),
}


# 用于指标部分

INDICATOR_TYPE = Literal['line', 'mark']
INDICATOR_LINE_STYLE = Literal['solid', 'dotted', 'dashed', 'large_dashed', 'sparse_dotted']
INDICATOR_MARKER_POSITION = Literal['above', 'below', 'inside']
INDICATOR_MARKER_SHAPE = Literal['arrow_up', 'arrow_down', 'circle', 'square']


@dataclass
class IndicatorMarkItem:
    text: str
    color: Optional[str] = None
    position: Optional[INDICATOR_MARKER_POSITION] = None
    shape: Optional[INDICATOR_MARKER_SHAPE] = None


@dataclass()
class IndicatorConfig:
    type: INDICATOR_TYPE
    name: str
    display_name: Optional[str] = None
    chart: str = ''
    color: Optional[str] = None
    visable: bool = True

    # 仅用于 LINE
    line_style: INDICATOR_LINE_STYLE = 'solid'
    line_thick: int = 1

    # 用于 MARK
    mark_position: INDICATOR_MARKER_POSITION = 'below'
    mark_shape: INDICATOR_MARKER_SHAPE = 'arrow_up'

    def __post_init__(self) -> None:
        """"""
        if self.display_name is None:
            self.display_name = self.name
        if self.color is None:
            self.color = _get_random_color()


@dataclass
class IndicatorStore:
    config: Dict[str, List[IndicatorConfig]] = field(default_factory=dict)
    data: Dict[str, list[float|IndicatorMarkItem]] = field(default_factory=dict)


def _get_random_color():
    red = random.randint(30, 255)
    green = random.randint(30, 255)
    blue = random.randint(30, 255)
    color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color
