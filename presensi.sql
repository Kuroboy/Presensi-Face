-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 22 Sep 2022 pada 07.05
-- Versi server: 10.4.21-MariaDB
-- Versi PHP: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `presensi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `facebase`
--

CREATE TABLE `facebase` (
  `no` int(11) NOT NULL,
  `npm` varchar(8) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `kelas` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `facebase`
--

INSERT INTO `facebase` (`no`, `npm`, `nama`, `kelas`) VALUES
(1, '54419392', 'Muhammad Ridhwan', '3IA17'),
(2, '50419354', 'ahza rijas ', '3IA17');

-- --------------------------------------------------------

--
-- Struktur dari tabel `laporan`
--

CREATE TABLE `laporan` (
  `no` int(11) NOT NULL,
  `npm` varchar(8) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `tanggal` date NOT NULL,
  `hari` varchar(10) DEFAULT NULL,
  `jamMasuk` time NOT NULL,
  `jamKeluar` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `laporan`
--

INSERT INTO `laporan` (`no`, `npm`, `nama`, `tanggal`, `hari`, `jamMasuk`, `jamKeluar`) VALUES
(1, '54419392', 'Muhammad Ridhwan', '2022-09-04', 'Minggu', '19:36:32', '19:37:00'),
(2, '50419354', 'ahza rijas ', '2022-09-05', 'Senin', '11:16:13', '11:17:00'),
(3, '54419392', 'Muhammad Ridhwan', '2022-09-16', 'Jumat', '06:14:43', NULL),
(4, '54419392', 'Muhammad Ridhwan', '2022-09-22', 'Kamis', '11:33:04', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `passkey`
--

CREATE TABLE `passkey` (
  `no` int(11) NOT NULL,
  `pkey` int(8) NOT NULL,
  `nama` varchar(30) NOT NULL,
  `npm` varchar(8) NOT NULL,
  `kelas` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `passkey`
--

INSERT INTO `passkey` (`no`, `pkey`, `nama`, `npm`, `kelas`) VALUES
(1, 54419392, 'Muhammad Ridhwan', '54419392', '3IA17'),
(2, 50419354, 'ahza rijas ', '50419354', '3IA17');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `facebase`
--
ALTER TABLE `facebase`
  ADD PRIMARY KEY (`no`);

--
-- Indeks untuk tabel `laporan`
--
ALTER TABLE `laporan`
  ADD PRIMARY KEY (`no`);

--
-- Indeks untuk tabel `passkey`
--
ALTER TABLE `passkey`
  ADD PRIMARY KEY (`no`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `facebase`
--
ALTER TABLE `facebase`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `laporan`
--
ALTER TABLE `laporan`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `passkey`
--
ALTER TABLE `passkey`
  MODIFY `no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
