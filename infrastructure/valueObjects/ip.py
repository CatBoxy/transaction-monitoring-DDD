import socket
from dataclasses import dataclass
from typing import Optional

from infrastructure.ddd.value_object import ValueObject
from infrastructure.ddd.validation_exception import ValidationException


@dataclass(frozen=True)
class IpAddress(ValueObject):
    address: Optional[str]

    def __post_init__(self):
        try:
            if self.address is not None:
                socket.inet_aton(self.address)
        except socket.error:
            print(ValidationException("ip address invalido"))
            print(self.address)
            raise ValidationException("ip address invalido")