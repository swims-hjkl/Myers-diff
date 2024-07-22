from dataclasses import dataclass
from enum import Enum


class DiffType(Enum):

    INSERTED = "INSERTED"
    DELETED = "DELETED"
    EQUALS = "EQUALS"


@dataclass
class DiffDescriptor():

    diff_type: DiffType
    from_index: int
    to_index: int
