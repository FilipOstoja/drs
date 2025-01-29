from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pymysql
import os 

# Zamijeni ovo s vlastitim podacima
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://root:admin@localhost/drs_restapi")

# Za instalaciju pymysql kao MySQLdb
pymysql.install_as_MySQLdb()

def test_db_connection():
    try:
        # Kreiraj SQLAlchemy engine za konekciju s bazom
        engine = create_engine(DATABASE_URL)
        # Pokušaj povezivanje
        connection = engine.connect()
        connection.close()  # Zatvori konekciju
        return "Connection successful"
    except OperationalError as e:
        return f"Connection failed: {str(e)}"

if __name__ == "__main__":
    # Pokreni test
    print(test_db_connection())
