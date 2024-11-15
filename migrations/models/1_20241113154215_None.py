from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(32) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL  COMMENT '密码',
    `nickname` VARCHAR(32)   COMMENT '昵称',
    `email` VARCHAR(128)  UNIQUE COMMENT '邮箱',
    `mobile` VARCHAR(32)  UNIQUE COMMENT '手机号码',
    `is_active` BOOL NOT NULL  COMMENT '是否激活' DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL  COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL  COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE  INDEX `idx_user_email_1b4f1c` ON `user` (`email`);
CREATE  INDEX `idx_user_mobile_319e6a` ON `user` (`mobile`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
