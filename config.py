import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Set the DATABASE_URL from environment variable or use the default value
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://admin:admin@db:3306/drs_baza")

# Set the SECRET_KEY from environment variable or use the default value
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")