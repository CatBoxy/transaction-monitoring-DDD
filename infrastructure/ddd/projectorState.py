from collections.abc import Callable
from copy import copy
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from infrastructure.ddd.domain_event import DomainEvent
from infrastructure.ddd.metadata_domain_event import MetadataDomainEvent
from infrastructure.ddd.reproduction_state import ReproductionState
from infrastructure.ddd.serializable import Serializable


@dataclass
class ProjectorState():
    __projectorId: str
    __startingDate: str
    __position: int
    __lastUpdate: str
    __reproductionState: ReproductionState
    __lastError: Optional[str] = None

    def getProjectorId(self) -> str:
        return self.__projectorId

    def getStartingDate(self) -> str:
        return self.__startingDate

    def getPosition(self) -> int:
        return self.__position

    def getNextPosition(self) -> int:
        return self.__position + 1

    def getLastUpdate(self) -> str:
        return self.__lastUpdate

    def getReproductionState(self) -> ReproductionState:
        return self.__reproductionState

    def getLastError(self) -> Optional[str]:
        return self.__lastError

    def isEventReproduced(self, domainEvent: DomainEvent) -> bool:
        return domainEvent.getMetadata().getSequence() <= self.__position

    def playing(self) -> 'ProjectorState':
        if self.__reproductionState.isPlaying():
            return self
        state = copy(self)
        state.__reproductionState = ReproductionState.playing()
        state.__lastError = None
        return state

    def stopped(self) -> 'ProjectorState':
        if self.__reproductionState.isStopped():
            return self
        state = copy(self)
        state.__reproductionState = ReproductionState.stopped()
        return state

    def projectingEvent(self, domainEvent: DomainEvent, callableFunc: Callable[Serializable, MetadataDomainEvent]):
        self.verifyProjectorPlaying()
        self.verifyIsNextEventToPlay(domainEvent)
        state = copy(self)
        state.__lastUpdate = str(datetime.utcnow())
        try:
            callableFunc(
                domainEvent.getPayload(),
                domainEvent.getMetadata()
            )
            state.__position + 1
            state.__reproductionState = ReproductionState.playing()
        except Exception as exc:
            state.__lastError = str(exc)
            state.__reproductionState = ReproductionState.failing()
        return state

    def verifyProjectorPlaying(self):
        if not self.getReproductionState().isPlaying():
            raise Exception('El proyector {projectorId} no se encuentra reproduciendo eventos. ({lastError})'.format(
                projectorId=self.__projectorId,
                lastError=self.__lastError
            ))

    def verifyIsNextEventToPlay(self, domainEvent: DomainEvent):
        nextSequence = self.__position + 1
        sequence = domainEvent.getMetadata().getSequence()
        if sequence != nextSequence:
            raise Exception('El proyector {projectorId} esperaba el evento {nextSequence} y no el {sequence}'.format(
                projectorId=self.__projectorId,
                nextSequence=nextSequence,
                sequence=sequence
            ))


