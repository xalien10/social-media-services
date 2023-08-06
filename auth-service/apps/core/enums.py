from enum import Enum


class TextChoices(str, Enum):

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def names(cls) -> list[str]:
        return [item.name for item in cls]

    @classmethod
    def dict(cls) -> dict[str, str]:
        return {item.name: item.value for item in cls}


class IntegerChoices(int, Enum):

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]

    @classmethod
    def names(cls) -> list[str]:
        return [item.name for item in cls]

    @classmethod
    def dict(cls) -> dict[str, str]:
        return {item.name: item.value for item in cls}
