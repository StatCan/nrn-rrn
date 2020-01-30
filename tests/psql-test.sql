-- Alter default postgres password.
ALTER ROLE postgres WITH PASSWORD 'password';
-- Create a test database.
CREATE DATABASE gisdb;
-- Connect to the test database.
\c gisdb;
-- Spatially enabled the test database.
CREATE EXTENSION postgis;

