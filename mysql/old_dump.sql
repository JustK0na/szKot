CREATE DATABASE  IF NOT EXISTS `railway` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `railway`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: railway
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bilety`
--

DROP TABLE IF EXISTS `bilety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bilety` (
  `id_biletu` bigint NOT NULL,
  `id_pasazera` bigint DEFAULT NULL,
  `id_polaczenia` bigint DEFAULT NULL,
  `cena` int DEFAULT NULL,
  `ulgi` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_biletu`),
  KEY `fk_bilety_pasazer` (`id_pasazera`),
  KEY `fk_bilety_polaczenie` (`id_polaczenia`),
  CONSTRAINT `fk_bilety_pasazer` FOREIGN KEY (`id_pasazera`) REFERENCES `pasazerowie` (`id_pasazera`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_bilety_polaczenie` FOREIGN KEY (`id_polaczenia`) REFERENCES `polaczenie` (`id_polaczenia`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilety`
--

LOCK TABLES `bilety` WRITE;
/*!40000 ALTER TABLE `bilety` DISABLE KEYS */;
/*!40000 ALTER TABLE `bilety` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linia_kolejowa`
--

DROP TABLE IF EXISTS `linia_kolejowa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `linia_kolejowa` (
  `id_linii` bigint NOT NULL,
  `nazwa_linii` varchar(255) DEFAULT NULL,
  `id_stacji` bigint DEFAULT NULL,
  PRIMARY KEY (`id_linii`),
  KEY `fk_linia_stacja` (`id_stacji`),
  CONSTRAINT `fk_linia_stacja` FOREIGN KEY (`id_stacji`) REFERENCES `stacja_kolejowa` (`id_stacji`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linia_kolejowa`
--

LOCK TABLES `linia_kolejowa` WRITE;
/*!40000 ALTER TABLE `linia_kolejowa` DISABLE KEYS */;
/*!40000 ALTER TABLE `linia_kolejowa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pasazerowie`
--

DROP TABLE IF EXISTS `pasazerowie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasazerowie` (
  `id_pasazera` bigint NOT NULL,
  `imie` varchar(255) DEFAULT NULL,
  `nazwisko` varchar(255) DEFAULT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `telefon` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_pasazera`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasazerowie`
--

LOCK TABLES `pasazerowie` WRITE;
/*!40000 ALTER TABLE `pasazerowie` DISABLE KEYS */;
INSERT INTO `pasazerowie` VALUES (1,'Jan','Kowalski','jan.kowalski@mail.com','123456789'),(2,'Anna','Nowak','anna.nowak@mail.com','987654321'),(3,'Piotr','Zieliński','piotr.zielinski@mail.com','112233445'),(4,'Maria','Wiśniewska','maria.wisniewska@mail.com','223344556'),(5,'Jan','Kowalski','jan.kowalski@mail.com','123456789'),(6,'Anna','Nowak','anna.nowak@mail.com','987654321'),(7,'Piotr','Zieliński','piotr.zielinski@mail.com','112233445'),(8,'Maria','Wiśniewska','maria.wisniewska@mail.com','223344556');
/*!40000 ALTER TABLE `pasazerowie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pociag`
--

DROP TABLE IF EXISTS `pociag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pociag` (
  `id_pociagu` bigint NOT NULL,
  `model_pociagu` varchar(255) DEFAULT NULL,
  `id_wagonu` bigint DEFAULT NULL,
  `id_przewoznika` bigint DEFAULT NULL,
  `id_aktualna_stacja` bigint DEFAULT NULL,
  `stan` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_pociagu`),
  KEY `fk_pociag_wagon` (`id_wagonu`),
  KEY `fk_pociag_przewoznik` (`id_przewoznika`),
  KEY `fk_pociag_stacja` (`id_aktualna_stacja`),
  CONSTRAINT `fk_pociag_przewoznik` FOREIGN KEY (`id_przewoznika`) REFERENCES `przewoznik` (`id_przewoznika`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_pociag_stacja` FOREIGN KEY (`id_aktualna_stacja`) REFERENCES `stacja_kolejowa` (`id_stacji`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_pociag_wagon` FOREIGN KEY (`id_wagonu`) REFERENCES `wagon` (`id_wagonu`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pociag`
--

LOCK TABLES `pociag` WRITE;
/*!40000 ALTER TABLE `pociag` DISABLE KEYS */;
/*!40000 ALTER TABLE `pociag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `polaczenie`
--

DROP TABLE IF EXISTS `polaczenie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `polaczenie` (
  `id_polaczenia` bigint NOT NULL,
  `id_linii` bigint DEFAULT NULL,
  `id_stacji_poczatkowej` bigint DEFAULT NULL,
  `id_stacji_koncowej` bigint DEFAULT NULL,
  `id_pociagu` bigint DEFAULT NULL,
  `czas_przejazdu` bigint DEFAULT NULL,
  `data` bigint DEFAULT NULL,
  `opoznienie` bigint DEFAULT NULL,
  PRIMARY KEY (`id_polaczenia`),
  KEY `fk_polaczenie_linia` (`id_linii`),
  KEY `fk_polaczenie_pociag` (`id_pociagu`),
  KEY `fk_polaczenie_stacja_start` (`id_stacji_poczatkowej`),
  KEY `fk_polaczenie_stacja_koniec` (`id_stacji_koncowej`),
  CONSTRAINT `fk_polaczenie_linia` FOREIGN KEY (`id_linii`) REFERENCES `linia_kolejowa` (`id_linii`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_polaczenie_pociag` FOREIGN KEY (`id_pociagu`) REFERENCES `pociag` (`id_pociagu`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_polaczenie_stacja_koniec` FOREIGN KEY (`id_stacji_koncowej`) REFERENCES `stacja_kolejowa` (`id_stacji`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_polaczenie_stacja_start` FOREIGN KEY (`id_stacji_poczatkowej`) REFERENCES `stacja_kolejowa` (`id_stacji`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polaczenie`
--

LOCK TABLES `polaczenie` WRITE;
/*!40000 ALTER TABLE `polaczenie` DISABLE KEYS */;
/*!40000 ALTER TABLE `polaczenie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `przewoznik`
--

DROP TABLE IF EXISTS `przewoznik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `przewoznik` (
  `id_przewoznika` bigint NOT NULL,
  `nazwa` varchar(255) DEFAULT NULL,
  `id_linii` bigint DEFAULT NULL,
  PRIMARY KEY (`id_przewoznika`),
  KEY `fk_przewoznik_linia` (`id_linii`),
  CONSTRAINT `fk_przewoznik_linia` FOREIGN KEY (`id_linii`) REFERENCES `linia_kolejowa` (`id_linii`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `przewoznik`
--

LOCK TABLES `przewoznik` WRITE;
/*!40000 ALTER TABLE `przewoznik` DISABLE KEYS */;
/*!40000 ALTER TABLE `przewoznik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stacja_kolejowa`
--

DROP TABLE IF EXISTS `stacja_kolejowa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stacja_kolejowa` (
  `id_stacji` bigint NOT NULL,
  `nazwa_stacji` varchar(255) DEFAULT NULL,
  `miasto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_stacji`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stacja_kolejowa`
--

LOCK TABLES `stacja_kolejowa` WRITE;
/*!40000 ALTER TABLE `stacja_kolejowa` DISABLE KEYS */;
/*!40000 ALTER TABLE `stacja_kolejowa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagon`
--

DROP TABLE IF EXISTS `wagon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wagon` (
  `id_wagonu` bigint NOT NULL,
  `liczba_miejsc` bigint DEFAULT NULL,
  PRIMARY KEY (`id_wagonu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagon`
--

LOCK TABLES `wagon` WRITE;
/*!40000 ALTER TABLE `wagon` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagon` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-07 21:21:34
