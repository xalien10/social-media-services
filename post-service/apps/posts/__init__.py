from apps.core.enums import TextChoices


class StatusChoices(TextChoices):
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    ARCHIVED = "ARCHIVED"


class PostCategoryChoices(TextChoices):
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


class NFTStatusChoices(TextChoices):
    READY_FOR_MINTING = "READY_FOR_MINTING"
    MINTING_IN_PROGRESS = "MINTING_IN_PROGRESS"
    MINTING_FAILED = "MINTING_FAILED"
    MINTING_COMPLETED = "MINTING_COMPLETED"
