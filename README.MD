```markdown
# Hi - Habit Tracking

Welcome to the Habit Tracking App! This application helps you track and manage your habits effectively through a user-friendly interface and powerful API.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- Virtualenv

### Installation

1. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Freeze the current requirements:**
    ```bash
    pip freeze > requirements.txt
    ```

### Running the Application

#### Run the API
To run the API in a development environment:
```bash
ENVIRONMENT=development python -m app.api.run
```

#### Run the CLI
To run the Command Line Interface:
```bash
python -m app.cli.run
```

#### Run the CLI and API Together
> **Note:** This feature is currently broken. Please run the API and CLI separately.

To attempt to run both together:
```bash
python -m run
```

### Running Tests

To run all the tests:
```bash
ENVIRONMENT=testing python -m pytest tests/
```

### Creating a Sample Database

To create a sample database called `sample_db.db`:
```bash
SQLALCHEMY_DATABASE_URL=sqlite:///sample_db.db python -m tests.sample_data.create_sample_db
```

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License

---

Happy habit tracking!
```


