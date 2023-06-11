# Base stage
FROM python:3.9-slim AS base

# Set Python-related environment variables to reduce Python bytecode in the container
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Python dependencies stage
FROM base AS python-deps

# Install pipenv and dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# Runtime stage
FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create a new user to run your application
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Copy your application into the container
COPY src/ .

# Run the application
CMD ["python", "src/main.py"]
