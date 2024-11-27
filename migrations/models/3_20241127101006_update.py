from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_mobile_319e6a`;
        ALTER TABLE `user` DROP INDEX `idx_user_email_1b4f1c`;
        ALTER TABLE `user` ADD `is_delete` BOOL NOT NULL  COMMENT '是否删除' DEFAULT 0;
        ALTER TABLE `user` ADD `delete_at` DATETIME(6)   COMMENT '删除时间';
        CREATE  INDEX `idx_user_email_1b4f1c` ON `user` (`email`);
        CREATE  INDEX `idx_user_mobile_319e6a` ON `user` (`mobile`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_mobile_319e6a`;
        ALTER TABLE `user` DROP INDEX `idx_user_email_1b4f1c`;
        ALTER TABLE `user` DROP COLUMN `is_delete`;
        ALTER TABLE `user` DROP COLUMN `delete_at`;
        CREATE  INDEX `idx_user_email_1b4f1c` ON `user` (`email`);
        CREATE  INDEX `idx_user_mobile_319e6a` ON `user` (`mobile`);"""
