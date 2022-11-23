from abc import ABC
from dataclasses import dataclass


@dataclass
class Projection(ABC):
    def create(self):
        raise NotImplementedError('Not implemented')

    def empty(self):
        raise NotImplementedError('Not implemented')
