from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36),
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "email" VARCHAR(50) NOT NULL UNIQUE,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "password" VARCHAR(128) NOT NULL,
    "is_verified" INT   DEFAULT 0,
    "date_joined" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "rating" REAL   DEFAULT 0,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'INACTIVE' /* ACTIVE: ACTIVE\nINACTIVE: INACTIVE\nMUTED: MUTED\nBANNED: BANNED */,
    "interests" text[] NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_token" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36),
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_user" (
    "user_rel_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
