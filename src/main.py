from signalrcore.hub_connection_builder import HubConnectionBuilder
import datetime
import logging
import requests
import json
import time
import os
import psycopg2

class Main:
    def __init__(self):
        self._hub_connection = None
        self.HOST = os.getenv('HOST', 'http://34.95.34.5')  # Setup your host here
        self.TOKEN = os.getenv('TOKEN', '6f8162Qkd2')  # Setup your token here
        self.TICKETS = os.getenv('TICKETS', '10')  # Setup your tickets here
        self.T_MAX = os.getenv('T_MAX', '50')  # Setup your max temperature here
        self.T_MIN = os.getenv('T_MIN', '30')  # Setup your min temperature here
        self.DATABASE = os.getenv('database_name', 'oxygencsgrp2eq5')  # Setup your database here

        if self.TOKEN is None:
            raise ValueError("TOKEN environment variable is not set")

    def setup_database(self):
        db_config = {
            'dbname': 'postgres',  # Temporarily connect to the default database
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'root'),
            'host': os.getenv('DB_HOST', 'localhost'),
        }
        connection = psycopg2.connect(**db_config)
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        dbname = os.getenv('DB_NAME', 'oxygencsgrp2eq5')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {dbname}")

        connection.close()  # Close the temporary connection

        # Now connect to the new database
        db_config['dbname'] = dbname
        new_connection = psycopg2.connect(**db_config)
        cursor = new_connection.cursor()

        create_table_query = "CREATE TABLE IF NOT EXISTS sensordatas (timestamp TIMESTAMP PRIMARY KEY, temperature FLOAT)"

        cursor.execute(create_table_query)
        new_connection.commit()
        return new_connection
    
    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def setup(self):
        self.setSensorHub()

    def start(self):
        self.setup()
        self._hub_connection.start()

        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setSensorHub(self):
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )

        self._hub_connection.on("ReceiveSensorData", self.onSensorDataReceived)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(lambda data: print(f"||| An exception was thrown closed: {data.error}"))

    def onSensorDataReceived(self, data):
        try:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            date = data[0]["date"]
            converted_date = datetime.datetime.strptime(date[:25], date_format)
            datapoint = float(data[0]["data"])
            # self.send_temperature_to_fastapi(date, dp)
            self.send_event_to_database(converted_date, datapoint)
            self.analyzeDatapoint(date, datapoint)
        except Exception as err:
            print(err)

    def analyzeDatapoint(self, date, data):
        if float(data) >= float(self.T_MAX):
            self.sendActionToHvac(date, "TurnOnAc", self.TICKETS)
        elif float(data) <= float(self.T_MIN):
            self.sendActionToHvac(date, "TurnOnHeater", self.TICKETS)

    def sendActionToHvac(self, date, action, nbTick):
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{nbTick}")
        details = json.loads(r.text)
        print(details)

    def send_event_to_database(self, timestamp, event):
        try:
            print(event)
            conn = self.setup_database()
            cur = conn.cursor()

            # Defining the insert query
            insert_query = f"""
            INSERT INTO sensorDatas (timestamp, temperature)
            VALUES ('{timestamp}', '{event}');
            """
            # Executing the query
            cur.execute(insert_query)

            # Commit the transaction
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()
        except psycopg2.Error as e:
            print("An error occurred while trying to write to the database: ", e)
        except Exception as e:
            print("An unexpected error occurred: ", e)


if __name__ == "__main__":
    main = Main()
    main.start()
