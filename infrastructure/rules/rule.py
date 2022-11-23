from dataclasses import dataclass


@dataclass
class Rule():
    __code: int

    def getRuleCode(self) -> int:
        return self.__code
