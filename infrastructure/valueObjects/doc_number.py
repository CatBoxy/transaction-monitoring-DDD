import re
from dataclasses import dataclass
from typing import ClassVar, Union, Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class DocNumber(ValueObject):
    lenLimit: ClassVar[int] = 20
    number: Optional[str]

    def __post_init__(self):
        if self.number is not None:
            if not len(self.number) < DocNumber.lenLimit or not re.search('[a-zA-Z]', self.number) is None:
                print(ValidationException("docNumber debe ser menor a 20 caracteres y solo numeros"))
                print(self.number)
                raise ValidationException("docNumber debe ser menor a 20 caracteres y solo numeros")