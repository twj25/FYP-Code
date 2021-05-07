import os
import sqlite3

def db_connect():
    con = sqlite3.connect('C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/db.sqlite3')
    return con

def delete_all_places():
    con = db_connect()
    sql = 'DELETE FROM places'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return

def create_place(con, name):
    sql = """
        INSERT INTO places (place)
        VALUES (?)"""
    cur = con.cursor()
    cur.execute(sql, [name])
    return cur.lastrowid

def places_load(places_list):
    con = db_connect()
    for place in places_list:
        try:
            place_id = create_place(con,place)
            con.commit()
        except:
            con.rollback()
            raise RuntimeError("An error has occured")
    con.close()
    return

def create_sample(con, place_id, year, frequency, link):
    sql = """
        INSERT INTO samples (place_id, year, frequency, link)
        VALUES (?,?,?,?)"""
    cur = con.cursor()
    cur.execute(sql, (place_id,year,frequency,link))
    return cur.lastrowid

def samples_load(samples_list, place_id):
    con = db_connect()
    for sample in samples_list:
        if type(sample) is int:
            year = sample
        else:
            frequency = sample[0]
            link = sample[1]
            try:
                sample_id = create_sample(con,place_id,year,frequency,link)
                con.commit()
            except:
                con.rollback()
                raise RuntimeError("An error has occured")
    con.close()
    return

def delete_all_samples():
    con = db_connect()
    sql = 'DELETE FROM samples'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return

def return_all_samples():
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT id,link FROM samples")

    rows = cur.fetchall()
    return rows

def create_data(con, sample_id, date, link):
    sql = """
        INSERT INTO data (sample_id, date, link)
        VALUES (?,?,?)"""
    cur = con.cursor()
    cur.execute(sql, (sample_id, date, link))
    return cur.lastrowid

def data_load(data_list, sample_id):
    con = db_connect()
    for data in data_list:
        date = str(data[0]) + '/' + str(data[1])
        link = data[2]
        try:
            data_id = create_data(con,sample_id,date,link)
            con.commit()
        except:
            con.rollback()
            raise RuntimeError("An error has occured")
    con.close()
    return

def delete_all_data():
    con = db_connect()
    sql = 'DELETE FROM data'
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return

def return_all_data():
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT id,link FROM data")
    
    rows = cur.fetchall()
    return rows