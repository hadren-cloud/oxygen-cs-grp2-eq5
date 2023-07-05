# LOG-680 : Template for Oxygen-CS

![image](./doc/wheel.png)

This Python application continuously monitors a sensor hub and manages HVAC (Heating, Ventilation, and Air Conditioning) system actions based on received sensor data.

It leverages `signalrcore` to maintain a real-time connection to the sensor hub and utilizes `requests` to send GET requests to a remote HVAC control endpoint.

This application uses `pipenv`, a tool that aims to bring the best of all packaging worlds to the Python world.

## Requierements

- Python 3.8+
- pipenv

## Getting Started

1. Clone the repository :

```
git clone https://github.com/MarioGith/log680.git
cd log680
```

2. Install the project's dependencies :

```
pipenv install
```

## Setup

This project requires a `.env` file to function correctly. Please create a `variables.env` file in the root of the project directory and ensure it includes the following variables:

- `HOST`: The host address for the service. Format: 'http://[ip_address]'.
- `TOKEN`: The secret token for authentication. Format: Alphanumeric string.
- `TICKETS`: The number of tickets. Format: Numeric string.
- `T_MAX`: The maximum temperature. Format: Numeric string.
- `T_MIN`: The minimum temperature. Format: Numeric string.
- `DB_NAME`: The name of the database. Format: Alphanumeric string.
- `DB_USER`: The username for the database. Format: Alphanumeric string.
- `DB_PASSWORD`: The password for the database. Format: Alphanumeric string.
- `DB_HOST`: The host address for the database. Format: 'localhost' or '[ip_address]'.

Some default variables are set but the project will not work unless you provide the credentials.

## Running the Program

After setup, you can start the program with the following command:

```
pipenv run strart
```

## Logging

The application logs important events such as connection open/close and error events to help in troubleshooting.

## To Implement

There are placeholders in the code for sending events to a database and handling request exceptions. These sections should be completed as per the requirements of your specific application.

## License

MIT

## Contact

For more information, please feel free to contact the repository owner.
