from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Currency(ValueObject):
    currencyValues: ClassVar[list] = ['ARS', 'USD']
    currency: str

    def __post_init__(self):
        if self.currency not in Currency.currencyValues:
            print(ValidationException("currency invalido"))
            print(self.currency)
            raise ValidationException("currency invalido")