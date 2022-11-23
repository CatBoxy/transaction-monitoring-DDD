from domain.transactions.transaction import Transaction
from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.persistence.aggregate_repository import AggregateRepository


class TransactionRepository(AggregateRepository):
    def __init__(self, eventStore):
        super().__init__(eventStore, Transaction.__module__, Transaction.__name__)

    def getTransactionId(self, transactionId: AggregateId) -> Aggregate:
        try:
            return self._getAggregate(transactionId)
        except Exception:
            raise Exception('Transaccion no encontrada')

    def save(self, transaction: Transaction):
        self._saveAggregate(transaction)
