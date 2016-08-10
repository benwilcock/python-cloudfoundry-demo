import psycopg2
import sys
import os

db = os.getenv('DATABASE_URL', None)
con = None
connected = False

if db is not None:
    try:
        con = psycopg2.connect(db)
        connected = True
    except:
        connected = False

def seedCarsDb():
    if con is not None:
        try:
            cur = con.cursor()
            cur.execute("DROP SCHEMA IF EXISTS demo CASCADE")
            cur.execute("CREATE SCHEMA demo")
            cur.execute("DROP TABLE IF EXISTS demo.cars CASCADE")
            cur.execute("CREATE TABLE demo.cars(Id INTEGER PRIMARY KEY, Name VARCHAR(20))")
            cur.execute("INSERT INTO demo.cars VALUES(1,'Audi')")
            cur.execute("INSERT INTO demo.cars VALUES(2,'Mercedes')")
            cur.execute("INSERT INTO demo.cars VALUES(3,'Skoda')")
            cur.execute("INSERT INTO demo.cars VALUES(4,'Volvo')")
            cur.execute("INSERT INTO demo.cars VALUES(5,'Bentley')")
            cur.execute("INSERT INTO demo.cars VALUES(6,'Citroen')")
            cur.execute("INSERT INTO demo.cars VALUES(7,'BMW')")
            cur.execute("INSERT INTO demo.cars VALUES(8,'Volkswagen')")
            con.commit()

        except:

            if con:
                con.rollback()

            sys.exit(1)

        finally:

            if con:
                con.close()