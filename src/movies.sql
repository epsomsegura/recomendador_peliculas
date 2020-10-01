-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 30-09-2020 a las 00:38:54
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

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` text NOT NULL,
  `city` varchar(100) NOT NULL,
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

INSERT INTO `users` (`id`, `username`, `email`, `password`, `city`, `terms`, `created_at`, `updated_at`) VALUES
(1, 'test', 'test@test.com', '$2b$12$vgIrCT3jouChPjhOUtfkhOs3fFXwzItyOHLQVlmZEB2MtYuZcpLL.', 'Xalapa Ver', 1, '2020-09-24 17:25:15', NULL),
(2, 'test2', 'test2@test.com', '$2b$12$QcxBY5SZmvxypW7N8wD8Z.MtcaHnj1qDGrm4sohkXMpkCOq4Ua.k.', 'Xalapa Ver', 0, '2020-09-27 15:24:26', NULL);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
