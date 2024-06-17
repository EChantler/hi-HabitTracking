python -m venv env   

source env/bin/activate

pip freeze > requirements.txt

Run Api: ENVIRONMENT=development python -m app.api.run
Run Tests: ENVIRONMENT=testing python -m pytest tests/
Run Cli: python -m app.cli.run


