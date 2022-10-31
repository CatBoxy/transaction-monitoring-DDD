from dataclasses import dataclass
from typing import List

from infrastructure.rules.rule import Rule
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass(frozen=True)
class ScanScheduled():
    screeningId: UUIDValue
    startingDate: DateTime
    redFlags: List[Rule]
    periodStart: DateTime
    periodEnd: DateTime
    isFullScan: bool
