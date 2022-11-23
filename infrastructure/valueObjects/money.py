import re
from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Money(ValueObject):
    number: str
    currency: str
    __currencyValues: ClassVar[list] = ['ARS', 'USD']

    def __post_init__(self):
        if not re.search('[a-zA-Z]', self.number) is None:
            print(ValidationException("amount debe poseer solo numeros"))
            print(self.number)
            raise ValidationException("amount debe poseer solo numeros")
        if self.currency not in Money.__currencyValues:
            print(ValidationException("currency invalido"))
            print(self.currency)
            raise ValidationException("currency invalido")