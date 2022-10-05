from datetime import datetime
from dataclasses import dataclass

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class DateTime(ValueObject):
    dateTime: str

    def __post_init__(self):
        try:
            datetime.strptime(self.dateTime, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print(ValidationException('dateTime invalido'))
            raise ValidationException('dateTime invalido')