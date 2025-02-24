from enum import Enum


class Statuses(str, Enum):
    IN_QUEUE = "In Queue"
    RUN = "Run"
    COMPLETED = "Completed"
