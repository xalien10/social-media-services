from apps.core.enums import TextChoices


class StatusChoices(TextChoices):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MUTED = "MUTED"
    BANNED = "BANNED"


class InterestChoices(TextChoices):
    SPORTS = "SPORTS"
    NEWS = "NEWS"
    HEALTH = "HEALTH"
    POLITICS = "POLITICS"
    TRAVEL = "TRAVEL"
    FOOD = "FOOD"
    FICTION = "FICTION"
    TECHNOLOGY = "TECHNOLOGY"
    COMMUNICATION = "COMMUNICATION"
    INTERNATIONAL = "INTERNATIONAL"
    NATIONAL = "NATIONAL"
    CULTURAL = "CULTURAL"
    LIFE_STYLE = "LIFE_STYLE"
    FASHION = "FASHION"
    EDUCATIONAL = "EDUCATIONAL"
    PERSONAL_EVENT = "PERSONAL_EVENT"
    OTHER = "OTHER"
    MUSIC_AND_ART = "MUSIC_AND_ART"
    NOVEL_AND_POETRY = "NOVEL_AND_POETRY"
    BOOKS = "BOOKS"
    PROTEST = "PROTEST"
    SCIENTIFIC = "SCIENTIFIC"