DROP DATABASE IF EXISTS szkot;
START TRANSACTION;

CREATE DATABASE  IF NOT EXISTS `szkot` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `szkot`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: szkot
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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `haslo` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'root','4813494d137e1631');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bilety`
--

DROP TABLE IF EXISTS `bilety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bilety` (
  `id_biletu` int NOT NULL AUTO_INCREMENT,
  `id_pasażera` int DEFAULT NULL,
  `id_przejazdu` int NOT NULL,
  `cena` decimal(10,2) DEFAULT NULL,
  `ulgi` enum('None','Student','Senior','Weteran','Dziecko') DEFAULT NULL,
  PRIMARY KEY (`id_biletu`),
  KEY `id_pasażera` (`id_pasażera`),
  KEY `fk_bilety_przejazdy` (`id_przejazdu`),
  CONSTRAINT `bilety_ibfk_1` FOREIGN KEY (`id_pasażera`) REFERENCES `pasazerowie` (`id_pasażera`) ON DELETE CASCADE,
  CONSTRAINT `fk_bilety_przejazdy` FOREIGN KEY (`id_przejazdu`) REFERENCES `przejazdy` (`id_przejazdu`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilety`
--

LOCK TABLES `bilety` WRITE;
/*!40000 ALTER TABLE `bilety` DISABLE KEYS */;
/*!40000 ALTER TABLE `bilety` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modele_pociagow`
--

DROP TABLE IF EXISTS `modele_pociagow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modele_pociagow` (
  `id_modelu` int NOT NULL AUTO_INCREMENT,
  `nazwa_modelu` varchar(100) NOT NULL,
  PRIMARY KEY (`id_modelu`),
  UNIQUE KEY `nazwa_modelu` (`nazwa_modelu`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modele_pociagow`
--

LOCK TABLES `modele_pociagow` WRITE;
/*!40000 ALTER TABLE `modele_pociagow` DISABLE KEYS */;
INSERT INTO `modele_pociagow` VALUES (13,'Bizon'),(15,'Dragon'),(6,'ED161'),(3,'EN57'),(4,'EN71'),(5,'EN75'),(2,'EU44 - Lokomotywa Tauron'),(11,'FLIRT'),(7,'HCP 303E'),(10,'IC 150'),(12,'Impuls 45WE'),(1,'Pendolino ED250'),(14,'Pesa Dart'),(9,'SA109'),(8,'SA137');
/*!40000 ALTER TABLE `modele_pociagow` ENABLE KEYS */;
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
  `id_przewoźnika` int DEFAULT NULL,
  `id_aktualna_stacja` int DEFAULT NULL,
  `stan` enum('operacyjny','konserwacja','uszkodzony','nieużytkowy') NOT NULL DEFAULT 'operacyjny',
  `id_modelu` int NOT NULL,
  PRIMARY KEY (`id_pociągu`),
  KEY `id_przewoźnika` (`id_przewoźnika`),
  KEY `id_aktualna_stacja` (`id_aktualna_stacja`),
  KEY `fk_pociagi_modele` (`id_modelu`),
  CONSTRAINT `fk_pociagi_modele` FOREIGN KEY (`id_modelu`) REFERENCES `modele_pociagow` (`id_modelu`),
  CONSTRAINT `pociagi_ibfk_1` FOREIGN KEY (`id_przewoźnika`) REFERENCES `przewoznicy` (`id_przewoznika`) ON DELETE CASCADE,
  CONSTRAINT `pociagi_ibfk_2` FOREIGN KEY (`id_aktualna_stacja`) REFERENCES `stacje_kolejowe` (`id_stacji`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pociagi`
--

LOCK TABLES `pociagi` WRITE;
/*!40000 ALTER TABLE `pociagi` DISABLE KEYS */;
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
  `id_stacji_początkowej` int DEFAULT NULL,
  `id_stacji_końcowej` int DEFAULT NULL,
  `id_pociągu` int DEFAULT NULL,
  `czas_przejazdu` time DEFAULT NULL,
  `godzina_odjazdu` time DEFAULT NULL,
  `dni_tygodnia` set('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') DEFAULT NULL,
  PRIMARY KEY (`id_połączenia`),
  KEY `id_stacji_początkowej` (`id_stacji_początkowej`),
  KEY `id_stacji_końcowej` (`id_stacji_końcowej`),
  KEY `id_pociągu` (`id_pociągu`),
  CONSTRAINT `polaczenia_ibfk_2` FOREIGN KEY (`id_stacji_początkowej`) REFERENCES `stacje_kolejowe` (`id_stacji`) ON DELETE CASCADE,
  CONSTRAINT `polaczenia_ibfk_3` FOREIGN KEY (`id_stacji_końcowej`) REFERENCES `stacje_kolejowe` (`id_stacji`) ON DELETE CASCADE,
  CONSTRAINT `polaczenia_ibfk_4` FOREIGN KEY (`id_pociągu`) REFERENCES `pociagi` (`id_pociągu`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polaczenia`
--

LOCK TABLES `polaczenia` WRITE;
/*!40000 ALTER TABLE `polaczenia` DISABLE KEYS */;
/*!40000 ALTER TABLE `polaczenia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `przejazdy`
--

DROP TABLE IF EXISTS `przejazdy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `przejazdy` (
  `id_przejazdu` int NOT NULL AUTO_INCREMENT,
  `id_połączenia` int NOT NULL,
  `data_przejazdu` date NOT NULL,
  `stan` enum('Zaplanowany','W trakcie','Zakończony','Opóźniony','Anulowany') DEFAULT 'Zaplanowany',
  `opoznienie_minuty` int DEFAULT NULL,
  PRIMARY KEY (`id_przejazdu`),
  KEY `id_połączenia` (`id_połączenia`),
  CONSTRAINT `przejazdy_ibfk_1` FOREIGN KEY (`id_połączenia`) REFERENCES `polaczenia` (`id_połączenia`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `przejazdy`
--

LOCK TABLES `przejazdy` WRITE;
/*!40000 ALTER TABLE `przejazdy` DISABLE KEYS */;
/*!40000 ALTER TABLE `przejazdy` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `sprawdz_dzien_przejazdu` BEFORE INSERT ON `przejazdy` FOR EACH ROW BEGIN
  -- to jest cos mega dziwnego z chatem i indianami na youtubie wykminilem ze mozna sprawdzac by bylo dobrze czy data jest odpowiednia podczas insertowania
  DECLARE dzien_en VARCHAR(20);
  DECLARE dni_polaczenia SET('Poniedziałek','Wtorek','Środa','Czwartek','Piątek','Sobota','Niedziela');

  SET dzien_en = DAYNAME(NEW.data_przejazdu);

  SELECT dni_tygodnia INTO dni_polaczenia
  FROM polaczenia
  WHERE id_połączenia = NEW.id_połączenia;

  -- warunek by pozwolilo na inserta
  IF FIND_IN_SET(dzien_en, dni_polaczenia) = 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Data przejazdu nie pasuje do dni tygodnia połączenia';
  END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `przewoznicy`
--

DROP TABLE IF EXISTS `przewoznicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `przewoznicy` (
  `id_przewoznika` int NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(100) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `haslo` varchar(255) NOT NULL,
  PRIMARY KEY (`id_przewoznika`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `przewoznicy`
--

LOCK TABLES `przewoznicy` WRITE;
/*!40000 ALTER TABLE `przewoznicy` DISABLE KEYS */;
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
  `id_pociągu` int DEFAULT NULL,
  `liczba_miejsc` int DEFAULT NULL,
  PRIMARY KEY (`id_wagonu`),
  KEY `id_pociągu` (`id_pociągu`),
  CONSTRAINT `wagony_ibfk_1` FOREIGN KEY (`id_pociągu`) REFERENCES `pociagi` (`id_pociągu`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wagony`
--

LOCK TABLES `wagony` WRITE;
/*!40000 ALTER TABLE `wagony` DISABLE KEYS */;
/*!40000 ALTER TABLE `wagony` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'szkot'
--


--
-- Dumping routines for database 'szkot'
--


DROP USER IF EXISTS 'admin_user'@'%';
DROP USER IF EXISTS 'przewoznik_user'@'%';
DROP USER IF EXISTS 'pasazer_user'@'%';
DROP USER IF EXISTS 'auth_user'@'%';



CREATE USER IF NOT EXISTS 'admin_user'@'%' IDENTIFIED BY 'admin_pass';
GRANT ALL PRIVILEGES ON szkot.* TO 'admin_user'@'%';

CREATE USER IF NOT EXISTS 'przewoznik_user'@'%' IDENTIFIED BY 'przewoznik_pass';
GRANT SELECT, INSERT, UPDATE ON szkot.* TO 'przewoznik_user'@'%';

CREATE USER IF NOT EXISTS 'pasazer_user'@'%' IDENTIFIED BY 'pasazer_pass';
GRANT SELECT ON szkot.stacje_kolejowe TO 'pasazer_user'@'%';
GRANT SELECT ON szkot.polaczenia TO 'pasazer_user'@'%';
GRANT SELECT ON szkot.pociagi TO 'pasazer_user'@'%';
GRANT SELECT ON szkot.przewoznicy TO 'pasazer_user'@'%';
GRANT SELECT ON szkot.bilety TO 'pasazer_user'@'%';
GRANT INSERT ON szkot.bilety TO 'pasazer_user'@'%';


CREATE USER IF NOT EXISTS 'auth_user'@'%' IDENTIFIED BY 'auth_pass';
GRANT SELECT,INSERT ON szkot.pasazerowie TO 'auth_user'@'%';
GRANT SELECT ON szkot.admins TO 'auth_user'@'%';
GRANT SELECT ON szkot.przewoznicy TO 'auth_user'@'%';




/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-13  0:21:11
