from dataclasses import dataclass

from infrastructure.ddd.projector import Projector
from infrastructure.projections.current_transactions import CurrentTransactions


@dataclass
class CurrentTransactionsProjector(Projector):

    __currentTransactions: CurrentTransactions

    def onTransactionCreated(self):
        pass