# # Use the official Python base image
# FROM python:3.8-slim

# Use the official Ubuntu base image from Docker Hub
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Update package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy only the necessary files into the Docker image
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make entrypoint script executable
COPY ./docker_entrypoint.sh /app/docker_entrypoint.sh
RUN chmod +x /app/docker_entrypoint.sh

# Entrypoint script to prompt the user for test file selection
ENTRYPOINT ["/app/docker_entrypoint.sh"]


# Command to run the Python application or script
# CMD ["python3", "testing/keras_test.py"]
# CMD ["python3", "testing/docTR_test.py"]