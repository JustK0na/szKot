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
  PRIMARY KEY (`id_pociągu`),
  KEY `id_przewoźnika` (`id_przewoźnika`),
  KEY `id_aktualna_stacja` (`id_aktualna_stacja`),
  CONSTRAINT `pociagi_ibfk_1` FOREIGN KEY (`id_przewoźnika`) REFERENCES `przewoznicy` (`id_przewoznika`),
  CONSTRAINT `pociagi_ibfk_2` FOREIGN KEY (`id_aktualna_stacja`) REFERENCES `stacje_kolejowe` (`id_stacji`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pociagi`
--

--
-- Table structure for table `polaczenia`
--

DROP TABLE IF EXISTS `polaczenia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;

CREATE TABLE polaczenia (
  id_połączenia int NOT NULL AUTO_INCREMENT,
  id_lini int DEFAULT NULL,
  id_stacji_początkowej int DEFAULT NULL,
  id_stacji_końcowej int DEFAULT NULL,
  id_pociągu int DEFAULT NULL,
  czas_przejazdu time DEFAULT NULL,
  godzina_odjazdu time DEFAULT NULL,
  dni_tygodnia SET('Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela') DEFAULT NULL,
  PRIMARY KEY (id_połączenia),
  KEY id_lini (id_lini),
  KEY id_stacji_początkowej (id_stacji_początkowej),
  KEY id_stacji_końcowej (id_stacji_końcowej),
  KEY id_pociągu (id_pociągu),
  CONSTRAINT polaczenia_ibfk_1 FOREIGN KEY (id_lini) REFERENCES linie_kolejowe (id_linii),
  CONSTRAINT polaczenia_ibfk_2 FOREIGN KEY (id_stacji_początkowej) REFERENCES stacje_kolejowe (id_stacji),
  CONSTRAINT polaczenia_ibfk_3 FOREIGN KEY (id_stacji_końcowej) REFERENCES stacje_kolejowe (id_stacji),
  CONSTRAINT polaczenia_ibfk_4 FOREIGN KEY (id_pociągu) REFERENCES pociagi (id_pociągu)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;





--
-- Table structure for table `wagony`
--

DROP TABLE IF EXISTS `wagony`;
CREATE TABLE `wagony` (
  `id_wagonu` INT NOT NULL AUTO_INCREMENT,
  `id_pociągu` INT DEFAULT NULL,
  `liczba_miejsc` INT DEFAULT NULL,
  PRIMARY KEY (`id_wagonu`),
  KEY `id_pociągu` (`id_pociągu`),
  CONSTRAINT `wagony_ibfk_1` FOREIGN KEY (`id_pociągu`) REFERENCES `pociagi` (`id_pociągu`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-02 16:47:38
