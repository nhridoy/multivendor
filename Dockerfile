# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

EXPOSE 8000
# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /code
COPY . /app

# Install dependencies
RUN pip install  -r requirements.txt # --no-cache-dir



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# RUN echo 'appuser ALL=(ALL) NOPASSWD: ALL' >  /etc/sudoers.d/appuser
USER appuser

RUN chmod +x entrypoint.sh

# Set the entrypoint script as the default command to execute when the container starts
ENTRYPOINT ["sh", "entrypoint.sh"]