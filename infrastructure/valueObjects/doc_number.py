import re
from dataclasses import dataclass
from typing import ClassVar, Union, Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class DocNumber(ValueObject):
    number: Optional[str]
    docType: Optional[str]
    __lenLimit: ClassVar[int] = 20
    __docTypes: ClassVar[list] = ['DNI', 'Otro', 'CUIT', 'CUIL', 'Pasaporte', None]

    def __post_init__(self):
        if self.number is not None:
            if not len(self.number) < DocNumber.__lenLimit or not re.search('[a-zA-Z]', self.number) is None:
                print(ValidationException("docNumber debe ser menor a 20 caracteres y solo numeros"))
                print(self.number)
                raise ValidationException("docNumber debe ser menor a 20 caracteres y solo numeros")
        if self.docType is not None:
            if self.docType not in DocNumber.__docTypes:
                print(ValidationException("docType invalido"))
                print(self.docType)
                raise ValidationException("docType invalido")
