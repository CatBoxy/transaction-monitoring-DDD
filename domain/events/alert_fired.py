from dataclasses import dataclass
from typing import List

from infrastructure.rules.rule import Rule
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass(frozen=True)
class AlertFired():
    alertId: UUIDValue
    accountId: UUIDValue
    screeningId: UUIDValue
    creationDateTime: DateTime
    redFlag: Rule
    dateFrom: DateTime
    dateTo: DateTime
    # metaData: AlertMetadata
    transactions: List[UUIDValue]
