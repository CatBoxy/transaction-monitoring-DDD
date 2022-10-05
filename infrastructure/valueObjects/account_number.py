from dataclasses import dataclass
from typing import ClassVar, Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class AccountNumber(ValueObject):
    lenLimit: ClassVar[int] = 30
    number: Optional[str]

    def __post_init__(self):
        if self.number is not None:
            if not len(self.number) < AccountNumber.lenLimit:
                print(ValidationException("accountNumber debe ser menor a 30 caracteres"))
                print(self.number)
                raise ValidationException("accountNumber debe ser menor a 30 caracteres")