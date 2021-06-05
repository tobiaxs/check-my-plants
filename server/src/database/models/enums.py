import enum


class Conditions(str, enum.Enum):
    """Enum for defining conditions type."""

    low = "low"
    average = "average"
    high = "high"
