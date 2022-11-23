from dataclasses import dataclass
from typing import List

from infrastructure.rules.rule import Rule


@dataclass
class ScheduleScanCommand():
    startingDate: str
    redFlags: List[Rule]
    periodStart: str
    periodEnd: str
    isFullScan: bool
