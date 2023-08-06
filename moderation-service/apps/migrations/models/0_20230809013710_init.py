from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "moderation" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36),
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "type" VARCHAR(7) NOT NULL  /* POST: POST\nCOMMENT: COMMENT */,
    "content_id" CHAR(36) NOT NULL,
    "raw_content" JSON,
    "status" VARCHAR(16) NOT NULL  DEFAULT 'DELETE_REQUESTED' /* DELETE_REQUESTED: DELETE_REQUESTED\nDELETE_CONFIRMED: DELETE_CONFIRMED */,
    "reason" VARCHAR(17) NOT NULL  DEFAULT 'RULES_VIOLATION' /* OFFENSIVE_CONTENT: OFFENSIVE_CONTENT\nNUDITY: NUDITY\nRULES_VIOLATION: RULES_VIOLATION\nRACISM: RACISM */
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
