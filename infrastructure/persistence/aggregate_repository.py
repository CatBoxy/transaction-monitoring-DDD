

from infrastructure.ddd.aggregate import Aggregate
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.persistence.aggregate_not_found import AggregateNotFound
import importlib

from infrastructure.persistence.event_store import EventStore


class AggregateRepository():
    def __init__(self, eventStore: EventStore, module: str, className: str):
        self.__eventStore = eventStore
        self.__module = module
        self.__class = className

    def _getAggregate(self, aggregateId: AggregateId) -> Aggregate:
        eventStream = self.__eventStore.obtainFromAggregate(aggregateId)
        if eventStream.isEmpty():
            raise AggregateNotFound(aggregateId.getUUID())
        try:
            my_module = importlib.import_module(self.__module)
            myClass = getattr(my_module, self.__class)
            aggregate = myClass(aggregateId, eventStream)
            return aggregate
        except ValueError:
            print()
            raise ValueError('Clase inexistente {0}'.format(self.__class))

    def _saveAggregate(self, aggregate: Aggregate):
        aggregateClass = aggregate.__class__.__name__
        if aggregateClass != self.__class:
            raise Exception(
                'Clase de agregacion {aggregateClass}, se esperaba una agregacion de clase {__class}'.format(
                    aggregateClass=aggregateClass, __class=self.__class))
        self.__eventStore.save(aggregate.getAggregateId(), aggregate.getPendingEvents())
