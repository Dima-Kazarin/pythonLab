from dataclasses import dataclass, field
import uuid


@dataclass
class Passenger:
    place: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Seats:
    class_type: str
    number_of_row: int
    position_in_row: str
    id: str
    passenger: Passenger = None

    def __post_init__(self):
        if not (1 <= self.number_of_row):
            raise ValueError('Invalid number of row')
        if not ('a' <= self.position_in_row <= 'f'):
            raise ValueError('Invalid position in row')
        if not (self.class_type in ('business', 'econom')):
            raise ValueError('Invalid class type')

        if self.id is None:
            self.id = f'{self.number_of_row}_{self.position_in_row}'
