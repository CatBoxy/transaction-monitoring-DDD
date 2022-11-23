from dataclasses import dataclass

from infrastructure.ddd.projector import Projector


@dataclass
class CurrentTransactionsProjector(Projector):

    def onTransactionCreated(self):
        pass