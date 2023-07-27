FROM python:3.8

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install python-dotenv

# Copy and install Python dependencies
COPY Pipfile* ./
RUN pip install pipenv && pipenv install --system --deploy

# Copy the rest of the application code
COPY . .

# Start the application
CMD ["python", "src/main.py"]
