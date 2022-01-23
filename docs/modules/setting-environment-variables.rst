############
Setting environment Variables
############

The following environment variables are used by the API.

- **SECRET_KEY:** Django secret key
- **DEBUG:** Boolean if true in DEBUG mode.
- **ALLOWED_HOSTS:** List of all allowed hosts e.g localhost
- **DATABASE_URL:** URL of the database e.g postgres://philip:90min2entebe*@localhost:5432/pdm


**Setting Up the Environment**


Create a `.env` file and add the following lines:

Example:

`
export DEBUG=True

export DJANGO_SECRET_KEY=addsecretkey

export POSTGRES_USER=addpostgresuser

export POSTGRES_PASSWORD=addpostgrespassword

export POSTGRES_DB=addpostgresdbname

export POSTGRES_PORT=5432

export POSTGRES_HOST=localhost

`

**Note**: If you are running your API locally don't add the `SENTRY_DSN` variable.


The run `source .env` to set the environment variables.
