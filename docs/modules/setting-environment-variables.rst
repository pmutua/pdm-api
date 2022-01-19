############
Setting environment Variables
############

The following environment variables are used by the API.

- **SECRET_KEY:** Django secret key
- **DEBUG:** Boolean if true in DEBUG mode. 
- **ALLOWED_HOSTS:** List of all allowed hosts e.g localhost
- **DATABASE_URL:** URL of the database e.g postgres://philip:90min2entebe*@localhost:5432/pdm

### Setting Up the Environment

Create a `.env` file and add the following lines:

Example: 

```bash
    SECRET_KEY=django-insecure-yr@$l&z=k(y$u8%*xq+p75j+-3m65ic@jfuuq52g(ayej-@k@d
    DEBUG=True
    ALLOWED_HOSTS=*
    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/databasename
    SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
```

**Note**: If you are running your API locally don't add the `SENTRY_DSN` variable.


The run `source .env` to set the environment variables.