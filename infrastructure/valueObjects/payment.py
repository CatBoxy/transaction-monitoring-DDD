from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Payment(ValueObject):
    transactionType: str
    transactionMethod: str
    __transactionTypes: ClassVar[list] = ['incoming_payment']
    __transactionMethods: ClassVar[list] = ['debit_card', 'credit_card']


    def __post_init__(self):
        if self.transactionType not in Payment.__transactionTypes:
            print(ValidationException("docType invalido"))
            print(self.transactionType)
            raise ValidationException("docType invalido")
        if self.transactionMethod not in Payment.__transactionMethods:
            print(ValidationException("docType invalido"))
            print(self.transactionMethod)
            raise ValidationException("docType invalido")