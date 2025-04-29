DROP DATABASE IF EXISTS szkot;
START TRANSACTION;

CREATE DATABASE IF NOT EXISTS szkot;
USE szkot;

CREATE TABLE IF NOT EXISTS `przewoznicy` (
    `id_przewoznika` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `nazwa` VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `pasazerowie` (
    `id_pasażera` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `imie` VARCHAR(255) NOT NULL,
    `nazwisko` VARCHAR(255) NOT NULL,
    `mail` VARCHAR(255) NOT NULL,
    `telefon` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id_pasażera`)
);

CREATE TABLE IF NOT EXISTS `stacje_kolejowe` (
    `id_stacji` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `nazwa_stacji` VARCHAR(255) NOT NULL,
    `miasto` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id_stacji`)
);

CREATE TABLE IF NOT EXISTS `linie_kolejowe` (
    `id_linii` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `nazwa_linii` VARCHAR(255) NOT NULL,
    `id_stacji` INT UNSIGNED NOT NULL,
    `id_przewoznika` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`id_linii`)
);

CREATE TABLE IF NOT EXISTS `pociagi` (
    `id_pociągu` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `model_pociągu` VARCHAR(255) NOT NULL,
    `id_wagonu` INT UNSIGNED NOT NULL,
    `id_przewoźnika` INT UNSIGNED NOT NULL,
    `id_aktualna_stacja` INT UNSIGNED NOT NULL,
    `stan` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id_pociągu`)
);

CREATE TABLE IF NOT EXISTS `wagony` (
    `id_wagonu` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `liczba_miejsc` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (`id_wagonu`)
);

CREATE TABLE IF NOT EXISTS `polaczenia` (
    `id_połączenia` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `id_lini` INT UNSIGNED NOT NULL,
    `id_stacji_początkowej` INT UNSIGNED NOT NULL,
    `id_stacji_końcowej` INT UNSIGNED NOT NULL,
    `id_pociągu` INT UNSIGNED NOT NULL,
    `czas_przejazdu` TIME NOT NULL,
    `data` DATE NOT NULL,
    `opóźnienie` TIME NOT NULL,
    PRIMARY KEY (`id_połączenia`)
);

CREATE TABLE IF NOT EXISTS `bilety` (
    `id_biletu` INT UNSIGNED AUTO_INCREMENT NOT NULL,
    `id_pasażera` INT UNSIGNED,
    `id_połączenia` INT UNSIGNED NOT NULL,
    `cena` SMALLINT UNSIGNED NOT NULL,
    `ulgi` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id_biletu`)
);

-- FOREIGN KEYS

ALTER TABLE `bilety`
ADD CONSTRAINT `fk_bilety_id_pasażera` FOREIGN KEY (`id_pasażera`) REFERENCES `pasazerowie`(`id_pasażera`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `bilety`
ADD CONSTRAINT `fk_bilety_id_polaczenia` FOREIGN KEY (`id_połączenia`) REFERENCES `polaczenia`(`id_połączenia`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `pociagi`
ADD CONSTRAINT `fk_pociagi_id_wagonu` FOREIGN KEY (`id_wagonu`) REFERENCES `wagony`(`id_wagonu`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `pociagi`
ADD CONSTRAINT `fk_pociagi_id_aktualna_stacja` FOREIGN KEY (`id_aktualna_stacja`) REFERENCES `stacje_kolejowe`(`id_stacji`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `polaczenia`
ADD CONSTRAINT `fk_polaczenia_id_pociągu` FOREIGN KEY (`id_pociągu`) REFERENCES `pociagi`(`id_pociągu`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `polaczenia`
ADD CONSTRAINT `fk_polaczenia_id_linii` FOREIGN KEY (`id_lini`) REFERENCES `linie_kolejowe`(`id_linii`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `polaczenia`
ADD CONSTRAINT `fk_polaczenia_id_stacji_końcowej` FOREIGN KEY (`id_stacji_końcowej`) REFERENCES `stacje_kolejowe`(`id_stacji`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `polaczenia`
ADD CONSTRAINT `fk_polaczenia_id_stacji_początkowej` FOREIGN KEY (`id_stacji_początkowej`) REFERENCES `stacje_kolejowe`(`id_stacji`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `linie_kolejowe`
ADD CONSTRAINT `fk_linie_kolejowe_id_stacji` FOREIGN KEY (`id_stacji`) REFERENCES `stacje_kolejowe`(`id_stacji`)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE `linie_kolejowe`
ADD CONSTRAINT `fk_linie_kolejowe_id_przewoznika` FOREIGN KEY (`id_przewoznika`) REFERENCES `przewoznicy`(`id_przewoznika`)
ON UPDATE CASCADE ON DELETE RESTRICT;

COMMIT;
