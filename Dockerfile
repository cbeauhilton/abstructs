# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.1.6
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock README.md /app/

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN poetry install --only main

# Copy the current directory contents into the container at /app
# COPY . /app

# Expose port 8000
EXPOSE 8000

# Run FastAPI server
CMD ["poetry", "run", "uvicorn", "src.abstructs.main:app", "--host", "0.0.0.0", "--port", "8000"]
