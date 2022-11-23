from dataclasses import dataclass

from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.event_stream import EventStream
from infrastructure.ddd.projectorState import ProjectorState
from infrastructure.persistence.db import DataBase
from infrastructure.persistence.tableMysql import TableMysql


@dataclass
class Projector():
    __db: DataBase
    __table: TableMysql

    def play(self):
        newProjectorState = self.getProjectorState().playing()
        self.saveProjectorState(newProjectorState)

    def getProjectorState(self) -> ProjectorState:
        projections = ['projector_id', 'starting_date', 'position', 'last_update', 'reproduction_state', 'last_error']
        tableValues = self.__db.select(projections, )


    def projectStream(self, eventStream: EventStream):
        def callback():
            projectorState = self.getProjectorState
            for domainEvent in eventStream.getEvents():
                if projectorState.isEventReproduced(domainEvent):
                    continue
                callableFunc = self.__apply(domainEvent)
                projectorState = projectorState.projectingEvent(domainEvent, callableFunc)
                if not projectorState.getReproductionState().isPlaying():
                    break
            self.saveProjectorState(projectorState)
        self.__db.executeInTransaction(callback, None, eventStream)

    def __apply(self, event: DomainEvent):
        payload = event.getPayload()
        applyName = "on" + payload.__class__.__name__
        if hasattr(self, applyName):
            eventApply = getattr(self, applyName)
            return eventApply()
