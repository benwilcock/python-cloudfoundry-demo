import sys
import connector

connection = connector.getDatabaseConnection()

def seedCarsDb():
    if connection is not None:

        try:
            print("Seeding the database.")
            cur = connection.cursor()
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
            connection.commit()
            print("Seeding complete.")
        except:

            if connection:
                connection.rollback()
                print("Seeding rolled back.")

            sys.exit(1)

    else:
        print("Connection empty!?")

if __name__ == '__main__':
    seedCarsDb()