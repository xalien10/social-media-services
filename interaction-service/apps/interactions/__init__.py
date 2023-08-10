from apps.core.enums import TextChoices


class ReactionChoices(TextChoices):
    LIKE = "LIKE"
    LOVE = "LOVE"
    ANGRY = "ANGRY"
    SAD = "SAD"
    FUNNY = "FUNNY"
    JOY = "JOY"


class ReactionGroups(TextChoices):
    POSITIVE_REACTION = [ReactionChoices.LIKE, ReactionChoices.LOVE, ReactionChoices.FUNNY, ReactionChoices.JOY]
    NEGATIVE_REACTION = [ReactionChoices.SAD, ReactionChoices.ANGRY]


class NFTStatusChoices(TextChoices):
    READY_FOR_MINTING = "READY_FOR_MINTING"
    MINTING_IN_PROGRESS = "MINTING_IN_PROGRESS"
    MINTING_FAILED = "MINTING_FAILED"
    MINTING_COMPLETED = "MINTING_COMPLETED"
