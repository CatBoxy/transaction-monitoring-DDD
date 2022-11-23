from dataclasses import dataclass, field
from typing import List

from infrastructure.ddd.domain_event import DomainEvent


@dataclass
class EventBus():
    __subscribers: List = field(default_factory=lambda: [])

    def subscribe(self, eventListener: EventListener):
        self.__subscribers.append(eventListener)

    def publish(self, domainEvent: DomainEvent):
        for subscriber in self.__subscribers:
            subscriber.handle(domainEvent)