--
-- PostgreSQL database dump
--

\restrict cMoXs2uLbA2z2RdSor0R1rbvXRSsmaLa98Xlbdbrj9EEcg9E58muY8aUvpHsTdr

-- Dumped from database version 16.14
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: t; Type: TABLE; Schema: public; Owner: leaderboard
--

CREATE TABLE public.t (
    x integer
);


ALTER TABLE public.t OWNER TO leaderboard;

--
-- Data for Name: t; Type: TABLE DATA; Schema: public; Owner: leaderboard
--

COPY public.t (x) FROM stdin;
42
\.


--
-- PostgreSQL database dump complete
--

\unrestrict cMoXs2uLbA2z2RdSor0R1rbvXRSsmaLa98Xlbdbrj9EEcg9E58muY8aUvpHsTdr

