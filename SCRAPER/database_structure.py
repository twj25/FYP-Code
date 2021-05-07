from database_helper import db_connect

con = db_connect()
cur = con.cursor()
places_sq1 = """
CREATE TABLE places (
    id integer PRIMARY KEY,
    place text NOT NULL)"""
cur.execute(places_sq1)

samples_sq1 = """
CREATE TABLE samples (
    id integer PRIMARY KEY,
    place_id text NOT NULL,
    year integer NOT NULL,
    frequency integer NOT NULL,
    link text NOT NULL,
    FOREIGN KEY (place_id) REFERENCES places (id))"""
cur.execute(samples_sq1)

data_sq1 = """
CREATE TABLE data (
    id integer PRIMARY KEY,
    sample_id text NOT NULL,
    date date NOT NULL,
    link text NOT NULL,
    FOREIGN KEY (sample_id) REFERENCES samples (id))"""
cur.execute(data_sq1)
