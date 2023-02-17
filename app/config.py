import os
from dotenv import load_dotenv


load_dotenv()



TOKEN = os.getenv('TOKEN')


HOST=os.getenv('HOST')
DB_NAME=os.getenv('DB_NAME')
PASSWORD=os.getenv('PASSWORD')
USER=os.getenv('USER')