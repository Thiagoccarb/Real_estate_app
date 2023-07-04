# Real Estate App

Welcome to the Real Estate App! This is a full-featured real estate application that allows you to manage houses, create users, and perform various operations related to real estate listings. This README.md file will guide you through the installation and setup process.

## Prerequisites

Before you begin, please ensure you have the following dependencies installed:

- Docker
- Docker Compose

## Installation

To install and run the Real Estate App, follow these steps:

1. Clone the repository to your local machine:

   git clone <repository_url>

2. Navigate to the project's root directory:

cd real-estate-app

3. Create a .env file based on the provided .env.example file. Update the necessary configuration values such as database credentials, API keys, and email settings.

4. Create a free account at Blackblaze and obtain the necessary credentials to upload pictures to your bucket.

5. Configure an email account with permission to be used by third-party libraries for sending emails.

6. Start the application using Docker Compose:

  docker-compose up -d

This command will spin up the backend, frontend, and MySQL database containers, and orchestrate their communication.

## Usage

The Real Estate App offers several features and pages to help you manage real estate listings. Here's an overview of the available pages:

- **Landing Page**: The home page of the application, providing an introduction to the app and its features.

- **Houses for Rent/Sale**: These pages display a list of houses available for rent or sale, respectively. Users can browse through the listings and view more details about each property.

- **House Details**: This page provides detailed information about a specific house, including its features, location, and contact information.

- **Add Property Page**: Users can access this page to add new properties to the app. Note that you must be logged in to access this feature.

To get started, you can use the default user credentials provided in the backend migration files. Please refer to the backend code for the specific login details.

## Roadmap

The Real Estate App is an ongoing project, and more features and improvements are planned for the future. Stay tuned for updates and new releases.

---

We hope you enjoy using the Real Estate App! If you have any questions or encounter any issues, please don't hesitate to reach out to us. Happy real estate management!