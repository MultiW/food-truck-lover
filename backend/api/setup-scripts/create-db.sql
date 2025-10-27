-- Create postgres user
DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'postgres') THEN
      CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'postgres';
   END IF;
END
$$;

-- Create database
DROP DATABASE IF EXISTS food_truck_lover;
CREATE DATABASE food_truck_lover;