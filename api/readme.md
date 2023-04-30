# Real Estate API

This is a real estate API built with FastAPI framework and SQLAlchemy ORM. It allows you to manage properties and users through a RESTful interface. Additionally, the app uses a Blackblaze free account to store images in the cloud.

## Features

- Built with FastAPI framework and SQLAlchemy ORM
- Manage properties and users
- Uses Blackblaze free account to store images in the cloud
- Password reset logic with email confirmation
- Unit tests and basic CI/CD pipeline
- Alembic migrations to manage DB versions
- JWT logic to protect endpoints
- Sensitive data encryption before insertion into the DB
- Dockerized with a Dockerfile and docker-compose.yaml file

## Installation

To run the app, you need to have Docker and docker-compose installed on your machine.

1. Change into the root directory of the project:

cd your-repo-name

2. Build the Docker image and start the containers:

docker-compose up --build

3. The API is now available at `http://localhost:5000`.

## Development and testing

To develop the app, you will need to create a virtual environment and install the requirements. Then, you can run the app with the following command:

cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 5000


The app will be available at `http://localhost:5000` in development mode.

To run the unit tests, you can use the following command:

cd api
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -m unittest


## API Documentation

The API documentation is available at `http://localhost:5000/docs` when the app is running. You can use this interface to explore the API and test its endpoints.

## Password Reset

To reset a password. The API will send an email to the user with a token that can be used to reset the password.

## Authentication

To access protected endpoints, you need to provide a JWT token in the `Authorization` header of your requests. You can obtain a token by sending a POST request to the `/login` endpoint with valid credentials.

## Conclusion

This Real Estate API offers a robust solution for managing properties and users, with advanced features like Blackblaze image storage, password reset, and authentication. It is also easy to deploy with Docker and offers comprehensive API documentation.
