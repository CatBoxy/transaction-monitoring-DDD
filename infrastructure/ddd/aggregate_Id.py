from dataclasses import dataclass

from infrastructure.ddd.validation_exception import ValidationException
from infrastructure.valueObjects.uuid import UUIDValue


@dataclass
class AggregateId():
    __tag: str
    __uuid: UUIDValue

    def __post_init__(self):
        if len(self.__tag) == 0:
            print(ValidationException("Etiqueta de identificador vacia"))
            print(self.__tag)
            raise ValidationException("Etiqueta de identificador debe ser valida")

    def getTag(self) -> str:
        return self.__tag

    def getUUID(self) -> UUIDValue:
        return self.__uuid
