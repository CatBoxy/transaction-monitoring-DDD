from dataclasses import dataclass

from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass(frozen=True)
class EvidenceAttached():
    investigationId: UUIDValue
    attachedDate: DateTime
    evidenceId: UUIDValue