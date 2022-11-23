from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.ddd.domain_event import DomainEvent
# from infrastructure.ddd.event_bus import EventBus
from infrastructure.ddd.event_stream import EventStream
from infrastructure.ddd.metadata_domain_event import MetadataDomainEvent
from infrastructure.ddd.serializer import Serializer
from infrastructure.persistence.db import DataBase


@dataclass
class EventStore():
    __db: DataBase
    # __eventBus: Optional[EventBus] = None

    def obtain(self, fromSequence: int, quantity: int = None) -> EventStream:
        if fromSequence <= 0:
            raise Exception('Se esperaba un numero de secuencia mayor o igual a 1')
        if quantity is not None and quantity <= 0:
            return EventStream([])
        values = [str(fromSequence)]
        sql = "SELECT " \
              "e.message_id," \
              " e.datetime," \
              " e.sequence," \
              " e.aggregate," \
              " e.aggregate_id," \
              " e.order_number," \
              " e.event_type, " \
              " e.event_module, " \
              "e.payload " \
              "FROM events AS e WHERE e.sequence >= %s ORDER BY e.sequence"
        if quantity is not None:
            sql = sql + " LIMIT %s"
            values.append(str(quantity))
        values = tuple(values)

        regs = self.__db.result(sql, values)
        return self.__createEventStream(regs)

    def obtainFromAggregate(self, aggregateId: AggregateId, fromOrder: int = 1, quantity: int = None) -> EventStream:
        if fromOrder <= 0:
            raise Exception('Se esperaba un orden mayor o igual a 1')
        if quantity is not None and quantity <= 0:
            return EventStream([])
        values = [str(aggregateId.getUUID()), str(fromOrder)]
        sql = "SELECT " \
              "e.message_id," \
              " e.datetime," \
              " e.sequence," \
              " e.aggregate," \
              " e.aggregate_id," \
              " e.order_number," \
              " e.event_type, " \
              " e.event_module, " \
              "e.payload " \
              "FROM events AS e WHERE e.aggregate_id = %s AND e.order_number >= %s ORDER BY e.order_number"
        if quantity is not None:
            sql = sql + " LIMIT %s"
            values.append(str(quantity))
        values = tuple(values)

        regs = self.__db.result(sql, values)
        return self.__createEventStream(regs)

    def __createEventStream(self, regs: List) -> EventStream:
        domainEvents = []
        for reg in regs:
            payload = Serializer.unserialize(reg['payload'], reg['event_type'], reg['event_module'])
            dateObj = datetime.strptime(str(reg['datetime']), '%Y-%m-%d %H:%M:%S')
            timeStamp = dateObj.timestamp()
            metadata = MetadataDomainEvent(
                str(reg['message_id']),
                timeStamp,
                int(reg['sequence']),
                str(reg['aggregate']),
                str(reg['aggregate_id']),
                int(reg['order_number'])
            )
            domainEvents.append(DomainEvent(payload, metadata))
        return EventStream(domainEvents)

    def save(self, aggregateId: AggregateId, eventStream: EventStream):
        def callback(aggregateId: AggregateId, eventStream: EventStream):
            nextEventSequence = self._getNextEventSequence()
            nextEventOrderNumber = self._getNextEventOrder(aggregateId.getUUID())
            for domainEvent in eventStream.getEvents():
                if domainEvent.getMetadata().getOrderNumber() != nextEventOrderNumber:
                    raise Exception('Evento fuera de orden')
                domainEvent = domainEvent.withSequence(nextEventSequence)
                self._addEvent(domainEvent)
                # self.__eventBus.publish(domainEvent)
                nextEventSequence += 1
                nextEventOrderNumber += 1

        self.__db.executeInTransaction(callback, aggregateId, eventStream)

    def _getNextEventSequence(self) -> int:
        sql = "SELECT IFNULL(MAX(sequence), 0) as sequence FROM events FOR UPDATE"
        row = self.__db.result(sql, None)
        return row[0]['sequence'] + 1

    def _getNextEventOrder(self, aggregateId: str) -> int:
        sql = "SELECT IFNULL(MAX(order_number), 0) as orderNumber FROM events WHERE aggregate_id = %s FOR UPDATE"
        row = self.__db.result(sql, (aggregateId,))
        return row[0]['orderNumber'] + 1

    def _addEvent(self, domainEvent: DomainEvent):
        metadata = domainEvent.getMetadata()
        payload = domainEvent.getPayload()
        serializedPayload = Serializer.serialize(payload)
        values = [
            metadata.getMessageId(),
            metadata.getDatetimeUTC(),
            str(metadata.getSequence()),
            metadata.getAggregate(),
            metadata.getAggregateId(),
            str(metadata.getOrderNumber()),
            domainEvent.getType(),
            domainEvent.getModule(),
            serializedPayload
        ]
        sql = "INSERT INTO events (" \
              "message_id," \
              " datetime," \
              " sequence," \
              " aggregate," \
              " aggregate_id," \
              " order_number," \
              " event_type," \
              " event_module," \
              " payload" \
              ")" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.__db.execute(sql, tuple(values))
