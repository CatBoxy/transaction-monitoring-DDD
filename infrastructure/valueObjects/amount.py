import re
from dataclasses import dataclass

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Amount(ValueObject):
    number: str

    def __post_init__(self):
        if not re.search('[a-zA-Z]', self.number) is None:
            print(ValidationException("amount debe poseer solo numeros"))
            print(self.number)
            raise ValidationException("amount debe poseer solo numeros")