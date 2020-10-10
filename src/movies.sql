-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 10-10-2020 a las 18:14:55
-- Versión del servidor: 10.4.11-MariaDB
-- Versión de PHP: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `movies`
--
CREATE DATABASE IF NOT EXISTS `movies` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `movies`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genres`
--

DROP TABLE IF EXISTS `genres`;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL,
  `genre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Truncar tablas antes de insertar `genres`
--

TRUNCATE TABLE `genres`;
--
-- Volcado de datos para la tabla `genres`
--

INSERT INTO `genres` (`id`, `genre`) VALUES
(1, 'action'),
(3, 'animation'),
(4, 'aniplex'),
(5, 'brosta tv'),
(6, 'carousel productions'),
(7, 'comedy'),
(8, 'crime'),
(9, 'documentary'),
(10, 'drama'),
(11, 'family'),
(12, 'fantasy'),
(13, 'foreign'),
(14, 'gohands'),
(15, 'history'),
(16, 'horror'),
(17, 'mardock scramble production committee'),
(18, 'music'),
(19, 'mistery'),
(20, 'odyssey media'),
(21, 'pulser productions'),
(22, 'rogue state'),
(23, 'romance'),
(24, 'scinece fiction'),
(25, 'telescene film group productions'),
(26, 'sentai filmworks'),
(27, 'the cartel'),
(28, 'thriller'),
(29, 'tv movie'),
(30, 'vision view entertainment'),
(31, 'war'),
(32, 'western');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `username` varchar(250) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `terms` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Truncar tablas antes de insertar `users`
--

TRUNCATE TABLE `users`;
--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `email`, `password`, `terms`, `created_at`, `updated_at`) VALUES
(1, 'Tester 1', 'test1', 'test1@test.com', '$2b$12$HFbg0.q0wkfQ5dEWfARDEedN9iA3VwdKSE02aJ/efkbBpEzmn..NK', 0, '2020-10-10 10:54:51', NULL),
(2, 'Tester 2', 'test2', 'test2@test.com', '$2b$12$ky7CHLr2HanPxHsJPwZrT.i6BQXwIRN6CL/06Rj.sziRZ0KWRMPOy', 0, '2020-10-10 10:56:28', NULL),
(3, 'Tester 3', 'test3', 'test3@test.com', '$2b$12$bNF1hbYb0NWT2aOB4.YGceA/Jbl6O1eGKq9YA4yHqYSurwSk/qrEG', 0, '2020-10-10 10:58:44', NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `genres`
--
ALTER TABLE `genres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
