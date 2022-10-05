from dataclasses import dataclass
from typing import ClassVar, Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class Doctype(ValueObject):
    docTypes: ClassVar[list] = ['DNI', 'Otro', 'CUIT', 'CUIL', 'Pasaporte', None]
    docType: Optional[str]

    def __post_init__(self):
        if self.docType is not None:
            if self.docType not in Doctype.docTypes:
                print(ValidationException("docType invalido"))
                print(self.docType)
                raise ValidationException("docType invalido")