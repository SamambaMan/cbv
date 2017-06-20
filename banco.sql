-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: 13.66.34.46    Database: cbvprd
-- ------------------------------------------------------
-- Server version	5.6.34

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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `account_emailaddress_user_id_2c513194_fk_auth_user_id` (`user_id`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=342 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_bannercensodovolei`
--

DROP TABLE IF EXISTS `sitecbv_bannercensodovolei`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_bannercensodovolei` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(100) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Subtitulo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_bannerconteudoexclusivo`
--

DROP TABLE IF EXISTS `sitecbv_bannerconteudoexclusivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_bannerconteudoexclusivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Subtitulo` varchar(100) DEFAULT NULL,
  `Ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_bannerexperiencia`
--

DROP TABLE IF EXISTS `sitecbv_bannerexperiencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_bannerexperiencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Subtitulo` varchar(100) DEFAULT NULL,
  `Ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_bannerrededesconto`
--

DROP TABLE IF EXISTS `sitecbv_bannerrededesconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_bannerrededesconto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(100) NOT NULL,
  `Imagem` varchar(100) DEFAULT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Subtitulo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_categoriacensodovolei`
--

DROP TABLE IF EXISTS `sitecbv_categoriacensodovolei`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_categoriacensodovolei` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `slug` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_categoriaconteudoexclusivo`
--

DROP TABLE IF EXISTS `sitecbv_categoriaconteudoexclusivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_categoriaconteudoexclusivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `slug` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_categoriaexperiencia`
--

DROP TABLE IF EXISTS `sitecbv_categoriaexperiencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_categoriaexperiencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `slug` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_categoriaredededesconto`
--

DROP TABLE IF EXISTS `sitecbv_categoriaredededesconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_categoriaredededesconto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(50) NOT NULL,
  `slug` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_censodovolei`
--

DROP TABLE IF EXISTS `sitecbv_censodovolei`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_censodovolei` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Detalhe` varchar(140) DEFAULT NULL,
  `Thumb` varchar(100) DEFAULT NULL,
  `Topo` varchar(100) DEFAULT NULL,
  `Conteudo` longtext,
  `DataPublicacao` date DEFAULT NULL,
  `Publicar` tinyint(1) NOT NULL,
  `ImagemCarrossel` varchar(100) DEFAULT NULL,
  `Link` varchar(1000) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Categoria_id` int(11) NOT NULL,
  `Subtitulo` varchar(140) DEFAULT NULL,
  `Destaque` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sitecbv_censodovolei_Categoria_id_3ec6ffae_fk_sitecbv_c` (`Categoria_id`),
  CONSTRAINT `sitecbv_censodovolei_Categoria_id_3ec6ffae_fk_sitecbv_c` FOREIGN KEY (`Categoria_id`) REFERENCES `sitecbv_categoriacensodovolei` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_conteudoexclusivo`
--

DROP TABLE IF EXISTS `sitecbv_conteudoexclusivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_conteudoexclusivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Detalhe` varchar(140) DEFAULT NULL,
  `Thumb` varchar(100) DEFAULT NULL,
  `Topo` varchar(100) DEFAULT NULL,
  `Conteudo` longtext,
  `DataPublicacao` date DEFAULT NULL,
  `Publicar` tinyint(1) NOT NULL,
  `Destaque` tinyint(1) NOT NULL,
  `ImagemCarrossel` varchar(100) DEFAULT NULL,
  `Categoria_id` int(11) NOT NULL,
  `Subtitulo` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sitecbv_conteudoexcl_Categoria_id_9569e154_fk_sitecbv_c` (`Categoria_id`),
  CONSTRAINT `sitecbv_conteudoexcl_Categoria_id_9569e154_fk_sitecbv_c` FOREIGN KEY (`Categoria_id`) REFERENCES `sitecbv_categoriaconteudoexclusivo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_experiencia`
--

DROP TABLE IF EXISTS `sitecbv_experiencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_experiencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Detalhe` varchar(140) DEFAULT NULL,
  `Thumb` varchar(100) DEFAULT NULL,
  `Topo` varchar(100) DEFAULT NULL,
  `Conteudo` longtext,
  `DataPublicacao` date DEFAULT NULL,
  `Publicar` tinyint(1) NOT NULL,
  `ImagemCarrossel` varchar(100) DEFAULT NULL,
  `Destaque` tinyint(1) NOT NULL,
  `Link` varchar(1000) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Categoria_id` int(11) NOT NULL,
  `Subtitulo` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sitecbv_experiencia_Categoria_id_dd378527_fk_sitecbv_c` (`Categoria_id`),
  CONSTRAINT `sitecbv_experiencia_Categoria_id_dd378527_fk_sitecbv_c` FOREIGN KEY (`Categoria_id`) REFERENCES `sitecbv_categoriaexperiencia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_infosadicionaisusuario`
--

DROP TABLE IF EXISTS `sitecbv_infosadicionaisusuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_infosadicionaisusuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cadastrocompleto` tinyint(1) NOT NULL,
  `cpf` varchar(11) DEFAULT NULL,
  `tipodocumento` varchar(3) NOT NULL,
  `ufed` varchar(50) DEFAULT NULL,
  `sexo` varchar(1) DEFAULT NULL,
  `celular` varchar(15) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `cep` varchar(9) DEFAULT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  `numero` varchar(15) DEFAULT NULL,
  `complemento` varchar(100) DEFAULT NULL,
  `bairro` varchar(100) DEFAULT NULL,
  `cidade` varchar(100) DEFAULT NULL,
  `pais` varchar(100) DEFAULT NULL,
  `modalidade_favorita` varchar(2) NOT NULL,
  `jogador_favorito_id` int(11) DEFAULT NULL,
  `jogadora_favorita_id` int(11) DEFAULT NULL,
  `time_favorito_feminino_id` int(11) DEFAULT NULL,
  `time_favorito_masculino_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `nascimento` date DEFAULT NULL,
  `receberinformacoesprograma` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `sitecbv_infosadicion_jogador_favorito_id_06de196c_fk_sitecbv_j` (`jogador_favorito_id`),
  KEY `sitecbv_infosadicion_jogadora_favorita_id_b62e546f_fk_sitecbv_j` (`jogadora_favorita_id`),
  KEY `sitecbv_infosadicion_time_favorito_femini_52539069_fk_sitecbv_t` (`time_favorito_feminino_id`),
  KEY `sitecbv_infosadicion_time_favorito_mascul_3416679e_fk_sitecbv_t` (`time_favorito_masculino_id`),
  CONSTRAINT `sitecbv_infosadicion_jogador_favorito_id_06de196c_fk_sitecbv_j` FOREIGN KEY (`jogador_favorito_id`) REFERENCES `sitecbv_jogador` (`id`),
  CONSTRAINT `sitecbv_infosadicion_jogadora_favorita_id_b62e546f_fk_sitecbv_j` FOREIGN KEY (`jogadora_favorita_id`) REFERENCES `sitecbv_jogador` (`id`),
  CONSTRAINT `sitecbv_infosadicion_time_favorito_femini_52539069_fk_sitecbv_t` FOREIGN KEY (`time_favorito_feminino_id`) REFERENCES `sitecbv_time` (`id`),
  CONSTRAINT `sitecbv_infosadicion_time_favorito_mascul_3416679e_fk_sitecbv_t` FOREIGN KEY (`time_favorito_masculino_id`) REFERENCES `sitecbv_time` (`id`),
  CONSTRAINT `sitecbv_infosadicionaisusuario_user_id_f2a0e72b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_infosadicionaisusuario_jogadoras_secundarias_femininas`
--

DROP TABLE IF EXISTS `sitecbv_infosadicionaisusuario_jogadoras_secundarias_femininas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_infosadicionaisusuario_jogadoras_secundarias_femininas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `infosadicionaisusuario_id` int(11) NOT NULL,
  `jogador_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sitecbv_infosadicionaisu_infosadicionaisusuario_i_eb7e464b_uniq` (`infosadicionaisusuario_id`,`jogador_id`),
  KEY `sitecbv_infosadicion_jogador_id_c86adcaa_fk_sitecbv_j` (`jogador_id`),
  CONSTRAINT `sitecbv_infosadicion_infosadicionaisusuar_9e24a53a_fk_sitecbv_i` FOREIGN KEY (`infosadicionaisusuario_id`) REFERENCES `sitecbv_infosadicionaisusuario` (`id`),
  CONSTRAINT `sitecbv_infosadicion_jogador_id_c86adcaa_fk_sitecbv_j` FOREIGN KEY (`jogador_id`) REFERENCES `sitecbv_jogador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_infosadicionaisusuario_jogadores_secundario_masculinos`
--

DROP TABLE IF EXISTS `sitecbv_infosadicionaisusuario_jogadores_secundario_masculinos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_infosadicionaisusuario_jogadores_secundario_masculinos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `infosadicionaisusuario_id` int(11) NOT NULL,
  `jogador_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sitecbv_infosadicionaisu_infosadicionaisusuario_i_7b240c4f_uniq` (`infosadicionaisusuario_id`,`jogador_id`),
  KEY `sitecbv_infosadicion_jogador_id_da3ba504_fk_sitecbv_j` (`jogador_id`),
  CONSTRAINT `sitecbv_infosadicion_infosadicionaisusuar_a7708dd7_fk_sitecbv_i` FOREIGN KEY (`infosadicionaisusuario_id`) REFERENCES `sitecbv_infosadicionaisusuario` (`id`),
  CONSTRAINT `sitecbv_infosadicion_jogador_id_da3ba504_fk_sitecbv_j` FOREIGN KEY (`jogador_id`) REFERENCES `sitecbv_jogador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_infosadicionaisusuario_times_secundarios_feminino`
--

DROP TABLE IF EXISTS `sitecbv_infosadicionaisusuario_times_secundarios_feminino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_infosadicionaisusuario_times_secundarios_feminino` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `infosadicionaisusuario_id` int(11) NOT NULL,
  `time_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sitecbv_infosadicionaisu_infosadicionaisusuario_i_51c8e5c8_uniq` (`infosadicionaisusuario_id`,`time_id`),
  KEY `sitecbv_infosadicion_time_id_33bae331_fk_sitecbv_t` (`time_id`),
  CONSTRAINT `sitecbv_infosadicion_infosadicionaisusuar_1f162437_fk_sitecbv_i` FOREIGN KEY (`infosadicionaisusuario_id`) REFERENCES `sitecbv_infosadicionaisusuario` (`id`),
  CONSTRAINT `sitecbv_infosadicion_time_id_33bae331_fk_sitecbv_t` FOREIGN KEY (`time_id`) REFERENCES `sitecbv_time` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_infosadicionaisusuario_times_secundarios_masculino`
--

DROP TABLE IF EXISTS `sitecbv_infosadicionaisusuario_times_secundarios_masculino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_infosadicionaisusuario_times_secundarios_masculino` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `infosadicionaisusuario_id` int(11) NOT NULL,
  `time_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sitecbv_infosadicionaisu_infosadicionaisusuario_i_0c40738f_uniq` (`infosadicionaisusuario_id`,`time_id`),
  KEY `sitecbv_infosadicion_time_id_dbe024e1_fk_sitecbv_t` (`time_id`),
  CONSTRAINT `sitecbv_infosadicion_infosadicionaisusuar_0d383601_fk_sitecbv_i` FOREIGN KEY (`infosadicionaisusuario_id`) REFERENCES `sitecbv_infosadicionaisusuario` (`id`),
  CONSTRAINT `sitecbv_infosadicion_time_id_dbe024e1_fk_sitecbv_t` FOREIGN KEY (`time_id`) REFERENCES `sitecbv_time` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_jogador`
--

DROP TABLE IF EXISTS `sitecbv_jogador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_jogador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(35) NOT NULL,
  `Sexo` varchar(1) NOT NULL,
  `Foto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_programa`
--

DROP TABLE IF EXISTS `sitecbv_programa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_programa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Topo` varchar(100) NOT NULL,
  `Conteudo` longtext,
  `Publicar` tinyint(1) NOT NULL,
  `Subtitulo` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_redededesconto`
--

DROP TABLE IF EXISTS `sitecbv_redededesconto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_redededesconto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Titulo` varchar(50) NOT NULL,
  `Detalhe` varchar(140) DEFAULT NULL,
  `Thumb` varchar(100) DEFAULT NULL,
  `Topo` varchar(100) DEFAULT NULL,
  `Conteudo` longtext,
  `DataPublicacao` date DEFAULT NULL,
  `Publicar` tinyint(1) NOT NULL,
  `ImagemCarrossel` varchar(100) DEFAULT NULL,
  `Link` varchar(1000) NOT NULL,
  `Ativo` tinyint(1) NOT NULL,
  `Categoria_id` int(11) NOT NULL,
  `Subtitulo` varchar(140) DEFAULT NULL,
  `Selo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sitecbv_redededescon_Categoria_id_1df540cb_fk_sitecbv_c` (`Categoria_id`),
  CONSTRAINT `sitecbv_redededescon_Categoria_id_1df540cb_fk_sitecbv_c` FOREIGN KEY (`Categoria_id`) REFERENCES `sitecbv_categoriaredededesconto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sitecbv_time`
--

DROP TABLE IF EXISTS `sitecbv_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sitecbv_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Nome` varchar(35) NOT NULL,
  `Logo` varchar(100) NOT NULL,
  `Sexo` varchar(1) NOT NULL,
  `Superliga` varchar(2) NOT NULL,
  `Link` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-20  1:28:05
