# Greenhouse Companion

Greenhouse Companion is a comprehensive web application developed as a culminating project at Holberton School. This versatile web app serves as a virtual garden assistant, enhancing the gardening experience through a range of functionalities. This repository contains the backend component of the application, implemented as a RESTful API using Python Flask.

The backend API not only supports gardening features but also doubles as a domotic system: A microcontroller can post data from sensors to the API, which will analyze the data and respond with actions based on the received values. Users can also make decisions through the web app, enabling seamless integration of automation with gardening.

## Table of Contents

- Introduction
- Features
- Prerequisites
- Installation
- API Documentation
- Contributing
- License

## Features

- Sensor Integration and Automation: Enable a microcontroller to post data to the API. It will send back responses for action based on the sent data and user requirements.
- Real-Time Sensor Data Logging: Store data from microcontrollers allowing users to track and monitor environmental conditions within the greenhouse or focus on specific sensor data for analysis.
- Plant Manager: Manage greenhouse plant data by area, track production, harvest and monitor growth.
- To-Do List: Create and manage gardening task lists and reminders.
- Plant Information and Growing Advice: Access a database of plant information and care instructions.

## Software Requirements

The Greenhouse Companion API has been developed and tested on the following software versions:

- **Mac OS Sonoma (Version 14.0):**

- **Python3 (Version 3.11):**

- **MySQL (Ver 8.1.0 for macos13.3 on arm64):**

- **SQLite (Version 3.39.5):**

## Getting Started

Follow these steps to set up and run the Greenhouse Companion API on your local machine.

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```
git clone git@github.com:benjaminvandammeholberton/portfolio_GreenhouseCompanion_V2.git
```

### 2. Create a Virtual Environment

Navigate to the project's root directory and create a virtual environment using Python 3:

```
python3 -m venv .venv
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Choose Your Database

You have the option to choose between SQLite and MySQL as your database. Set the DATABASE environment variable accordingly:
For SQLite:

```
export DATABASE=sqlite
```

For MySQL, set the following environment variables with your database connection details:

```
export DATABASE=mysql
export GREENHOUSE_MYSQL_USER='<your_mysql_username>'
export GREENHOUSE_MYSQL_PWD='<your_mysql_password>'
export GREENHOUSE_MYSQL_HOST='<your_mysql_host>'
export GREENHOUSE_MYSQL_DB='<your_mysql_database>'
export GREENHOUSE_MYSQL_PORT='<your_mysql_port>'
```

### 5. Run the API

Start the API with the following command. By default, it will run on http://127.0.0.1:5000:

```
flask run
```

### 6. Add Vegetable Data

To add data about vegetables to the database, open a new terminal window, navigate to the project's root directory, and run the following command:

```
python3 add_vegetable_info.py ./vegetables_data/vegetable_infos_data.json
```

You can verify that the data has been added by making a GET request to:

```
http://127.0.0.1:5000/vegetable_infos
```

## Contributing

We welcome contributions to the Greenhouse Companion project! If you find any issues or have ideas for improvements, please feel free to open an issue or submit a pull request. Follow these guidelines when contributing:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure tests pass.
4. Commit your changes with a clear and concise commit message.
5. Push your changes to your fork.
6. Submit a pull request, explaining the purpose and changes made.

## Related projects

- [Greenhouse Companion Frontend](https://github.com/benjaminvandammeholberton/portfolio_GreenhouseCompanion_Frontend): The frontend component of the Greenhouse Companion web application.

## Licensing

This project is licensed under the [MIT License](LICENSE).
