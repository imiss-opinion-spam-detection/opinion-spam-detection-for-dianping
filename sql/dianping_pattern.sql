-- phpMyAdmin SQL Dump
-- version phpStudy 2014
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016 年 07 月 26 日 18:22
-- 服务器版本: 5.6.28-ndb-7.4.10-cluster-gpl
-- PHP 版本: 5.3.29

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `dianping`
--
CREATE DATABASE `dianping` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `dianping`;

-- --------------------------------------------------------

--
-- 表的结构 `dianpingcontent`
--

CREATE TABLE IF NOT EXISTS `dianpingcontent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nameid` varchar(255) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `contribution` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `userinforank` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `review` text CHARACTER SET utf8 NOT NULL,
  `time` varchar(255) CHARACTER SET utf8 NOT NULL,
  `shop` varchar(255) CHARACTER SET utf8 NOT NULL,
  `cost` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `rst1` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `rst2` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `rst3` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
