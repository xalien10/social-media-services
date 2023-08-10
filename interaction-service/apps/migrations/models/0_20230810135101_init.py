from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "comment" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36) NOT NULL,
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "post_id" CHAR(36) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "comment_nft" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36) NOT NULL,
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "description" TEXT NOT NULL,
    "data" JSON NOT NULL,
    "token_uri" VARCHAR(150),
    "status" VARCHAR(19) NOT NULL  DEFAULT 'READY_FOR_MINTING' /* READY_FOR_MINTING: READY_FOR_MINTING\nMINTING_IN_PROGRESS: MINTING_IN_PROGRESS\nMINTING_FAILED: MINTING_FAILED\nMINTING_COMPLETED: MINTING_COMPLETED */,
    "comment_id" CHAR(36) NOT NULL REFERENCES "comment" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "reaction" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36) NOT NULL,
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "post_id" CHAR(36) NOT NULL,
    "type" VARCHAR(5) NOT NULL  DEFAULT 'LIKE' /* LIKE: LIKE\nLOVE: LOVE\nANGRY: ANGRY\nSAD: SAD\nFUNNY: FUNNY\nJOY: JOY */,
    CONSTRAINT "uid_reaction_post_id_d92b9e" UNIQUE ("post_id", "created_by")
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
