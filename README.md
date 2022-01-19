[![CircleCI](https://circleci.com/gh/pmutua/pdm-api/tree/main.svg?style=svg)](https://circleci.com/gh/pmutua/pdm-api/tree/main)
# Parish Development Model API

Parish Development Model REST API

# Prerequisites

1. [Python 3.9 >=](https://www.python.org/downloads/)
2. [Virtualenv](https://pypi.org/project/virtualenv/)
3. [PostgreSQL](https://www.postgresql.org/)
4. [Make](https://makefiletutorial.com/)
5. Create a database and user for the API to use.

# For Windows Users

If you are using windows you will need to install [chocolatey](https://chocolatey.org/install) to install [Make](https://makefiletutorial.com/) follow the link for installation instructions.

Then run `choco install make`

# Running the project locally

1. Make sure you have the prerequisites installed.

2. Clone the repository `git clone https://github.com/pmutua/pdm-api.git`

3. `cd` to project

4. Create a virtual environment run `make venv`

5. Activate Python environment run **Linux** `source venv/bin/activate` (or `source venv/Scripts/activate` on Windows)

6. Create `.env` file run `touch .env` in the root directory (where **manage.py** is located).

7. Add the following environment variables in your `.env` file as follows:

**Example**

```bash
    SECRET_KEY=secretkey
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=github_actions
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
    DB_PORT=5432


```

8. The run `source .env` to set the environment variables. 

9. Run `make migrate` to apply migrations.
    
10. Create a superuser run `make superuser`

11.  Launch the application by running `python manage.py runserver`

To view all **Make** commands run `make help`
