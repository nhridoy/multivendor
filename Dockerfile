# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

EXPOSE 8000
# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Copy .env file into the container
COPY .env /code/

# Install dependencies
RUN pip install  -r requirements.txt # --no-cache-dir


# Run Django ASGI application with Daphne
CMD ["daphne", "--bind", "0.0.0.0:8000", "core.asgi:application"]
