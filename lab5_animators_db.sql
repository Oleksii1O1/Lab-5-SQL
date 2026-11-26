DROP DATABASE IF EXISTS `animators_db`;

CREATE DATABASE IF NOT EXISTS `animators_db`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE `animators_db`;
SET NAMES utf8mb4;

DROP TABLE IF EXISTS `payments`;
DROP TABLE IF EXISTS `order_animators`;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `animator_specializations`;
DROP TABLE IF EXISTS `agency_animators`;
DROP TABLE IF EXISTS `payment_methods`;
DROP TABLE IF EXISTS `roles`;
DROP TABLE IF EXISTS `order_statuses`;
DROP TABLE IF EXISTS `holiday_types`;
DROP TABLE IF EXISTS `clients`;
DROP TABLE IF EXISTS `specializations`;
DROP TABLE IF EXISTS `animators`;
DROP TABLE IF EXISTS `agencies`;
DROP TABLE IF EXISTS `addresses`;

CREATE TABLE `addresses` (
  `address_id` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(50) NOT NULL,
  `street` VARCHAR(100) NOT NULL,
  `building` VARCHAR(20) NOT NULL,
  `place_name` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`address_id`),
  INDEX `idx_addresses_city` (`city`)
);

CREATE TABLE `agencies` (
  `agency_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `city` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`agency_id`),
  UNIQUE INDEX `uq_agencies_name` (`name`),
  UNIQUE INDEX `uq_agencies_phone` (`phone`),
  INDEX `idx_agencies_city` (`city`)
);

CREATE TABLE `animators` (
  `animator_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `hourly_rate` DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (`animator_id`),
  UNIQUE INDEX `uq_animators_phone` (`phone`),
  INDEX `idx_animators_name` (`last_name`, `first_name`),
  INDEX `idx_animators_rate` (`hourly_rate`)
) ;

CREATE TABLE `specializations` (
  `specialization_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`specialization_id`),
  UNIQUE INDEX `uq_specializations_name` (`name`)
) ;

CREATE TABLE `clients` (
  `client_id` INT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(100) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE INDEX `uq_clients_phone` (`phone`),
  INDEX `idx_clients_full_name` (`full_name`)
) ENGINE = InnoDB;

CREATE TABLE `holiday_types` (
  `holiday_type_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`holiday_type_id`),
  UNIQUE INDEX `uq_holiday_types_name` (`name`)
);

CREATE TABLE `order_statuses` (
  `status_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`status_id`),
  UNIQUE INDEX `uq_order_statuses_name` (`name`)
) ;

CREATE TABLE `roles` (
  `role_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `uq_roles_name` (`name`)
);

CREATE TABLE `payment_methods` (
  `method_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`method_id`),
  UNIQUE INDEX `uq_payment_methods_name` (`name`)
) ;

CREATE TABLE `agency_animators` (
  `agency_id` INT NOT NULL,
  `animator_id` INT NOT NULL,
  `cooperation_start` DATE NOT NULL,
  PRIMARY KEY (`agency_id`, `animator_id`),
  INDEX `fk_aa_animator` (`animator_id`),
  CONSTRAINT `fk_aa_agency` FOREIGN KEY (`agency_id`)
    REFERENCES `agencies` (`agency_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_aa_animator` FOREIGN KEY (`animator_id`)
    REFERENCES `animators` (`animator_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `animator_specializations` (
  `animator_id` INT NOT NULL,
  `specialization_id` INT NOT NULL,
  PRIMARY KEY (`animator_id`, `specialization_id`),
  INDEX `fk_as_spec` (`specialization_id`),
  CONSTRAINT `fk_as_animator` FOREIGN KEY (`animator_id`)
    REFERENCES `animators` (`animator_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_as_spec` FOREIGN KEY (`specialization_id`)
    REFERENCES `specializations` (`specialization_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `agency_id` INT NOT NULL,
  `client_id` INT NOT NULL,
  `holiday_type_id` INT NOT NULL,
  `address_id` INT NOT NULL,
  `status_id` INT NOT NULL,
  `event_date` DATE NOT NULL,
  `start_time` TIME NOT NULL,
  `duration_minutes` INT NOT NULL,
  `total_cost` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `idx_orders_agency_date` (`agency_id`, `event_date`),
  INDEX `fk_orders_client` (`client_id`),
  INDEX `fk_orders_holiday` (`holiday_type_id`),
  INDEX `fk_orders_address` (`address_id`),
  INDEX `fk_orders_status` (`status_id`),
  INDEX `idx_orders_event_date` (`event_date`),
  CONSTRAINT `fk_orders_address` FOREIGN KEY (`address_id`)
    REFERENCES `addresses` (`address_id`),
  CONSTRAINT `fk_orders_agency` FOREIGN KEY (`agency_id`)
    REFERENCES `agencies` (`agency_id`),
  CONSTRAINT `fk_orders_client` FOREIGN KEY (`client_id`)
    REFERENCES `clients` (`client_id`),
  CONSTRAINT `fk_orders_holiday` FOREIGN KEY (`holiday_type_id`)
    REFERENCES `holiday_types` (`holiday_type_id`),
  CONSTRAINT `fk_orders_status` FOREIGN KEY (`status_id`)
    REFERENCES `order_statuses` (`status_id`)
) ;

CREATE TABLE `order_animators` (
  `order_id` INT NOT NULL,
  `animator_id` INT NOT NULL,
  `role_id` INT NOT NULL,
  `fee` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`order_id`, `animator_id`),
  INDEX `fk_oa_animator` (`animator_id`),
  INDEX `fk_oa_role` (`role_id`),
  CONSTRAINT `fk_oa_animator` FOREIGN KEY (`animator_id`)
    REFERENCES `animators` (`animator_id`),
  CONSTRAINT `fk_oa_order` FOREIGN KEY (`order_id`)
    REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_oa_role` FOREIGN KEY (`role_id`)
    REFERENCES `roles` (`role_id`)
);

CREATE TABLE `payments` (
  `payment_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `method_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `paid_at` DATE NOT NULL,
  PRIMARY KEY (`payment_id`),
  INDEX `fk_pay_order` (`order_id`),
  INDEX `fk_pay_method` (`method_id`),
  INDEX `idx_payments_paid_at` (`paid_at`),
  CONSTRAINT `fk_pay_method` FOREIGN KEY (`method_id`)
    REFERENCES `payment_methods` (`method_id`),
  CONSTRAINT `fk_pay_order` FOREIGN KEY (`order_id`)
    REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO `addresses` (`address_id`, `city`, `street`, `building`, `place_name`) VALUES
(1,  'Львів',          'вул. Городоцька',      '120',  NULL),
(2,  'Львів',          'пр. Свободи',          '15',   'Ресторан "Гарден"'),
(3,  'Львів',          'вул. Стрийська',       '30А',  'Дитячий центр "Казка"'),
(4,  'Київ',           'вул. Хрещатик',        '22',   'Готель "Прем''єр"'),
(5,  'Київ',           'просп. Перемоги',      '67',   NULL),
(6,  'Одеса',          'вул. Дерибасівська',   '10',   'Кафе "Море"'),
(7,  'Харків',         'вул. Сумська',         '45',   NULL),
(8,  'Дніпро',         'просп. Яворницького',  '88',   'Лофт "Індастрі"'),
(9,  'Тернопіль',      'вул. Руська',          '12',   NULL),
(10, 'Івано-Франківськ','вул. Незалежності',   '5',    'Банкетний зал "Мрія"'),
(11, 'Львів',          'вул. Зелена',          '201',  NULL),
(12, 'Ужгород',        'пл. Театральна',       '3',    'Ресторан "Старий замок"');

INSERT INTO `agencies` (`agency_id`, `name`, `phone`, `email`, `city`) VALUES
(1,  'Веселка',        '+380321111111', 'info@veselka.ua',   'Львів'),
(2,  'Чудо-свято',     '+380321222222', 'hello@chudo.ua',    'Львів'),
(3,  'Карнавал',       '+380441333333', 'mail@karnaval.ua',  'Київ'),
(4,  'Дитячий мир',    '+380441444444', NULL,                'Київ'),
(5,  'Сонячні усмішки','+380481555555', 'sun@smile.ua',      'Одеса'),
(6,  'Фієста',         '+380571666666', 'fiesta@mail.ua',    'Харків'),
(7,  'Чарівники',      '+380561777777', 'magic@charivnyky.ua','Дніпро'),
(8,  'Казкова країна', '+380352888888', NULL,                'Тернопіль'),
(9,  'Святкова хвиля', '+380342999999', 'wave@holiday.ua',   'Івано-Франківськ'),
(10, 'Гулі-гуляй',     '+380312000000', 'gulia@gulyai.ua',   'Ужгород');

INSERT INTO `animators` (`animator_id`, `first_name`, `last_name`, `phone`, `email`, `hourly_rate`) VALUES
(1,  'Олена',    'Коваль',     '+380501000001', 'olena.koval@mail.ua',   400.00),
(2,  'Андрій',   'Шевченко',   '+380501000002', 'andrii.sh@mail.ua',     350.00),
(3,  'Марія',    'Бондар',     '+380501000003', NULL,                    450.00),
(4,  'Ігор',     'Мельник',    '+380501000004', 'igor.m@mail.ua',        500.00),
(5,  'Наталія',  'Ткачук',     '+380501000005', 'nata.tk@mail.ua',       300.00),
(6,  'Дмитро',   'Кравченко',  '+380501000006', NULL,                    375.00),
(7,  'Софія',    'Олійник',    '+380501000007', 'sofia.o@mail.ua',       425.00),
(8,  'Максим',   'Савчук',     '+380501000008', 'max.savchuk@mail.ua',   600.00),
(9,  'Юлія',     'Гончар',     '+380501000009', NULL,                    500.00),
(10, 'Богдан',   'Паламарчук', '+380501000010', 'bohdan.p@mail.ua',      475.00),
(11, 'Катерина', 'Лисенко',    '+380501000011', 'kate.lys@mail.ua',      350.00),
(12, 'Тарас',    'Іваненко',   '+380501000012', 'taras.iv@mail.ua',      400.00);

INSERT INTO `specializations` (`specialization_id`, `name`) VALUES
(1,  'Клоунада'),
(2,  'Аквагрим'),
(3,  'Фокуси'),
(4,  'Бульбашкове шоу'),
(5,  'Пінна вечірка'),
(6,  'Ведучий'),
(7,  'Ляльковий театр'),
(8,  'Квести'),
(9,  'Науково-хімічне шоу'),
(10, 'Танцювальна анімація');

INSERT INTO `clients` (`client_id`, `full_name`, `phone`, `email`) VALUES
(1,  'Петренко Ірина Василівна',     '+380671000001', 'irina.p@gmail.com'),
(2,  'Сидоренко Олег Петрович',      '+380671000002', 'oleg.s@gmail.com'),
(3,  'Гриценко Анна Миколаївна',     '+380671000003', NULL),
(4,  'Мазур Віталій Іванович',       '+380671000004', 'vitalii.m@ukr.net'),
(5,  'Левченко Оксана Степанівна',   '+380671000005', 'oksana.l@gmail.com'),
(6,  'Романюк Павло Андрійович',     '+380671000006', NULL),
(7,  'Захарченко Леся Богданівна',   '+380671000007', 'lesia.z@ukr.net'),
(8,  'Кузьменко Артем Олексійович',  '+380671000008', 'artem.k@gmail.com'),
(9,  'Бойко Наталя Юріївна',         '+380671000009', 'natalia.b@gmail.com'),
(10, 'Поліщук Руслан Валерійович',   '+380671000010', NULL),
(11, 'Стельмах Дарина Ігорівна',     '+380671000011', 'daryna.s@ukr.net'),
(12, 'Мороз Євген Сергійович',       '+380671000012', 'yevhen.m@gmail.com');

INSERT INTO `holiday_types` (`holiday_type_id`, `name`) VALUES
(1,  'День народження'),
(2,  'Випускний'),
(3,  'Весілля'),
(4,  'Хрестини'),
(5,  'Новий рік'),
(6,  'Корпоратив'),
(7,  'Дитячий ранок'),
(8,  'Гелловін'),
(9,  'Гендер-паті'),
(10, 'Свято Миколая');

INSERT INTO `order_statuses` (`status_id`, `name`) VALUES
(1, 'Нове'),
(2, 'Підтверджено'),
(3, 'Виконано'),
(4, 'Скасовано'),
(5, 'Очікує оплати'),
(6, 'Перенесено');

INSERT INTO `roles` (`role_id`, `name`) VALUES
(1,  'Ведучий'),
(2,  'Клоун'),
(3,  'Аквагример'),
(4,  'Фокусник'),
(5,  'Помічник'),
(6,  'Аніматор-персонаж'),
(7,  'Діджей'),
(8,  'Фотограф'),
(9,  'Майстер-класів'),
(10, 'Пінне шоу');

INSERT INTO `payment_methods` (`method_id`, `name`) VALUES
(1, 'Готівка'),
(2, 'Картка'),
(3, 'Переказ на рахунок'),
(4, 'Google Pay'),
(5, 'Apple Pay'),
(6, 'PayPal');

INSERT INTO `agency_animators` (`agency_id`, `animator_id`, `cooperation_start`) VALUES
(1, 1,  '2022-03-01'),
(1, 2,  '2022-06-15'),
(1, 3,  '2023-01-10'),
(2, 4,  '2021-09-01'),
(2, 5,  '2023-04-20'),
(3, 6,  '2022-11-05'),
(3, 7,  '2023-02-14'),
(4, 8,  '2021-05-30'),
(4, 9,  '2024-01-08'),
(5, 10, '2022-08-19'),
(5, 11, '2023-07-01'),
(6, 12, '2024-03-12'),
(7, 1,  '2024-05-01'),
(8, 5,  '2024-06-10');

INSERT INTO `animator_specializations` (`animator_id`, `specialization_id`) VALUES
(1, 1), (1, 2),
(2, 3), (2, 6),
(3, 2),
(4, 6), (4, 7),
(5, 4),
(6, 5),
(7, 8),
(8, 9),
(9, 10),
(10, 1);

INSERT INTO `animator_specializations` (`animator_id`, `specialization_id`) VALUES
(11, 3),
(12, 6);

INSERT INTO `orders` (`order_id`, `agency_id`, `client_id`, `holiday_type_id`, `address_id`, `status_id`, `event_date`, `start_time`, `duration_minutes`, `total_cost`) VALUES
(1,  1, 1,  1,  1,  3, '2026-05-12', '14:00:00', 120, 1500.00),
(2,  1, 2,  7,  3,  3, '2026-05-25', '10:00:00',  90,  900.00),
(3,  2, 3,  3,  2,  3, '2026-06-10', '16:00:00', 180, 1600.00),
(4,  3, 4,  4,  4,  3, '2026-06-22', '12:00:00',  60,  750.00),
(5,  3, 5,  1,  5,  3, '2026-07-05', '15:00:00', 120,  850.00),
(6,  4, 6,  2,  6,  3, '2026-07-18', '18:00:00', 150, 1200.00),
(7,  5, 7,  6,  7,  3, '2026-08-03', '19:00:00', 180, 1650.00),
(8,  6, 8,  8,  8,  3, '2026-08-14', '17:00:00', 120,  800.00),
(9,  7, 9,  9,  9,  2, '2026-11-08', '13:00:00', 120, 1100.00),
(10, 8, 10, 10, 10, 2, '2026-12-19', '11:00:00',  90,  900.00),
(11, 4, 11, 5,  11, 5, '2026-12-28', '16:00:00', 120, 1000.00),
(12, 2, 12, 5,  12, 1, '2026-12-30', '18:00:00', 120, 1050.00);

INSERT INTO `order_animators` (`order_id`, `animator_id`, `role_id`, `fee`) VALUES
(1,  1,  1, 800.00),
(1,  2,  2, 700.00),
(2,  3,  1, 900.00),
(3,  4,  1, 1000.00),
(3,  5,  5, 600.00),
(4,  6,  6, 750.00),
(5,  7,  2, 850.00),
(6,  8,  1, 1200.00),
(7,  10, 1, 950.00),
(7,  11, 5, 700.00),
(8,  12, 1, 800.00),
(9,  1,  6, 1100.00),
(10, 5,  1, 900.00),
(11, 9,  2, 1000.00),
(12, 4,  1, 1050.00);

INSERT INTO `payments` (`payment_id`, `order_id`, `method_id`, `amount`, `paid_at`) VALUES
(1,  1,  1, 750.00,  '2026-05-01'),
(2,  1,  2, 750.00,  '2026-05-12'),
(3,  2,  2, 900.00,  '2026-05-20'),
(4,  3,  1, 800.00,  '2026-06-01'),
(5,  3,  3, 800.00,  '2026-06-10'),
(6,  4,  2, 750.00,  '2026-06-20'),
(7,  5,  3, 850.00,  '2026-07-02'),
(8,  6,  2, 600.00,  '2026-07-15'),
(9,  7,  1, 1650.00, '2026-08-01'),
(10, 8,  4, 800.00,  '2026-08-10'),
(11, 9,  2, 550.00,  '2026-10-05'),
(12, 10, 5, 450.00,  '2026-10-20');

INSERT INTO animator_reviews (`review_id`, animator_id, `rating`, comment, `review_date`) VALUES
(1,  1, 5, 'Чудова аніматорка, діти в захваті від клоунади!', '2026-05-15'),
(2,  1, 5, 'Прекрасний аквагрим, дуже професійно!', '2026-06-02'),
(3,  2, 4, 'Гарні фокуси, але запізнився на 5 хвилин.', '2026-06-12'),
(4,  3, 5, 'Найкраща ведуча для дитячого свята!', '2026-07-01'),
(5,  4, 5, 'Ляльковий театр вразив усіх батьків.', '2026-07-20'),
(6,  5, 4, 'Бульбашкове шоу було видовищним.', '2026-08-05'),
(7,  6, 5, 'Пінна вечірка просто супер!', '2026-08-15'),
(8,  7, 5, 'Квест дуже продуманий та цікавий.', '2026-09-01'),
(9,  8, 5, 'Хімічні досліди захопили дітей старшого віку.', '2026-09-20'),
(10, 10, 4, 'Веселий клоун, гарний настрій на все свято.', '2026-10-10');

USE `animators_db`;

DROP TABLE IF EXISTS `animator_reviews`;

CREATE TABLE `animator_reviews` (
  `review_id` INT NOT NULL AUTO_INCREMENT,
  `animator_id` INT NOT NULL,
  `rating` INT NOT NULL,
  `comment` VARCHAR(255) NULL DEFAULT NULL,
  `review_date` DATE NOT NULL,
  PRIMARY KEY (`review_id`),
  INDEX `idx_reviews_animator` (`animator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TABLE IF EXISTS `animator_audit_logs`;

CREATE TABLE `animator_audit_logs` (
  `log_id` INT NOT NULL AUTO_INCREMENT,
  `animator_id` INT NOT NULL,
  `old_hourly_rate` DECIMAL(8,2) NOT NULL,
  `new_hourly_rate` DECIMAL(8,2) NOT NULL,
  `modified_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `details` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  INDEX `idx_audit_animator` (`animator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DROP TRIGGER IF EXISTS `trg_reviews_check_fk_insert`;
DELIMITER //
CREATE TRIGGER `trg_reviews_check_fk_insert`
BEFORE INSERT ON `animator_reviews`
FOR EACH ROW
BEGIN
    DECLARE v_exists INT DEFAULT 0;
    SELECT COUNT(*) INTO v_exists FROM `animators` WHERE `animator_id` = NEW.`animator_id`;
    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Trigger FK Error: animator_id does not exist in table animators';
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_reviews_check_fk_update`;
DELIMITER //
CREATE TRIGGER `trg_reviews_check_fk_update`
BEFORE UPDATE ON `animator_reviews`
FOR EACH ROW
BEGIN
    DECLARE v_exists INT DEFAULT 0;
    SELECT COUNT(*) INTO v_exists FROM `animators` WHERE `animator_id` = NEW.`animator_id`;
    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Trigger FK Error: animator_id does not exist in table animators';
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_animators_restrict_delete`;
DELIMITER //
CREATE TRIGGER `trg_animators_restrict_delete`
BEFORE DELETE ON `animators`
FOR EACH ROW
BEGIN
    DECLARE v_count INT DEFAULT 0;
    SELECT COUNT(*) INTO v_count FROM `animator_reviews` WHERE `animator_id` = OLD.`animator_id`;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Trigger Integrity Error: Cannot delete animator with existing reviews in animator_reviews';
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_animators_cascade_update`;
DELIMITER //
CREATE TRIGGER `trg_animators_cascade_update`
AFTER UPDATE ON `animators`
FOR EACH ROW
BEGIN
    IF OLD.`animator_id` <> NEW.`animator_id` THEN
        UPDATE `animator_reviews`
        SET `animator_id` = NEW.`animator_id`
        WHERE `animator_id` = OLD.`animator_id`;
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_payments_prevent_delete`;
DELIMITER //
CREATE TRIGGER `trg_payments_prevent_delete`
BEFORE DELETE ON `payments`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Trigger Error: Deletion of payments is strictly forbidden for financial integrity';
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_animators_log_update`;
DELIMITER //
CREATE TRIGGER `trg_animators_log_update`
AFTER UPDATE ON `animators`
FOR EACH ROW
BEGIN
    IF OLD.`hourly_rate` <> NEW.`hourly_rate` THEN
        INSERT INTO `animator_audit_logs` (
            `animator_id`,
            `old_hourly_rate`,
            `new_hourly_rate`,
            `modified_at`,
            `details`
        ) VALUES (
            NEW.`animator_id`,
            OLD.`hourly_rate`,
            NEW.`hourly_rate`,
            NOW(),
            CONCAT('Hourly rate changed from ', OLD.`hourly_rate`, ' to ', NEW.`hourly_rate`)
        );
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_animators_no_double_zeros_insert`;
DELIMITER //
CREATE TRIGGER `trg_animators_no_double_zeros_insert`
BEFORE INSERT ON `animators`
FOR EACH ROW
BEGIN
    IF MOD(ROUND(NEW.`hourly_rate`), 100) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Trigger Error: Hourly rate cannot end with two zeros (e.g. 300, 400, 500)';
    END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS `trg_animators_no_double_zeros_update`;
DELIMITER //
CREATE TRIGGER `trg_animators_no_double_zeros_update`
BEFORE UPDATE ON `animators`
FOR EACH ROW
BEGIN
    IF MOD(ROUND(NEW.`hourly_rate`), 100) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Trigger Error: Hourly rate cannot end with two zeros (e.g. 300, 400, 500)';
    END IF;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_insert_client`;
DELIMITER //
CREATE PROCEDURE `sp_insert_client`(
    IN  p_full_name VARCHAR(100),
    IN  p_phone     VARCHAR(20),
    IN  p_email     VARCHAR(100),
    OUT p_client_id INT
)
BEGIN
    INSERT INTO `clients` (`full_name`, `phone`, `email`)
    VALUES (p_full_name, p_phone, p_email);

    SET p_client_id = LAST_INSERT_ID();
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_link_animator_specialization`;
DELIMITER //
CREATE PROCEDURE `sp_link_animator_specialization`(
    IN p_first_name          VARCHAR(50),
    IN p_last_name           VARCHAR(50),
    IN p_specialization_name VARCHAR(50)
)
BEGIN
    DECLARE v_animator_id INT;
    DECLARE v_spec_id INT;

    SELECT `animator_id` INTO v_animator_id
    FROM `animators`
    WHERE `first_name` = p_first_name AND `last_name` = p_last_name
    LIMIT 1;

    IF v_animator_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Animator with given first_name and last_name not found';
    END IF;

    SELECT `specialization_id` INTO v_spec_id
    FROM `specializations`
    WHERE `name` = p_specialization_name
    LIMIT 1;

    IF v_spec_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Specialization with given name not found';
    END IF;

    INSERT INTO `animator_specializations` (`animator_id`, `specialization_id`)
    VALUES (v_animator_id, v_spec_id);

    SELECT v_animator_id AS `animator_id`, v_spec_id AS `specialization_id`, 'Successfully linked' AS `status`;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_insert_ten_nonames`;
DELIMITER //
CREATE PROCEDURE `sp_insert_ten_nonames`()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE v_max_num INT DEFAULT 0;
    DECLARE v_name VARCHAR(50);

    SELECT IFNULL(MAX(CAST(SUBSTRING(`name`, 7) AS UNSIGNED)), 0)
    INTO v_max_num
    FROM `specializations`
    WHERE `name` REGEXP '^Noname[0-9]+$';

    WHILE i <= 10 DO
        SET v_name = CONCAT('Noname', (v_max_num + i));
        INSERT INTO `specializations` (`name`) VALUES (v_name);
        SET i = i + 1;
    END WHILE;

    SELECT CONCAT('Successfully inserted 10 nonames from Noname', (v_max_num + 1), ' to Noname', (v_max_num + 10)) AS `result`;
END //
DELIMITER ;

DROP FUNCTION IF EXISTS `fn_get_avg_hourly_rate`;
DELIMITER //
CREATE FUNCTION `fn_get_avg_hourly_rate`()
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_avg DECIMAL(10,2);
    SELECT IFNULL(AVG(`hourly_rate`), 0.00) INTO v_avg FROM `animators`;
    RETURN v_avg;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_get_animators_above_avg_rate`;
DELIMITER //
CREATE PROCEDURE `sp_get_animators_above_avg_rate`()
BEGIN
    SELECT
        `animator_id`,
        `first_name`,
        `last_name`,
        `hourly_rate`,
        `fn_get_avg_hourly_rate`() AS `average_hourly_rate`,
        ROUND(`hourly_rate` - `fn_get_avg_hourly_rate`(), 2) AS `difference_from_avg`
    FROM `animators`
    WHERE `hourly_rate` >= `fn_get_avg_hourly_rate`()
    ORDER BY `hourly_rate` DESC;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS `sp_cursor_split_animators`;
DELIMITER //
CREATE PROCEDURE `sp_cursor_split_animators`(
    OUT p_table1 VARCHAR(64),
    OUT p_table2 VARCHAR(64),
    OUT p_total_rows INT,
    OUT p_rows_t1 INT,
    OUT p_rows_t2 INT
)
BEGIN
    DECLARE v_done INT DEFAULT FALSE;
    DECLARE v_id INT;
    DECLARE v_fname VARCHAR(50);
    DECLARE v_lname VARCHAR(50);
    DECLARE v_phone VARCHAR(20);
    DECLARE v_email VARCHAR(100);
    DECLARE v_rate DECIMAL(8,2);
    DECLARE v_ts VARCHAR(32);
    DECLARE v_t1 VARCHAR(64);
    DECLARE v_t2 VARCHAR(64);
    DECLARE v_target VARCHAR(64);
    DECLARE v_count_t1 INT DEFAULT 0;
    DECLARE v_count_t2 INT DEFAULT 0;
    DECLARE v_total INT DEFAULT 0;

    DECLARE cur_anim CURSOR FOR
        SELECT `animator_id`, `first_name`, `last_name`, `phone`, `email`, `hourly_rate`
        FROM `animators`;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

    SET v_ts = DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s');
    SET v_t1 = CONCAT('animators_split1_', v_ts);
    SET v_t2 = CONCAT('animators_split2_', v_ts);

    SET @sql1 = CONCAT('CREATE TABLE `', v_t1, '` LIKE `animators`;');
    PREPARE stmt1 FROM @sql1;
    EXECUTE stmt1;
    DEALLOCATE PREPARE stmt1;

    SET @sql2 = CONCAT('CREATE TABLE `', v_t2, '` LIKE `animators`;');
    PREPARE stmt2 FROM @sql2;
    EXECUTE stmt2;
    DEALLOCATE PREPARE stmt2;

    OPEN cur_anim;

    read_loop: LOOP
        FETCH cur_anim INTO v_id, v_fname, v_lname, v_phone, v_email, v_rate;
        IF v_done THEN
            LEAVE read_loop;
        END IF;

        SET v_total = v_total + 1;

        IF RAND() < 0.5 THEN
            SET v_target = v_t1;
            SET v_count_t1 = v_count_t1 + 1;
        ELSE
            SET v_target = v_t2;
            SET v_count_t2 = v_count_t2 + 1;
        END IF;

        SET @sql_ins = CONCAT('INSERT INTO `', v_target,
            '` (`animator_id`, `first_name`, `last_name`, `phone`, `email`, `hourly_rate`) VALUES (?, ?, ?, ?, ?, ?)');
        SET @p_id = v_id;
        SET @p_fname = v_fname;
        SET @p_lname = v_lname;
        SET @p_phone = v_phone;
        SET @p_email = v_email;
        SET @p_rate = v_rate;

        PREPARE stmt_ins FROM @sql_ins;
        EXECUTE stmt_ins USING @p_id, @p_fname, @p_lname, @p_phone, @p_email, @p_rate;
        DEALLOCATE PREPARE stmt_ins;
    END LOOP;

    CLOSE cur_anim;

    SET p_table1 = v_t1;
    SET p_table2 = v_t2;
    SET p_total_rows = v_total;
    SET p_rows_t1 = v_count_t1;
    SET p_rows_t2 = v_count_t2;

    SELECT
        v_t1 AS `table1_name`,
        v_count_t1 AS `table1_rows`,
        v_t2 AS `table2_name`,
        v_count_t2 AS `table2_rows`,
        v_total AS `total_rows_processed`;
END //
DELIMITER ;
