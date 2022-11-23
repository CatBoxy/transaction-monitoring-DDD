from dataclasses import dataclass

from domain.events.alert_dismissed import AlertDismissed
from domain.events.alert_fired import AlertFired
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.valueObjects.date_time import DateTime
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class Alert(Aggregate):
    @classmethod
    def create(
            cls,
            uuid: UUIDValue,
            accountId: UUIDValue,
            screeningId: UUIDValue,
            creationDateTime: DateTime,
            redFlag,
            dateFrom: DateTime,
            dateTo: DateTime,
            params,
            transactions
    ):
        alert = Alert(AggregateId(uuid.myUuid))
        alertFired = AlertFired(
            alertId=uuid.myUuid,
            accountId=accountId.myUuid,
            screeningId=screeningId.myUuid,
            creationDateTime=creationDateTime.dateTime,
            redFlag=redFlag,
            dateFrom=dateFrom.dateTime,
            dateTo=dateTo.dateTime,
            params=params,
            transactions=transactions
        )
        alert._publish(alertFired)
        return alert

    def dismiss(self, dateTime: str):
        if self.dismissed:
            raise ValueError("Alerta ya descartada")
        event = AlertDismissed(dismissalDate=dateTime, alertId=self.getAggregateId().getUUID())
        self._publish(event)

    def investigate(self, dateTime: str):
        pass

    #     Buscar los eventos con agregacion tipo Investigation
    #     Preguntar si

    def _applyAlertFired(self, event: AlertFired):
        self.dismissed = False

    def _applyAlertDismissed(self, event: AlertDismissed):
        self.dismissed = True
