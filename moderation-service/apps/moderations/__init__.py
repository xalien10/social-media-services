from apps.core.enums import TextChoices


class ContentTypes(TextChoices):
    POST = "POST"
    COMMENT = "COMMENT"


class StatusChoices(TextChoices):
    DELETE_REQUESTED = "DELETE_REQUESTED"
    DELETE_CONFIRMED = "DELETE_CONFIRMED"


class ModerationReasons(TextChoices):
    OFFENSIVE_CONTENT = "OFFENSIVE_CONTENT"
    NUDITY = "NUDITY"
    RULES_VIOLATION = "RULES_VIOLATION"
    RACISM = "RACISM"
