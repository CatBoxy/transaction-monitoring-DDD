from dataclasses import dataclass


@dataclass
class Rule():
    _code: int

    def getRuleCode(self) -> int:
        return self._code
