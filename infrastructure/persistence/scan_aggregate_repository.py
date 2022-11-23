from domain.scannings.scan import Scan
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.persistence.aggregate_repository import AggregateRepository


class ScanRepository(AggregateRepository):
    def __init__(self, eventStore):
        super().__init__(eventStore, Scan.__module__, Scan.__name__)

    def getScanId(self, scanId: AggregateId) -> Aggregate:
        try:
            return self._getAggregate(scanId)
        except Exception:
            raise Exception('Scan no encontrado')

    def save(self, scan: Scan):
        self._saveAggregate(scan)