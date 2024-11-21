from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_email_1b4f1c`;
        ALTER TABLE `user` DROP INDEX `idx_user_mobile_319e6a`;
        ALTER TABLE `user` ADD `is_superuser` BOOL NOT NULL  COMMENT '是否是超级管理员' DEFAULT 0;
        CREATE  INDEX `idx_user_email_1b4f1c` ON `user` (`email`);
        CREATE  INDEX `idx_user_mobile_319e6a` ON `user` (`mobile`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP INDEX `idx_user_mobile_319e6a`;
        ALTER TABLE `user` DROP INDEX `idx_user_email_1b4f1c`;
        ALTER TABLE `user` DROP COLUMN `is_superuser`;
        CREATE  INDEX `idx_user_mobile_319e6a` ON `user` (`mobile`);
        CREATE  INDEX `idx_user_email_1b4f1c` ON `user` (`email`);"""
