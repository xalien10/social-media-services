from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "post" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36) NOT NULL,
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "title" VARCHAR(100),
    "content" TEXT NOT NULL,
    "types" text[] NOT NULL,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'DRAFT' /* DRAFT: DRAFT\nPOSTED: POSTED\nARCHIVED: ARCHIVED */,
    "total_views" INT   DEFAULT 0,
    "total_comments" INT   DEFAULT 0,
    "total_reactions" INT   DEFAULT 0,
    "score" REAL   DEFAULT 0,
    "popularity" REAL   DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "post_nft" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "created_by" CHAR(36) NOT NULL,
    "updated_at" TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    "updated_by" CHAR(36),
    "title" VARCHAR(100),
    "description" TEXT NOT NULL,
    "data" JSON NOT NULL,
    "token_uri" VARCHAR(150),
    "status" VARCHAR(19) NOT NULL  DEFAULT 'READY_FOR_MINTING' /* READY_FOR_MINTING: READY_FOR_MINTING\nMINTING_IN_PROGRESS: MINTING_IN_PROGRESS\nMINTING_FAILED: MINTING_FAILED\nMINTING_COMPLETED: MINTING_COMPLETED */,
    "post_id" CHAR(36) NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
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
