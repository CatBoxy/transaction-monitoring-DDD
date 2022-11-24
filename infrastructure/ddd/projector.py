from dataclasses import dataclass

from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.event_stream import EventStream
from infrastructure.ddd.projectorState import ProjectorState
from infrastructure.ddd.reproduction_state import ReproductionState
from infrastructure.persistence.db import DataBase
from infrastructure.persistence.tableMysql import TableMysql


@dataclass
class Projector():
    __db: DataBase
    __table: TableMysql
    __projectorId: str

    def start(self):
        count = self.__table
    def play(self):
        newProjectorState = self.getProjectorState().playing()
        self.saveProjectorState(newProjectorState)

    def getProjectorState(self) -> ProjectorState:
        projections = ['projector_id', 'starting_date', 'position', 'last_update', 'reproduction_state', 'last_error']
        conditions = [{'projector_id': self.__projectorId}]
        tableValues = self.__table.select(projections, conditions)
        if len(tableValues) != 1:
            raise Exception('Estado del proyector no disponible')
        reg = tableValues[0]
        return ProjectorState(
            self.__projectorId,
            reg['starting_date'],
            reg['position'],
            reg['last_update'],
            ReproductionState(reg['reproduction_state']),
            reg['last_error']
        )

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

    def saveProjectorState(self, projectorState: ProjectorState):
        fields = {
            'projector_id': self.__projectorId,
            'starting_date': projectorState.getStartingDate(),
            'position': projectorState.getPosition(),
            'last_update': projectorState.getLastUpdate(),
            'reproduction_state': projectorState.getReproductionState(),
            'last_error': projectorState.getLastError()
        }
        self.__table.replace(fields)

    def __apply(self, event: DomainEvent):
        payload = event.getPayload()
        applyName = "on" + payload.__class__.__name__
        if hasattr(self, applyName):
            eventApply = getattr(self, applyName)
            return eventApply()
