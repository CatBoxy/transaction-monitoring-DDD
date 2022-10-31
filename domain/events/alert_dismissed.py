from dataclasses import dataclass

from infrastructure.valueObjects.date_time import DateTime


@dataclass(frozen=True)
class AlertDismissed():
    dismissalDate: DateTime
