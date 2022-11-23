import uuid
from datetime import datetime

from domain.alerts.alert import Alert
from domain.events.alert_fired import RuleParam
from infrastructure.ddd.aggregate_Id import AggregateId
from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.event_stream import EventStream
from infrastructure.persistence.db import DataBase
from infrastructure.persistence.event_store import EventStore


# def test_event_store_addEvent():
#     """
#     GIVEN EventStore class initialized
#     WHEN addEvent method is called
#     THEN a new row in uif_db.events must be filled and payload must be a json object
#     """
#
#     ruleparam1 = RuleParam(name='rule1', value='1')
#     ruleparam2 = RuleParam(name='rule2', value='2')
#
#     database = DataBase('uif_db')
#     eventStore = EventStore(database)
#     myUuid = uuid.uuid4()
#
#     alertAggregate = Alert.create(
#         uuid=str(myUuid),
#         accountId=str(uuid.uuid4()),
#         screeningId=str(uuid.uuid4()),
#         creationDateTime=str(datetime.utcnow()),
#         redFlag='amountLimitRule',
#         dateFrom='21-05-2020 20:55:12',
#         dateTo='22-05-2020 16:55:12',
#         params=(ruleparam1, ruleparam2),
#         transactions=['id1', 'id2']
#     )
#     domainEvent = alertAggregate.getPendingEvents().getEvents()[0]
#
#     eventStore._addEvent(domainEvent)

def test_event_store_save():
    ruleparam1 = RuleParam(name='rule1', value='1')
    ruleparam2 = RuleParam(name='rule2', value='2')

    database = DataBase('uif_db')
    eventStore = EventStore(database)
    myUuid = uuid.uuid4()

    alertAggregate = Alert.create(
        uuid=str(myUuid),
        accountId=str(uuid.uuid4()),
        screeningId=str(uuid.uuid4()),
        creationDateTime=str(datetime.utcnow()),
        redFlag='amountLimitRule',
        dateFrom='21-05-2020 20:55:12',
        dateTo='22-05-2020 16:55:12',
        params=(ruleparam1, ruleparam2),
        transactions=['id1', 'id2']
    )
    alertAggregate.dismiss('25-05-2020 11:12:04')
    domainEvents = alertAggregate.getPendingEvents()

    eventStore.save(alertAggregate.getAggregateId(), domainEvents)


# def test_event_store_getNextEventOrder():
#     """
#     GIVEN aggregateId
#     WHEN getNextEventOrder method is called
#     THEN the last order_number must be returned, must be of type int
#     """
#     aggregateId = '530303ee-55a6-4f31-b410-db0f92ccd007'
#     database = DataBase('uif_db')
#     eventStore = EventStore(database)
#
#     row = eventStore._getNextEventOrder(aggregateId)
#     assert type(row) == int


# def test_event_store_getNextEventSequence():
#     """
#         GIVEN getNextEventSequence called
#         WHEN getNextEventSequence method is called
#         THEN the last sequence must be returned, must be of type int
#     """
#     database = DataBase('uif_db')
#     eventStore = EventStore(database)
#
#     row = eventStore._getNextEventSequence()
#     assert type(row) == int
#
#
# def test_event_store_obtain():
#     """
#         GIVEN an eventStore class instantiated, and a list of registers of events from DB
#         WHEN obtain method is called
#         THEN an EventStream of domain events must be instantiated and returned
#     """
#     database = DataBase('uif_db')
#     eventStore = EventStore(database)
#
#     eventStream = eventStore.obtain(1)
#     assert type(eventStream) == EventStream
#     assert eventStream.isEmpty() is False
#     assert type(eventStream.getEvents()[0]) == DomainEvent
#     emptyEventStream = eventStore.obtain(1, 0)
#     assert type(emptyEventStream) == EventStream
#     assert emptyEventStream.isEmpty() is True
#
#
# def test_event_store_obtainFromAggregate():
#     """
#         GIVEN an eventStore class instantiated, and a list of registers of events from DB
#         WHEN __createEventStream method is called
#         THEN an EventStream of domain events must be instantiated and returned
#     """
#     database = DataBase('uif_db')
#     eventStore = EventStore(database)
#
#     newAggregateId = AggregateId('530303ee-55a6-4f31-b410-db0f92ccd007')
#     eventStream = eventStore.obtainFromAggregate(newAggregateId, 1)
#
#     assert type(eventStream) == EventStream
#     assert eventStream.isEmpty() is False
#     assert type(eventStream.getEvents()[0]) == DomainEvent
#     emptyEventStream = eventStore.obtainFromAggregate(newAggregateId, 1, 0)
#     assert type(emptyEventStream) == EventStream
#     assert emptyEventStream.isEmpty() is True
