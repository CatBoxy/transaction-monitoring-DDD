from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Method(ValueObject):
    transactionMethods: ClassVar[list] = ['debit_card', 'credit_card']
    transactionMethod: str

    def __post_init__(self):
        if self.transactionMethod not in Method.transactionMethods:
            print(ValidationException("docType invalido"))
            print(self.transactionMethod)
            raise ValidationException("docType invalido")