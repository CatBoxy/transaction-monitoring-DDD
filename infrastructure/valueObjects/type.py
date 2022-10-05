from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Type(ValueObject):
    transactionTypes: ClassVar[list] = ['incoming_payment']
    transactionType: str

    def __post_init__(self):
        if self.transactionType not in Type.transactionTypes:
            print(ValidationException("docType invalido"))
            print(self.transactionType)
            raise ValidationException("docType invalido")