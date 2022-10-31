from dataclasses import dataclass

from domain.events.alert_dismissed import AlertDismissed
from domain.events.alert_fired import AlertFired
from infrastructure.ddd.aggregate import Aggregate


@dataclass
class Alert(Aggregate):
    @classmethod
    def create(
            cls,
            uuid,
            accountId,
            screeningId,
            creationDateTime,
            redFlag,
            dateFrom,
            dateTo,
            # metaData,
            transactions
    ):
        alert = Alert(uuid)
        alertFired = AlertFired(
            alertId=uuid,
            accountId=accountId,
            screeningId=screeningId,
            creationDateTime=creationDateTime,
            redFlag=redFlag,
            dateFrom=dateFrom,
            dateTo=dateTo,
            # metaData=metaData,
            transactions=transactions
        )
        alert._publish(alertFired)
        return alert

    def dismiss(self, dateTime):
        if self.dismissed:
            raise ValueError("Alerta ya descartada")
        event = AlertDismissed(dismissalDate=dateTime)
        self._publish(event)

    def _applyAlertFired(self, event: AlertFired):
        self.dismissed = False

    def _applyAlertDismissed(self, event: AlertDismissed):
        self.dismissed = True