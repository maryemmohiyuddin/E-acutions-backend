FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the project files
COPY . ./

# Default command is not set here; it will be handled in docker-compose.yml
