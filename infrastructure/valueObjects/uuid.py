import uuid
from dataclasses import dataclass
from typing import ClassVar

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class UUIDValue(ValueObject):
    __uuidVersion: ClassVar[int] = 4
    myUuid: str

    def __post_init__(self):
        if not uuid.UUID(self.myUuid).version == UUIDValue.__uuidVersion:
            print(ValidationException("uuid debe ser un uuid valido"))
            print(self.myUuid)
            raise ValidationException("uuid debe ser un uuid valido")

    def __str__(self):
        return self.myUuid

    def __repr__(self):
        return self.myUuid
