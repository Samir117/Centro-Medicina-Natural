-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 08, 2023 at 08:35 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `center_salud`
--

-- --------------------------------------------------------

--
-- Table structure for table `analisis_sentimiento`
--

CREATE TABLE `analisis_sentimiento` (
  `id_analisi` int(11) NOT NULL,
  `positivo` double NOT NULL,
  `negativo` double NOT NULL,
  `neutro` double NOT NULL,
  `compuesto` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
-- --------------------------------------------------------

--
-- Table structure for table `resumenes`
--

CREATE TABLE `resumenes` (
  `id_resumen` int(11) NOT NULL,
  `link` varchar(200) NOT NULL,
  `original` longtext NOT NULL,
  `traducido` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `res_chatbot`
--

CREATE TABLE `res_chatbot` (
  `id_respuesta` int(11) NOT NULL,
  `entrada` varchar(500) NOT NULL,
  `respuesta` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `analisis_sentimiento`
--
ALTER TABLE `analisis_sentimiento`
  ADD PRIMARY KEY (`id_analisi`);

--
-- Indexes for table `resumenes`
--
ALTER TABLE `resumenes`
  ADD PRIMARY KEY (`id_resumen`);

--
-- Indexes for table `res_chatbot`
--
ALTER TABLE `res_chatbot`
  ADD PRIMARY KEY (`id_respuesta`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `analisis_sentimiento`
--
ALTER TABLE `analisis_sentimiento`
  MODIFY `id_analisi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `resumenes`
--
ALTER TABLE `resumenes`
  MODIFY `id_resumen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `res_chatbot`
--
ALTER TABLE `res_chatbot`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
