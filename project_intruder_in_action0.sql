-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: project
-- ------------------------------------------------------
-- Server version	5.7.21-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `intruder_in_action`
--

DROP TABLE IF EXISTS `intruder_in_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `intruder_in_action` (
  `intruder_id` int(11) DEFAULT NULL,
  `camera_id` int(11) DEFAULT NULL,
  `video_id` int(11) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `start_frame` int(11) DEFAULT NULL,
  `end_frame` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `common_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `intruder_id` (`intruder_id`),
  KEY `camera_id` (`camera_id`),
  KEY `video_id` (`video_id`),
  CONSTRAINT `intruder_in_action_ibfk_1` FOREIGN KEY (`intruder_id`) REFERENCES `intruder_data` (`id`),
  CONSTRAINT `intruder_in_action_ibfk_2` FOREIGN KEY (`camera_id`) REFERENCES `camera_data` (`id`),
  CONSTRAINT `intruder_in_action_ibfk_3` FOREIGN KEY (`video_id`) REFERENCES `video_clips` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=835 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intruder_in_action`
--

LOCK TABLES `intruder_in_action` WRITE;
/*!40000 ALTER TABLE `intruder_in_action` DISABLE KEYS */;
INSERT INTO `intruder_in_action` VALUES (1428,1,112,'2018-02-02 01:52:51','2018-02-02 01:53:03',2026,2328,833,NULL),(1429,1,113,'2018-02-02 01:53:04','2018-02-02 01:53:20',2352,2754,834,NULL);
/*!40000 ALTER TABLE `intruder_in_action` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-10 23:15:52
