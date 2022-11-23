from domain.alerts.alert import Alert
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.persistence.aggregate_repository import AggregateRepository


class AlertRepository(AggregateRepository):
    def __init__(self, eventStore):
        super().__init__(eventStore, Alert.__module__, Alert.__name__)

    def getAlertId(self, alertId: AggregateId) -> Aggregate:
        try:
            return self._getAggregate(alertId)
        except Exception:
            raise Exception('Alerta no encontrada')

    def save(self, alert: Alert):
        self._saveAggregate(alert)
