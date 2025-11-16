from enum import Enum


class Statuses(Enum):
    NEW = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CLOSED = 4
    PENDING = 5
    BLOCKED = 6

    @classmethod
    def choices(cls):
        return [(attr.value, attr.name) for attr in cls]


class Priority(Enum):
    LOW = 5
    MEDIUM = 4
    HIGH = 3
    VERY_HIGH = 2
    URGENT = 1

    @classmethod
    def choices(cls):
        return [(attr.value, attr.name) for attr in cls]
