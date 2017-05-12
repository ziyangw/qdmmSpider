CREATE DATABASE qdmmdb;
CREATE TABLE `qdmminfo` (
	`title` text NOT NULL,
    `author` text NOT NULL,
    `link` text NOT NULL,
    `key` int(12) NOT NULL,
    `cover_url` text NOT NULL,
    `intro` longtext NOT NULL,
    `catalog` text NOT NULL,
    `genre` text NOT NULL,
    `progress` text NOT NULL,
    `total_hit` text NOT NULL,
    `total_recmd` text NOT NULL,
    `month_hit` text NOT NULL,
    `month_recmd` text NOT NULL,
    `week_hit` text NOT NULL,
    `week_recmd` text NOT NULL,
    `word_count` text NOT NULL,
    `chapter_info` longtext NOT NULL,
    `update_time` datetime(6) NOT NULL,
    `added_time` datetime(6) NOT NULL,
    `created_time` datetime(6) NOT NULL,
    PRIMARY KEY (`key`)
)ENGINE = MyISAM DEFAULT CHARSET = utf8;