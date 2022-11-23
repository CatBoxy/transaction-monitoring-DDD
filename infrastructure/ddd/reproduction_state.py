from dataclasses import dataclass


@dataclass
class ReproductionState():
    STOPPED = 'stopped'
    INITIATED = 'initiating'
    PLAYING = 'playing'
    FAILING = 'failing'
    __state: str

    def __post_init__(self):
        if self.__state not in [self.STOPPED, self.INITIATED, self.PLAYING, self.FAILING]:
            raise Exception('estado de reproduccion invalido')

    def isStopped(self) -> bool:
        return self.__state == self.STOPPED

    def isInitiating(self) -> bool:
        return self.__state == self.INITIATED

    def isPlaying(self) -> bool:
        return self.__state == self.PLAYING

    def isFailing(self) -> bool:
        return self.__state == self.FAILING

    def toString(self) -> str:
        return self.__state

    @classmethod
    def stopped(cls) -> 'ReproductionState':
        return ReproductionState(cls.STOPPED)

    @classmethod
    def initiating(cls) -> 'ReproductionState':
        return ReproductionState(cls.INITIATED)

    @classmethod
    def playing(cls) -> 'ReproductionState':
        return ReproductionState(cls.PLAYING)

    @classmethod
    def failing(cls) -> 'ReproductionState':
        return ReproductionState(cls.FAILING)
