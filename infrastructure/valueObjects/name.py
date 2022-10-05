from dataclasses import dataclass
from typing import ClassVar, Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Name(ValueObject):
    lenLimit: ClassVar[int] = 60
    name: Optional[str]

    def __post_init__(self):
        if self.name is not None:
            if not len(self.name) < Name.lenLimit:
                print(ValidationException("name debe ser menor a 60 caracteres"))
                print("name: " + self.name)
                raise ValidationException("name debe ser menor a 60 caracteres")