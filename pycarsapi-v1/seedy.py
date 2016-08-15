import psycopg2
import sys
import os

db = os.getenv('DATABASE_URL', 'postgres://postgres:password@127.0.0.1:5432/postgres')
con = None
connected = False

if db is not None:
    try:
        con = psycopg2.connect(db)
        connected = True
        print("Connected: " + str(connected))
    except:
        connected = False
        print("Connected: " + str(connected))
        sys.exit(1)

def seedCarsDb():
    if con is not None:
        print(str(con))
        try:
            print("Creating.")
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
            print("Committed.")
        except:

            if con:
                con.rollback()
                print("Rollback.")

            sys.exit(1)

        finally:

            if con:
                con.close()
                print("Closed.")
    else:
        print("Connection empty!?")

if __name__ == '__main__':
    seedCarsDb()