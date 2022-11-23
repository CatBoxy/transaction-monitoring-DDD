from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AddBulkCommand():
    fileData: Iterable[str]