from dataclasses import dataclass

from domain.events.scan_canceled import ScanCanceled
from domain.events.scan_ended import ScanEnded
from domain.events.scan_executed import ScanExecuted
from domain.events.scan_scheduled import ScanScheduled
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class Scan(Aggregate):
    def getScanId(self) -> str:
        return self.getAggregateId().getUUID()

    @classmethod
    def schedule(
            cls,
            uuid: UUIDValue,
            startingDate: DateTime,
            rules,
            periodStart: DateTime,
            periodEnd: DateTime,
            isFullScan: bool
    ):
        scan = Scan(AggregateId(uuid.myUuid))
        scanScheduled = ScanScheduled(
            screeningId=uuid.myUuid,
            startingDate=startingDate.dateTime,
            redFlags=rules,
            periodStart=periodStart.dateTime,
            periodEnd=periodEnd.dateTime,
            isFullScan=isFullScan
        )
        scan._publish(scanScheduled)
        return scan

    def execute(self, dateTime, rules):
        if self.executed:
            raise ValueError("Scan ya ejecutado")
        event = ScanExecuted(screeningId=self.getScanId(), executionDate=dateTime, redFlags=rules)
        self._publish(event)

    def cancel(self, dateTime, rules):
        event = ScanCanceled(screeningId=self.getScanId(), cancelationDate=dateTime, redFlags=rules)
        self._publish(event)

    def end(self, dateTime, rules):
        event = ScanEnded(screeningId=self.getScanId(), finishedDate=dateTime, redFlags=rules)
        self._publish(event)

    def _applyScanScheduled(self, event: ScanScheduled):
        self.executed = False
        self.canceled = False
        self.ended = False

    def _applyScanExecuted(self, event: ScanExecuted):
        self.executed = True

    def _applyScanCanceled(self, event: ScanCanceled):
        self.canceled = True

    def _applyScanEnded(self, event: ScanEnded):
        self.ended = True
