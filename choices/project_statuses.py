from enum import StrEnum


class ProjectStatus(StrEnum):
    ACTIVE = "Active"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    PLANNING = "Planning"

    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]
