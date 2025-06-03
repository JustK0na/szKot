DROP DATABASE IF EXISTS szkot;
START TRANSACTION;

CREATE DATABASE IF NOT EXISTS szkot;
USE szkot;

-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: szkot
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
  `id_biletu` int NOT NULL AUTO_INCREMENT,
  `id_pasażera` int DEFAULT NULL,
  `id_połączenia` int DEFAULT NULL,
  `cena` decimal(10,2) DEFAULT NULL,
  `ulgi` enum('None','Student','Senior','Weteran','Dziecko') DEFAULT NULL,
  PRIMARY KEY (`id_biletu`),
  KEY `id_pasażera` (`id_pasażera`),
  KEY `id_połączenia` (`id_połączenia`),
  CONSTRAINT `bilety_ibfk_1` FOREIGN KEY (`id_pasażera`) REFERENCES `pasazerowie` (`id_pasażera`),
  CONSTRAINT `bilety_ibfk_2` FOREIGN KEY (`id_połączenia`) REFERENCES `polaczenia` (`id_połączenia`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilety`
--

LOCK TABLES `bilety` WRITE;
/*!40000 ALTER TABLE `bilety` DISABLE KEYS */;
INSERT INTO `bilety` VALUES (1,6420,100,156.00,'Dziecko'),(2,5826,26,234.00,'Senior'),(3,4360,71,300.00,'Senior'),(4,5286,63,284.00,'Student'),(5,8801,6,250.00,'Student'),(6,8974,91,246.00,'Senior'),(7,3328,85,53.00,'Senior'),(8,9911,79,88.00,'Dziecko'),(9,2443,54,266.00,'Dziecko'),(10,7004,81,293.00,'Weteran'),(11,1830,49,196.00,'Weteran'),(12,7441,16,127.00,'Dziecko'),(13,6626,60,202.00,'Weteran'),(14,5228,69,180.00,'None'),(15,4961,100,298.00,'Senior'),(16,97,57,294.00,'Student'),(17,3421,79,218.00,'Student'),(18,9357,86,162.00,'Dziecko'),(19,4753,38,272.00,'Senior'),(20,8262,43,197.00,'Senior'),(21,8288,16,218.00,'Dziecko'),(22,6581,66,223.00,'Student'),(23,7952,22,171.00,'Weteran'),(24,3924,88,166.00,'Dziecko'),(25,5915,55,294.00,'None'),(26,2023,78,245.00,'Senior'),(27,1998,4,237.00,'Dziecko'),(28,1963,89,273.00,'Dziecko'),(29,3803,64,259.00,'Student'),(30,1785,73,207.00,'None'),(31,9059,58,178.00,'Senior'),(32,3799,68,265.00,'None'),(33,3172,83,145.00,'Senior'),(34,7101,97,193.00,'Senior'),(35,5706,61,128.00,'Student'),(36,7840,10,275.00,'Senior'),(37,6598,7,261.00,'Senior'),(38,4838,15,158.00,'Weteran'),(39,8499,85,75.00,'Senior'),(40,9788,14,98.00,'Dziecko'),(41,883,95,133.00,'None'),(42,4275,8,286.00,'None'),(43,5745,2,272.00,'Dziecko'),(44,9999,14,123.00,'Weteran'),(45,7677,77,50.00,'Weteran'),(46,5387,62,108.00,'Weteran'),(47,8810,21,73.00,'Dziecko'),(48,3513,54,270.00,'None'),(49,4058,47,185.00,'Dziecko'),(50,3446,94,68.00,'Weteran'),(51,5024,13,293.00,'Weteran'),(52,2889,46,108.00,'Weteran'),(53,8572,99,106.00,'Senior'),(54,2012,4,229.00,'Student'),(55,1550,21,62.00,'Student'),(56,6325,52,283.00,'Weteran'),(57,7796,40,92.00,'Weteran'),(58,5890,36,247.00,'Weteran'),(59,4136,15,234.00,'Weteran'),(60,1766,6,258.00,'Student'),(61,823,13,189.00,'Weteran'),(62,587,23,133.00,'Student'),(63,3190,69,174.00,'None'),(64,4777,23,296.00,'None'),(65,7207,24,245.00,'Senior'),(66,4027,95,221.00,'None'),(67,9518,89,144.00,'Dziecko'),(68,346,22,96.00,'Senior'),(69,710,2,76.00,'None'),(70,6207,50,65.00,'Weteran'),(71,7286,89,252.00,'None'),(72,6842,57,186.00,'None'),(73,1829,64,168.00,'Senior'),(74,9027,90,174.00,'Weteran'),(75,8803,5,235.00,'Senior'),(76,5576,55,153.00,'None'),(77,3952,35,60.00,'Senior'),(78,8288,60,190.00,'Senior'),(79,5869,25,242.00,'Dziecko'),(80,9728,92,239.00,'Weteran'),(81,9749,53,267.00,'Senior'),(82,5437,46,64.00,'Weteran'),(83,4645,13,52.00,'Senior'),(84,7557,75,173.00,'Student'),(85,4062,71,178.00,'None'),(86,9513,64,144.00,'Weteran'),(87,4159,19,174.00,'Senior'),(88,7456,22,243.00,'Senior'),(89,6044,43,84.00,'Dziecko'),(90,3973,51,63.00,'Dziecko'),(91,3078,57,173.00,'Student'),(92,5041,4,128.00,'Weteran'),(93,9928,28,299.00,'Student'),(94,6655,8,193.00,'Senior'),(95,1292,48,214.00,'Student'),(96,7961,97,177.00,'Student'),(97,2241,42,128.00,'None'),(98,7693,74,132.00,'Weteran'),(99,6358,32,59.00,'Weteran'),(100,9266,53,194.00,'None'),(101,10002,79,81.00,'Student'),(102,10004,2,96.00,'Weteran'),(103,10001,18,179.00,'None'),(104,10005,5,82.00,'Weteran');
/*!40000 ALTER TABLE `bilety` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linie_kolejowe`
--

DROP TABLE IF EXISTS `linie_kolejowe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `linie_kolejowe` (
  `id_linii` int NOT NULL AUTO_INCREMENT,
  `nazwa_linii` varchar(100) DEFAULT NULL,
  `id_stacji` int DEFAULT NULL,
  `id_przewoznika` int DEFAULT NULL,
  PRIMARY KEY (`id_linii`),
  KEY `id_stacji` (`id_stacji`),
  KEY `id_przewoznika` (`id_przewoznika`),
  CONSTRAINT `linie_kolejowe_ibfk_1` FOREIGN KEY (`id_stacji`) REFERENCES `stacje_kolejowe` (`id_stacji`),
  CONSTRAINT `linie_kolejowe_ibfk_2` FOREIGN KEY (`id_przewoznika`) REFERENCES `przewoznicy` (`id_przewoznika`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linie_kolejowe`
--

LOCK TABLES `linie_kolejowe` WRITE;
/*!40000 ALTER TABLE `linie_kolejowe` DISABLE KEYS */;
INSERT INTO `linie_kolejowe` VALUES (1,'Linia Wejherowo',188,6),(2,'Linia Łowicz',127,7),(3,'Linia Pabianice',19,6),(4,'Linia Mikołów',165,1),(5,'Linia Jelenia Góra',45,8),(6,'Linia Zakopane',38,8),(7,'Linia Piotrków Trybunalski',23,9),(8,'Linia Nowy Sącz',187,1),(9,'Linia Nowy Sącz',187,6),(10,'Linia Kutno',134,8),(11,'Linia Wodzisław Śląski',178,8),(12,'Linia Elbląg',37,9),(13,'Linia Bytom',149,5),(14,'Linia Tarnowskie Góry',181,5),(15,'Linia Jasło',108,2),(16,'Linia Pszczyna',8,1),(17,'Linia Wodzisław Śląski',178,9),(18,'Linia Mysłowice',161,8),(19,'Linia Biłgoraj',61,8),(20,'Linia Sochaczew',96,9),(21,'Linia Tczew',138,4),(22,'Linia Suwałki',30,6),(23,'Linia Jastrzębie-Zdrój',95,5),(24,'Linia Ostrów Mazowiecka',81,1),(25,'Linia Mława',54,2),(26,'Linia Pruszków',55,4),(27,'Linia Kraśnik',142,3),(28,'Linia Tomaszów Mazowiecki',2,1),(29,'Linia Tarnowskie Góry',181,5),(30,'Linia Wodzisław Śląski',178,3),(31,'Linia Otwock',117,6),(32,'Linia Biłgoraj',61,2),(33,'Linia Augustów',186,4),(34,'Linia Bolesławiec',180,9),(35,'Linia Świdnik',59,9),(36,'Linia Chełm',46,1),(37,'Linia Jasło',108,7),(38,'Linia Kętrzyn',62,9),(39,'Linia Łódź',87,2),(40,'Linia Radom',22,6),(41,'Linia Śrem',168,4),(42,'Linia Nysa',192,7),(43,'Linia Stargard Szczeciński',52,9),(44,'Linia Biłgoraj',61,4),(45,'Linia Stargard Szczeciński',52,5),(46,'Linia Rybnik',151,2),(47,'Linia Swarzędz',153,4),(48,'Linia Sieradz',107,1),(49,'Linia Sopot',145,5),(50,'Linia Tychy',128,3),(51,'Linia Ostrów Mazowiecka',81,1),(52,'Linia Kluczbork',163,7),(53,'Linia Sandomierz',172,1),(54,'Linia Ciechanów',102,5),(55,'Linia Żyrardów',158,2),(56,'Linia Nowy Dwór Mazowiecki',126,7),(57,'Linia Świecie',90,7),(58,'Linia Ciechanów',102,5),(59,'Linia Żywiec',78,2),(60,'Linia Stargard Szczeciński',52,5),(61,'Linia Kwidzyn',63,3),(62,'Linia Brzeg',124,4),(63,'Linia Giżycko',154,9),(64,'Linia Czerwionka-Leszczyny',88,5),(65,'Linia Kołobrzeg',131,9),(66,'Linia Grodzisk Mazowiecki',3,2),(67,'Linia Pruszków',55,1),(68,'Linia Dębica',195,9),(69,'Linia Kościan',76,9),(70,'Linia Zamość',44,9),(71,'Linia Jastrzębie-Zdrój',95,5),(72,'Linia Łuków',49,8),(73,'Linia Szczecinek',24,5),(74,'Linia Bolesławiec',180,6),(75,'Linia Lubartów',68,1),(76,'Linia Szczecinek',24,4),(77,'Linia Płock',155,4),(78,'Linia Sieradz',107,5),(79,'Linia Sopot',145,4),(80,'Linia Wołomin',162,4),(81,'Linia Mysłowice',161,6),(82,'Linia Koło',140,7),(83,'Linia Turek',179,8),(84,'Linia Skarżysko-Kamienna',21,3),(85,'Linia Starogard Gdański',175,2),(86,'Linia Biłgoraj',61,3),(87,'Linia Pabianice',19,3),(88,'Linia Zakopane',38,7),(89,'Linia Białystok',6,1),(90,'Linia Skawina',89,1),(91,'Linia Wągrowiec',47,2),(92,'Linia Dzierżoniów',150,2),(93,'Linia Sanok',164,6),(94,'Linia Wołomin',162,4),(95,'Linia Wągrowiec',47,5),(96,'Linia Polkowice',129,2),(97,'Linia Płońsk',94,3),(98,'Linia Łuków',49,1),(99,'Linia Poznań',35,1),(100,'Linia Pruszcz Gdański',26,3),(101,'Linia Polkowice',129,1),(102,'Linia Żyrardów',158,8),(103,'Linia Włocławek',130,4),(104,'Linia Bielawa',66,7),(105,'Linia Sochaczew',96,6),(106,'Linia Bartoszyce',12,1),(107,'Linia Brodnica',1,8),(108,'Linia Olsztyn',120,7),(109,'Linia Żary',197,7),(110,'Linia Piotrków Trybunalski',23,7),(111,'Linia Piastów',27,8),(112,'Linia Chorzów',132,5),(113,'Linia Katowice',103,6),(114,'Linia Kętrzyn',62,8),(115,'Linia Ząbki',5,7),(116,'Linia Zawiercie',72,7),(117,'Linia Gdańsk',122,6),(118,'Linia Zielona Góra',71,3),(119,'Linia Kraków',16,8),(120,'Linia Biała Podlaska',41,8),(121,'Linia Gorzów Wielkopolski',98,8),(122,'Linia Iława',157,1),(123,'Linia Zambrów',166,4),(124,'Linia Stalowa Wola',93,9),(125,'Linia Tarnowskie Góry',181,3),(126,'Linia Nowa Ruda',113,4),(127,'Linia Stargard Szczeciński',52,4),(128,'Linia Jasło',108,6),(129,'Linia Rzeszów',43,9),(130,'Linia Puławy',4,3),(131,'Linia Pszczyna',8,6),(132,'Linia Białystok',6,2),(133,'Linia Bochnia',135,8),(134,'Linia Jaworzno',177,3),(135,'Linia Radom',22,5),(136,'Linia Mikołów',165,7),(137,'Linia Nowy Dwór Mazowiecki',126,5),(138,'Linia Chorzów',132,7),(139,'Linia Stargard Szczeciński',52,5),(140,'Linia Bełchatów',15,2),(141,'Linia Łaziska Górne',9,1),(142,'Linia Marki',167,4),(143,'Linia Jawor',79,6),(144,'Linia Rybnik',151,1),(145,'Linia Włocławek',130,6),(146,'Linia Piaseczno',123,7),(147,'Linia Zamość',44,1),(148,'Linia Konin',77,3),(149,'Linia Kielce',173,5),(150,'Linia Wałcz',69,4),(151,'Linia Zielona Góra',71,7),(152,'Linia Nowa Ruda',113,7),(153,'Linia Nowy Targ',137,8),(154,'Linia Zabrze',7,3),(155,'Linia Piotrków Trybunalski',23,1),(156,'Linia Nysa',192,8),(157,'Linia Łuków',49,2),(158,'Linia Koło',140,2),(159,'Linia Kościerzyna',73,5),(160,'Linia Sandomierz',172,2),(161,'Linia Bytom',149,9),(162,'Linia Sanok',164,5),(163,'Linia Chełm',46,9),(164,'Linia Piotrków Trybunalski',23,2),(165,'Linia Oława',112,9),(166,'Linia Zamość',44,7),(167,'Linia Będzin',170,9),(168,'Linia Wejherowo',188,9),(169,'Linia Chełm',46,4),(170,'Linia Chorzów',132,5),(171,'Linia Piła',97,6),(172,'Linia Jastrzębie-Zdrój',95,6),(173,'Linia Piekary Śląskie',100,3),(174,'Linia Siemianowice Śląskie',53,4),(175,'Linia Nowy Sącz',187,7),(176,'Linia Świdnica',121,3),(177,'Linia Świdnica',121,8),(178,'Linia Mysłowice',161,8),(179,'Linia Płońsk',94,1),(180,'Linia Brodnica',1,5),(181,'Linia Czechowice-Dziedzice',34,2),(182,'Linia Suwałki',30,6),(183,'Linia Jarosław',101,6),(184,'Linia Żagań',118,4),(185,'Linia Piastów',27,1),(186,'Linia Luboń',189,4),(187,'Linia Tarnobrzeg',191,5),(188,'Linia Kraków',16,6),(189,'Linia Wałbrzych',32,4),(190,'Linia Sopot',145,3),(191,'Linia Słupsk',25,8),(192,'Linia Czeladź',82,2),(193,'Linia Opole',42,9),(194,'Linia Ostrowiec Świętokrzyski',33,1),(195,'Linia Mława',54,6),(196,'Linia Nysa',192,9),(197,'Linia Lubartów',68,5),(198,'Linia Jarocin',65,9),(199,'Linia Jaworzno',177,5),(200,'Linia Białystok',6,6);
/*!40000 ALTER TABLE `linie_kolejowe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pasazerowie`
--

DROP TABLE IF EXISTS `pasazerowie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasazerowie` (
  `id_pasażera` int NOT NULL AUTO_INCREMENT,
  `imie` varchar(100) DEFAULT NULL,
  `nazwisko` varchar(100) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `telefon` varchar(20) DEFAULT NULL,
  `haslo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_pasażera`),
  UNIQUE KEY `mail` (`mail`)
) ENGINE=InnoDB AUTO_INCREMENT=10007 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasazerowie`
--

LOCK TABLES `pasazerowie` WRITE;
/*!40000 ALTER TABLE `pasazerowie` DISABLE KEYS */;

/*!40000 ALTER TABLE `pasazerowie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pociagi`
--

DROP TABLE IF EXISTS `pociagi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pociagi` (
  `id_pociągu` int NOT NULL AUTO_INCREMENT,
  `model_pociągu` varchar(100) DEFAULT NULL,
  `id_przewoźnika` int DEFAULT NULL,
  `id_aktualna_stacja` int DEFAULT NULL,
  `stan` varchar(50) DEFAULT NULL,
  `id_wagonu` int DEFAULT NULL,
  PRIMARY KEY (`id_pociągu`),
  KEY `id_przewoźnika` (`id_przewoźnika`),
  KEY `id_aktualna_stacja` (`id_aktualna_stacja`),
  KEY `id_wagonu` (`id_wagonu`),
  CONSTRAINT `pociagi_ibfk_1` FOREIGN KEY (`id_przewoźnika`) REFERENCES `przewoznicy` (`id_przewoznika`),
  CONSTRAINT `pociagi_ibfk_2` FOREIGN KEY (`id_aktualna_stacja`) REFERENCES `stacje_kolejowe` (`id_stacji`),
  CONSTRAINT `pociagi_ibfk_3` FOREIGN KEY (`id_wagonu`) REFERENCES `wagony` (`id_wagonu`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pociagi`
--

LOCK TABLES `pociagi` WRITE;
/*!40000 ALTER TABLE `pociagi` DISABLE KEYS */;
INSERT INTO `pociagi` VALUES (1,'Flirt',3,34,'Operational',1),(2,'Desiro',4,127,'Operational',2),(3,'Flirt',8,97,'Operational',3),(4,'IC NGT',8,140,'Operational',4),(5,'Pendolino',1,33,'Operational',5),(6,'Pendolino',6,132,'Operational',6),(7,'Desiro',5,87,'Operational',7),(8,'IC NGT',4,87,'Operational',8),(9,'IC NGT',8,64,'Operational',9),(10,'EIP',1,38,'Operational',10),(11,'EIP',7,174,'Operational',11),(12,'Intercity',4,121,'Operational',12),(13,'Pesa Elf',6,41,'Operational',13),(14,'IC NGT',2,114,'Operational',14),(15,'Pesa Elf',2,106,'Operational',15),(16,'Pesa Elf',2,37,'Operational',16),(17,'Flirt',6,83,'Operational',17),(18,'Pendolino',5,166,'Operational',18),(19,'Flirt',2,28,'Operational',19),(20,'Intercity',8,142,'Operational',20),(21,'IC NGT',5,174,'Operational',21),(22,'Flirt',9,80,'Operational',22),(23,'Pendolino',4,74,'Operational',23),(24,'IC NGT',1,74,'Operational',24),(25,'Desiro',8,15,'Operational',25),(26,'Pendolino',1,75,'Operational',26),(27,'EIP',8,82,'Operational',27),(28,'Pesa Elf',9,65,'Operational',28),(29,'Flirt',4,59,'Operational',29),(30,'Intercity',5,19,'Operational',30),(31,'Pesa Elf',1,67,'Operational',31),(32,'IC NGT',6,44,'Operational',32),(33,'Desiro',1,152,'Operational',33),(34,'EIP',4,108,'Operational',34),(35,'Pendolino',9,191,'Operational',35),(36,'Flirt',5,68,'Operational',36),(37,'IC NGT',1,21,'Operational',37),(38,'Intercity',5,69,'Operational',38),(39,'EIP',5,184,'Operational',39),(40,'Flirt',2,191,'Operational',40),(41,'Desiro',8,82,'Operational',41),(42,'Desiro',6,142,'Operational',42),(43,'EIP',4,165,'Operational',43),(44,'Flirt',1,116,'Operational',44),(45,'EIP',1,135,'Operational',45),(46,'IC NGT',2,57,'Operational',46),(47,'Desiro',1,153,'Operational',47),(48,'Intercity',6,111,'Operational',48),(49,'Flirt',9,9,'Operational',49),(50,'Pendolino',8,91,'Operational',50);
/*!40000 ALTER TABLE `pociagi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `polaczenia`
--

DROP TABLE IF EXISTS `polaczenia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `polaczenia` (
  `id_połączenia` int NOT NULL AUTO_INCREMENT,
  `id_lini` int DEFAULT NULL,
  `id_stacji_początkowej` int DEFAULT NULL,
  `id_stacji_końcowej` int DEFAULT NULL,
  `id_pociągu` int DEFAULT NULL,
  `czas_przejazdu` time DEFAULT NULL,
  `data` date DEFAULT NULL,
  `opóźnienie` time DEFAULT NULL,
  PRIMARY KEY (`id_połączenia`),
  KEY `id_lini` (`id_lini`),
  KEY `id_stacji_początkowej` (`id_stacji_początkowej`),
  KEY `id_stacji_końcowej` (`id_stacji_końcowej`),
  KEY `id_pociągu` (`id_pociągu`),
  CONSTRAINT `polaczenia_ibfk_1` FOREIGN KEY (`id_lini`) REFERENCES `linie_kolejowe` (`id_linii`),
  CONSTRAINT `polaczenia_ibfk_2` FOREIGN KEY (`id_stacji_początkowej`) REFERENCES `stacje_kolejowe` (`id_stacji`),
  CONSTRAINT `polaczenia_ibfk_3` FOREIGN KEY (`id_stacji_końcowej`) REFERENCES `stacje_kolejowe` (`id_stacji`),
  CONSTRAINT `polaczenia_ibfk_4` FOREIGN KEY (`id_pociągu`) REFERENCES `pociagi` (`id_pociągu`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polaczenia`
--

LOCK TABLES `polaczenia` WRITE;
/*!40000 ALTER TABLE `polaczenia` DISABLE KEYS */;
INSERT INTO `polaczenia` VALUES (1,119,16,78,27,'01:42:59','2025-03-09','00:29:28'),(2,25,54,157,16,'01:55:52','2025-01-06','00:30:14'),(3,160,172,143,14,'00:00:20','2025-11-03','02:17:33'),(4,11,178,57,20,'01:50:56','2025-07-24','01:37:24'),(5,119,16,167,20,'01:31:00','2025-01-20','02:01:49'),(6,33,186,150,8,'04:17:16','2025-04-14','00:23:03'),(7,114,62,53,3,'03:57:01','2025-04-07','02:28:30'),(8,136,165,148,11,'01:21:14','2025-09-05','00:50:52'),(9,190,145,118,1,'02:06:25','2025-06-23','02:12:43'),(10,103,130,68,43,'02:21:01','2025-06-16','02:20:22'),(11,139,52,186,36,'01:03:55','2025-10-14','02:27:24'),(12,9,187,127,17,'02:15:08','2025-06-19','01:53:58'),(13,66,3,95,40,'04:54:28','2025-09-07','01:57:13'),(14,15,108,126,14,'00:09:12','2025-05-18','01:39:37'),(15,193,42,158,49,'01:02:24','2025-03-12','00:32:50'),(16,30,178,9,1,'01:14:04','2025-07-04','00:53:28'),(17,19,61,83,41,'05:40:36','2025-10-04','02:58:20'),(18,123,166,35,34,'05:59:53','2025-02-15','02:07:47'),(19,21,138,190,23,'00:25:24','2025-04-01','01:59:10'),(20,81,161,104,13,'01:00:42','2025-02-15','02:21:02'),(21,191,25,22,41,'00:58:46','2025-03-05','00:38:18'),(22,40,22,68,6,'02:48:29','2025-05-28','00:32:19'),(23,33,186,171,8,'03:51:00','2025-08-18','00:10:03'),(24,174,53,87,23,'02:20:41','2025-11-27','00:27:34'),(25,196,192,149,28,'05:28:04','2025-05-19','02:25:09'),(26,113,103,59,13,'00:29:12','2025-09-03','02:55:26'),(27,61,63,135,1,'03:01:25','2025-03-16','02:20:02'),(28,49,145,180,21,'01:53:54','2025-08-10','01:27:21'),(29,39,87,116,40,'05:34:40','2025-10-09','00:20:57'),(30,189,32,48,43,'05:48:54','2025-06-10','02:10:23'),(31,162,164,167,39,'00:47:58','2025-09-20','02:07:27'),(32,150,69,194,29,'00:28:46','2025-03-24','02:13:02'),(33,108,120,189,11,'02:10:38','2025-09-27','01:17:19'),(34,142,167,64,43,'01:13:29','2025-06-12','02:04:14'),(35,117,122,123,32,'03:28:19','2025-04-27','02:29:03'),(36,41,168,118,2,'01:40:56','2025-02-23','01:37:30'),(37,191,25,127,20,'03:47:40','2025-04-26','02:29:03'),(38,57,90,48,11,'01:12:30','2025-06-17','02:35:48'),(39,47,153,59,23,'05:15:55','2025-01-10','02:30:02'),(40,22,30,94,32,'01:28:36','2025-12-19','00:57:45'),(41,60,52,35,30,'01:21:10','2025-04-27','01:16:56'),(42,150,69,125,8,'04:18:54','2025-05-16','00:34:48'),(43,97,94,122,1,'02:25:43','2025-08-05','01:31:19'),(44,195,54,167,17,'01:09:14','2025-04-19','01:18:47'),(45,93,164,71,17,'02:12:37','2025-09-19','02:23:15'),(46,6,38,131,41,'05:37:54','2025-07-01','00:51:21'),(47,8,187,47,24,'02:13:22','2025-04-21','01:33:29'),(48,70,44,174,35,'02:15:29','2025-10-07','02:27:28'),(49,190,145,162,1,'03:00:17','2025-05-26','02:12:34'),(50,102,158,37,50,'03:05:41','2025-08-12','02:55:59'),(51,70,44,167,49,'04:26:10','2025-06-23','01:35:49'),(52,76,24,171,8,'00:27:20','2025-07-04','00:24:24'),(53,130,4,129,1,'02:18:29','2025-05-16','00:27:47'),(54,100,26,193,1,'02:34:12','2025-05-09','02:07:49'),(55,88,38,85,11,'02:54:23','2025-02-28','00:14:12'),(56,120,41,76,4,'01:55:55','2025-02-10','01:41:14'),(57,195,54,183,42,'01:01:40','2025-08-15','00:24:20'),(58,161,149,21,49,'01:16:28','2025-08-11','01:03:37'),(59,67,55,98,44,'04:24:01','2025-06-10','00:50:37'),(60,196,192,51,35,'01:50:37','2025-03-16','02:34:27'),(61,34,180,190,22,'05:01:09','2025-06-01','00:29:57'),(62,83,179,144,3,'03:24:53','2025-02-25','02:41:49'),(63,19,61,79,3,'01:34:32','2025-07-25','02:18:57'),(64,172,95,65,13,'03:46:27','2025-05-14','01:22:54'),(65,47,153,154,8,'02:23:10','2025-03-23','00:59:46'),(66,192,82,44,46,'01:48:16','2025-06-02','01:50:19'),(67,108,120,175,11,'01:09:24','2025-06-24','02:52:42'),(68,125,181,39,1,'05:25:14','2025-10-01','00:12:30'),(69,71,95,128,18,'03:53:56','2025-11-02','02:06:12'),(70,63,154,123,35,'01:30:36','2025-11-03','00:45:16'),(71,65,131,97,49,'00:13:33','2025-04-25','01:27:57'),(72,49,145,43,18,'04:41:49','2025-06-05','02:47:50'),(73,117,122,170,42,'03:17:49','2025-08-12','02:12:51'),(74,120,41,182,41,'02:49:52','2025-10-20','01:02:44'),(75,179,94,151,47,'03:59:18','2025-11-08','01:02:39'),(76,61,63,29,1,'00:32:49','2025-01-28','00:56:09'),(77,144,151,132,31,'02:56:35','2025-06-13','01:39:59'),(78,171,97,45,6,'00:57:03','2025-02-14','02:08:05'),(79,44,61,18,43,'00:02:58','2025-02-15','02:46:54'),(80,6,38,57,3,'03:39:28','2025-01-27','00:45:40'),(81,145,130,192,32,'04:02:01','2025-09-08','02:09:57'),(82,61,63,77,1,'03:01:11','2025-09-02','01:08:24'),(83,193,42,62,49,'05:26:52','2025-04-05','02:30:41'),(84,121,98,69,41,'03:00:41','2025-10-07','02:54:35'),(85,89,6,52,47,'02:27:34','2025-05-24','01:01:01'),(86,100,26,16,1,'05:40:29','2025-06-13','02:46:08'),(87,173,100,85,1,'05:38:54','2025-10-23','01:14:00'),(88,10,134,175,9,'02:53:12','2025-05-14','01:56:09'),(89,37,108,2,11,'00:45:23','2025-08-28','02:43:01'),(90,101,129,181,47,'02:51:38','2025-07-18','01:17:04'),(91,101,129,133,10,'01:22:06','2025-07-10','01:01:21'),(92,48,107,162,10,'05:03:58','2025-09-26','02:06:40'),(93,101,129,71,45,'05:08:58','2025-03-15','00:59:16'),(94,149,173,48,38,'04:31:59','2025-05-19','02:35:46'),(95,154,7,143,1,'03:31:59','2025-02-25','00:25:36'),(96,114,62,74,41,'03:38:21','2025-03-21','02:44:01'),(97,37,108,140,11,'02:23:15','2025-05-17','02:56:30'),(98,162,164,122,18,'03:18:31','2025-12-14','00:52:54'),(99,61,63,45,1,'01:58:12','2025-07-11','00:45:48'),(100,143,79,10,48,'01:31:40','2025-12-09','00:15:25');
/*!40000 ALTER TABLE `polaczenia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `przewoznicy`
--

DROP TABLE IF EXISTS `przewoznicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `przewoznicy` (
  `id_przewoznika` int NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_przewoznika`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `przewoznicy`
--

LOCK TABLES `przewoznicy` WRITE;
/*!40000 ALTER TABLE `przewoznicy` DISABLE KEYS */;
INSERT INTO `przewoznicy` VALUES (1,'PKP Intercity'),(2,'Arriva'),(3,'Koleje Mazowieckie'),(4,'Koleje Śląskie'),(5,'Łódzka Kolej Aglomeracyjna'),(6,'Przewozy Regionalne'),(7,'Warszawska Kolej Dojazdowa'),(8,'Koleje Wielkopolskie'),(9,'Koleje Dolnośląskie');
/*!40000 ALTER TABLE `przewoznicy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stacje_kolejowe`
--

DROP TABLE IF EXISTS `stacje_kolejowe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stacje_kolejowe` (
  `id_stacji` int NOT NULL AUTO_INCREMENT,
  `nazwa_stacji` varchar(100) DEFAULT NULL,
  `miasto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_stacji`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stacje_kolejowe`
--

LOCK TABLES `stacje_kolejowe` WRITE;
/*!40000 ALTER TABLE `stacje_kolejowe` DISABLE KEYS */;
INSERT INTO `stacje_kolejowe` VALUES (1,'Brodnica Główny','Brodnica'),(2,'Tomaszów Mazowiecki Główny','Tomaszów Mazowiecki'),(3,'Grodzisk Mazowiecki Główny','Grodzisk Mazowiecki'),(4,'Puławy Główny','Puławy'),(5,'Ząbki Główny','Ząbki'),(6,'Białystok Główny','Białystok'),(7,'Zabrze Główny','Zabrze'),(8,'Pszczyna Główny','Pszczyna'),(9,'Łaziska Górne Główny','Łaziska Górne'),(10,'Rumia Główny','Rumia'),(11,'Szczecin Główny','Szczecin'),(12,'Bartoszyce Główny','Bartoszyce'),(13,'Racibórz Główny','Racibórz'),(14,'Środa Wielkopolska Główny','Środa Wielkopolska'),(15,'Bełchatów Główny','Bełchatów'),(16,'Kraków Główny','Kraków'),(17,'Malbork Główny','Malbork'),(18,'Warszawa Główny','Warszawa'),(19,'Pabianice Główny','Pabianice'),(20,'Mińsk Mazowiecki Główny','Mińsk Mazowiecki'),(21,'Skarżysko-Kamienna Główny','Skarżysko-Kamienna'),(22,'Radom Główny','Radom'),(23,'Piotrków Trybunalski Główny','Piotrków Trybunalski'),(24,'Szczecinek Główny','Szczecinek'),(25,'Słupsk Główny','Słupsk'),(26,'Pruszcz Gdański Główny','Pruszcz Gdański'),(27,'Piastów Główny','Piastów'),(28,'Kłodzko Główny','Kłodzko'),(29,'Białogard Główny','Białogard'),(30,'Suwałki Główny','Suwałki'),(31,'Świebodzice Główny','Świebodzice'),(32,'Wałbrzych Główny','Wałbrzych'),(33,'Ostrowiec Świętokrzyski Główny','Ostrowiec Świętokrzyski'),(34,'Czechowice-Dziedzice Główny','Czechowice-Dziedzice'),(35,'Poznań Główny','Poznań'),(36,'Gliwice Główny','Gliwice'),(37,'Elbląg Główny','Elbląg'),(38,'Zakopane Główny','Zakopane'),(39,'Głogów Główny','Głogów'),(40,'Lubliniec Główny','Lubliniec'),(41,'Biała Podlaska Główny','Biała Podlaska'),(42,'Opole Główny','Opole'),(43,'Rzeszów Główny','Rzeszów'),(44,'Zamość Główny','Zamość'),(45,'Jelenia Góra Główny','Jelenia Góra'),(46,'Chełm Główny','Chełm'),(47,'Wągrowiec Główny','Wągrowiec'),(48,'Chojnice Główny','Chojnice'),(49,'Łuków Główny','Łuków'),(50,'Sosnowiec Główny','Sosnowiec'),(51,'Ruda Śląska Główny','Ruda Śląska'),(52,'Stargard Szczeciński Główny','Stargard Szczeciński'),(53,'Siemianowice Śląskie Główny','Siemianowice Śląskie'),(54,'Mława Główny','Mława'),(55,'Pruszków Główny','Pruszków'),(56,'Ostrołęka Główny','Ostrołęka'),(57,'Bydgoszcz Główny','Bydgoszcz'),(58,'Ostróda Główny','Ostróda'),(59,'Świdnik Główny','Świdnik'),(60,'Świnoujście Główny','Świnoujście'),(61,'Biłgoraj Główny','Biłgoraj'),(62,'Kętrzyn Główny','Kętrzyn'),(63,'Kwidzyn Główny','Kwidzyn'),(64,'Zgierz Główny','Zgierz'),(65,'Jarocin Główny','Jarocin'),(66,'Bielawa Główny','Bielawa'),(67,'Zduńska Wola Główny','Zduńska Wola'),(68,'Lubartów Główny','Lubartów'),(69,'Wałcz Główny','Wałcz'),(70,'Wyszków Główny','Wyszków'),(71,'Zielona Góra Główny','Zielona Góra'),(72,'Zawiercie Główny','Zawiercie'),(73,'Kościerzyna Główny','Kościerzyna'),(74,'Radomsko Główny','Radomsko'),(75,'Reda Główny','Reda'),(76,'Kościan Główny','Kościan'),(77,'Konin Główny','Konin'),(78,'Żywiec Główny','Żywiec'),(79,'Jawor Główny','Jawor'),(80,'Leszno Główny','Leszno'),(81,'Ostrów Mazowiecka Główny','Ostrów Mazowiecka'),(82,'Czeladź Główny','Czeladź'),(83,'Ostrów Wielkopolski Główny','Ostrów Wielkopolski'),(84,'Inowrocław Główny','Inowrocław'),(85,'Częstochowa Główny','Częstochowa'),(86,'Myszków Główny','Myszków'),(87,'Łódź Główny','Łódź'),(88,'Czerwionka-Leszczyny Główny','Czerwionka-Leszczyny'),(89,'Skawina Główny','Skawina'),(90,'Świecie Główny','Świecie'),(91,'Września Główny','Września'),(92,'Grudziądz Główny','Grudziądz'),(93,'Stalowa Wola Główny','Stalowa Wola'),(94,'Płońsk Główny','Płońsk'),(95,'Jastrzębie-Zdrój Główny','Jastrzębie-Zdrój'),(96,'Sochaczew Główny','Sochaczew'),(97,'Piła Główny','Piła'),(98,'Gorzów Wielkopolski Główny','Gorzów Wielkopolski'),(99,'Skierniewice Główny','Skierniewice'),(100,'Piekary Śląskie Główny','Piekary Śląskie'),(101,'Jarosław Główny','Jarosław'),(102,'Ciechanów Główny','Ciechanów'),(103,'Katowice Główny','Katowice'),(104,'Chrzanów Główny','Chrzanów'),(105,'Olkusz Główny','Olkusz'),(106,'Bielsk Podlaski Główny','Bielsk Podlaski'),(107,'Sieradz Główny','Sieradz'),(108,'Jasło Główny','Jasło'),(109,'Knurów Główny','Knurów'),(110,'Zgorzelec Główny','Zgorzelec'),(111,'Ełk Główny','Ełk'),(112,'Oława Główny','Oława'),(113,'Nowa Ruda Główny','Nowa Ruda'),(114,'Kędzierzyn-Koźle Główny','Kędzierzyn-Koźle'),(115,'Lubin Główny','Lubin'),(116,'Wieluń Główny','Wieluń'),(117,'Otwock Główny','Otwock'),(118,'Żagań Główny','Żagań'),(119,'Krosno Główny','Krosno'),(120,'Olsztyn Główny','Olsztyn'),(121,'Świdnica Główny','Świdnica'),(122,'Gdańsk Główny','Gdańsk'),(123,'Piaseczno Główny','Piaseczno'),(124,'Brzeg Główny','Brzeg'),(125,'Starachowice Główny','Starachowice'),(126,'Nowy Dwór Mazowiecki Główny','Nowy Dwór Mazowiecki'),(127,'Łowicz Główny','Łowicz'),(128,'Tychy Główny','Tychy'),(129,'Polkowice Główny','Polkowice'),(130,'Włocławek Główny','Włocławek'),(131,'Kołobrzeg Główny','Kołobrzeg'),(132,'Chorzów Główny','Chorzów'),(133,'Bielsko-Biała Główny','Bielsko-Biała'),(134,'Kutno Główny','Kutno'),(135,'Bochnia Główny','Bochnia'),(136,'Łomża Główny','Łomża'),(137,'Nowy Targ Główny','Nowy Targ'),(138,'Tczew Główny','Tczew'),(139,'Przemyśl Główny','Przemyśl'),(140,'Koło Główny','Koło'),(141,'Gniezno Główny','Gniezno'),(142,'Kraśnik Główny','Kraśnik'),(143,'Szczytno Główny','Szczytno'),(144,'Toruń Główny','Toruń'),(145,'Sopot Główny','Sopot'),(146,'Siedlce Główny','Siedlce'),(147,'Tarnów Główny','Tarnów'),(148,'Gorlice Główny','Gorlice'),(149,'Bytom Główny','Bytom'),(150,'Dzierżoniów Główny','Dzierżoniów'),(151,'Rybnik Główny','Rybnik'),(152,'Oświęcim Główny','Oświęcim'),(153,'Swarzędz Główny','Swarzędz'),(154,'Giżycko Główny','Giżycko'),(155,'Płock Główny','Płock'),(156,'Świętochłowice Główny','Świętochłowice'),(157,'Iława Główny','Iława'),(158,'Żyrardów Główny','Żyrardów'),(159,'Mielec Główny','Mielec'),(160,'Kalisz Główny','Kalisz'),(161,'Mysłowice Główny','Mysłowice'),(162,'Wołomin Główny','Wołomin'),(163,'Kluczbork Główny','Kluczbork'),(164,'Sanok Główny','Sanok'),(165,'Mikołów Główny','Mikołów'),(166,'Zambrów Główny','Zambrów'),(167,'Marki Główny','Marki'),(168,'Śrem Główny','Śrem'),(169,'Krotoszyn Główny','Krotoszyn'),(170,'Będzin Główny','Będzin'),(171,'Police Główny','Police'),(172,'Sandomierz Główny','Sandomierz'),(173,'Kielce Główny','Kielce'),(174,'Lublin Główny','Lublin'),(175,'Starogard Gdański Główny','Starogard Gdański'),(176,'Legnica Główny','Legnica'),(177,'Jaworzno Główny','Jaworzno'),(178,'Wodzisław Śląski Główny','Wodzisław Śląski'),(179,'Turek Główny','Turek'),(180,'Bolesławiec Główny','Bolesławiec'),(181,'Tarnowskie Góry Główny','Tarnowskie Góry'),(182,'Nowa Sól Główny','Nowa Sól'),(183,'Gdynia Główny','Gdynia'),(184,'Dąbrowa Górnicza Główny','Dąbrowa Górnicza'),(185,'Cieszyn Główny','Cieszyn'),(186,'Augustów Główny','Augustów'),(187,'Nowy Sącz Główny','Nowy Sącz'),(188,'Wejherowo Główny','Wejherowo'),(189,'Luboń Główny','Luboń'),(190,'Żory Główny','Żory'),(191,'Tarnobrzeg Główny','Tarnobrzeg'),(192,'Nysa Główny','Nysa'),(193,'Lębork Główny','Lębork'),(194,'Wrocław Główny','Wrocław'),(195,'Dębica Główny','Dębica'),(196,'Koszalin Główny','Koszalin'),(197,'Żary Główny','Żary'),(198,'Goleniów Główny','Goleniów');
/*!40000 ALTER TABLE `stacje_kolejowe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wagony`
--

DROP TABLE IF EXISTS `wagony`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wagony` (
  `id_wagonu` int NOT NULL AUTO_INCREMENT,
  `liczba_miejsc` int DEFAULT NULL,
  PRIMARY KEY (`id_wagonu`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagony`
--

LOCK TABLES `wagony` WRITE;
/*!40000 ALTER TABLE `wagony` DISABLE KEYS */;
INSERT INTO `wagony` VALUES (1,70),(2,100),(3,30),(4,50),(5,30),(6,30),(7,70),(8,30),(9,50),(10,100),(11,100),(12,70),(13,70),(14,100),(15,50),(16,50),(17,70),(18,30),(19,100),(20,100),(21,100),(22,50),(23,30),(24,70),(25,100),(26,30),(27,100),(28,50),(29,100),(30,100),(31,30),(32,70),(33,50),(34,30),(35,100),(36,50),(37,30),(38,70),(39,100),(40,30),(41,50),(42,30),(43,50),(44,70),(45,50),(46,100),(47,70),(48,30),(49,50),(50,70),(51,30),(52,30),(53,30),(54,30),(55,70),(56,100),(57,30),(58,70),(59,30),(60,100),(61,70),(62,70),(63,30),(64,100),(65,30),(66,30),(67,30),(68,50),(69,100),(70,70),(71,30),(72,30),(73,70),(74,30),(75,50),(76,70),(77,100),(78,100),(79,50),(80,70),(81,30),(82,70),(83,50),(84,30),(85,30),(86,30),(87,70),(88,30),(89,100),(90,100),(91,70),(92,30),(93,70),(94,50),(95,100),(96,30),(97,30),(98,70),(99,100),(100,70);
/*!40000 ALTER TABLE `wagony` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-02 16:47:38
