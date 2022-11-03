from dataclasses import dataclass

from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.event_stream import EventStream
from infrastructure.ddd.serializer import Serializer
from infrastructure.persistence.db import DataBase


@dataclass
class EventStore():
    __db: DataBase

    def obtain(self, fromSequence: int, quantity: int = None) -> EventStream:
        if fromSequence <= 0:
            raise Exception('Se esperaba un numero de secuencia mayor o igual a 1')
        if quantity is not None and quantity <= 0:
            return EventStream([])
        sql = "SELECT " \
              "e.message_id," \
              " e.datetime," \
              " e.sequence," \
              " e.aggregate," \
              " e.aggregate_id," \
              " e.order_number," \
              " e.event_type, " \
              f"e.payload, " \
              f"FROM events AS e WHERE e.sequence >= {fromSequence} ORDER BY e.sequence".format(fromSequence=str(fromSequence))
        if quantity is not None:
            sql + f" LIMIT {quantity}".format(quantity=str(quantity))

        regs = self.__db.obtainRelated(sql)
        return self.createEventStream(regs)

    def addEvent(self, domainEvent: DomainEvent):
        metadata = domainEvent.getMetadata()
        payload = domainEvent.getPayload()
        serializedPayload = Serializer.serialize(payload)
        values = [
            metadata.getAggregateId(),
            metadata.getDatetimeUTC(),
            metadata.getSequence(),
            metadata.getAggregate(),
            metadata.getAggregateId(),
            metadata.getOrderNumber(),
            domainEvent.getType(),
            serializedPayload
        ]
        valuesString = ', '.join(values)
        sql = "INSERT INTO events (" \
              "message_id," \
              " datetime," \
              " sequence," \
              " aggregate," \
              " aggregate_id," \
              " order_number," \
              " event_type," \
              " payload" \
              ")" \
            "VALUES ({valuesString})".format(valuesString=valuesString)
        self.__db.execute(sql)
