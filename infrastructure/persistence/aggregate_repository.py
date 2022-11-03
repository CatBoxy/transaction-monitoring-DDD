from dataclasses import dataclass

from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.persistence.aggregate_not_found import AggregateNotFound
import importlib

from infrastructure.persistence.event_store import EventStore


@dataclass
class AggregateRepository():
    # checkear constructor de RepAgregacionesEventSourced.php
    __eventStore: EventStore
    __class: str

    def getAggregate(self, aggregateId: AggregateId) -> Aggregate:
        eventStream = self.__eventStore.getFromAggregate(aggregateId)
        if eventStream.isEmpty():
            raise AggregateNotFound(aggregateId.getUUID())
        try:
            # Checkear que exista la agregacion??
            AggregatePathLoader.isAggregate(self.__class)
            path = AggregatePathLoader.getImportString(self.__class)
            my_module = importlib.import_module(path)
            myClass = getattr(my_module, self.__class)
            aggregate = myClass(aggregateId, eventStream)
            return aggregate
        except ValueError:
            print()
            raise ValueError('Clase inexistente {0}'.format(self.__class))
            # my_module = importlib.import_module("module.submodule")
            # MyClass = getattr(my_module, self.__class)
            # instance = MyClass()


@dataclass
class AggregatePathLoader():
    __paths = {
        "alert": "domain.alerts.alert",
        "transaction": "domain.transactions.transaction",
        "scan": "domain.scannings.scan",
        "investigation": "domain.investigations.investigation"
    }

    @classmethod
    def getImportString(cls, className) -> str:
        if className in cls.__paths.keys():
            return cls.__paths.get(className)


    @classmethod
    def isAggregate(cls, className) -> bool:
        if className in cls.__paths.keys():
            return True
        else:
            raise ValueError