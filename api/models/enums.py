import enum

class ApplicationStatus(enum.Enum):
    APPROVED = "APPROVED"
    REQUESTED = "REQUESTED"
    ISSUED = "ISSUED"
    EXPIRED = "EXPIRED"
    SUSPEND = "SUSPEND"
