import unittest
from unittest.mock import patch
from datetime import datetime as dt
import sys
import os
from dotenv import load_dotenv
sys.path.append('../src')  # Add the 'src' directory to the system path
from main import Main  # Import the Main class from main.py

load_dotenv('../variables.env')

class test(unittest.TestCase):
    @patch('psycopg2.connect')
    def test_setup_database_initial_connection(self, mock_connect):
        db_config = {
            'dbname': 'postgres',  # Temporarily connect to the default database
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),
        }
        main = Main()
        main.setup_database()
        mock_connect.assert_any_call(**db_config)

    @patch('psycopg2.connect')
    def test_setup_database_final_connection(self, mock_connect):
        db_config = {
            'dbname': os.getenv('DB_NAME', 'postgres'),  # Temporarily connect to the default database
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),
        }
        main = Main()
        main.setup_database()
        mock_connect.assert_any_call(**db_config)

    @patch('psycopg2.connect')
    def test_send_event_to_database(self, mock_connect):
        # Arrange
        main = Main()
        timestamp = dt(2023, 7, 2, 21, 1, 22, 297810)
        temperature = '12.221'

        # Act
        main.send_event_to_database(timestamp, temperature)

        # Assert
        mock_connect.assert_called_with(
            dbname= os.getenv('DB_NAME', 'postgres'),
            user= os.getenv('DB_USER', 'postgres'),
            password= os.getenv('DB_PASSWORD'),
            host= os.getenv('DB_HOST', 'localhost')
        )

if __name__ == "__main__":
    unittest.main()