-- comments.sql
CREATE TABLE `comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `parent_id` INT DEFAULT NULL,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `website` VARCHAR(255) DEFAULT NULL,
  `comment_text` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL,
  `is_approved` TINYINT(1) DEFAULT 0,
  `is_flagged` TINYINT(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`parent_id`) REFERENCES `comments`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;