############
Requirements
############

Inside the project root (2) there is a directory called requirements with all the .txt files, breaking down the project dependencies like this:

- `base.txt`: Main dependencies, strictly necessary to make the project run. Common to all environments
- `tests.txt`: Inherits from base.txt + test utilities
- `local.txt`: Inherits from tests.txt + development utilities
- `production.txt`: Inherits from base.txt + production only dependencies

Now let’s have a look inside each of those requirements file and what are the python libraries.

**base.txt**

.. example-code::

    Django==4.0

    psycopg2-binary==2.9.3

    python-decouple==3.5

    pytz==2021.3

- **Django**: Django framework
- **psycopg2-binary**: PostgreSQL is my go-to database when working with Django. So I always have it here for all my environments
- **python-decouple**: A typed environment variable manager to help protect sensitive data that goes to your settings.py module. It also helps with decoupling configuration from source code
- **pytz**: For timezone aware datetime fields

**tests.txt**

.. example-code::

    -r base.txt

    black

    coverage==5.5

    factory-boy==3.2.0

    flake8==3.9.2

    isort==5.9.1

    tox==3.23.1

    Sphinx==4.4



The `-r base.txt` inherits all the requirements defined in the `base.txt` file.

- **black**: A Python auto-formatter so you don’t have to bother with styling and formatting your code. It let you focus on what really matters while coding and doing code reviews.
- **coverage**: Lib to generate test coverage reports of your project.
- **factory-boy**: A model factory to help you setup complex test cases where the code you are testing rely on multiple models being set in a certain way.
- **flake8**: Checks for code complexity, PEPs, formatting rules, etc
- **isort**: Auto-formatter for your imports so all imports are organized by blocks (standard library, Django, third-party, first-party, etc).
- **tox**: An interface for CI tools to run all code checks and unit tests.
- **Sphinx**: Documentation generator for Python.

**local.txt**

.. example-code::

    -r tests.txt

    django-debug-toolbar==3.2.1

    ipython==7.25.0


The `-r tests.txt` inherits all the requirements defined in the `base.txt` and `tests.txt` file.

- **django-debug-toolbar**: 99% of the time I use it to debug the query count on complex views so you can optimize your database access.
- **ipython**: Improved Python shell. I use it all the time during the development phase to start some implementation or to inspect code.


**production.txt**

.. example-code::
    -r base.txt

    gunicorn==20.1.0

    sentry-sdk==1.1.0



The `-r base.txt` inherits all the requirements defined in the `base.txt` file

- **gunicorn**: A Python WSGI HTTP server for production used behind a proxy server like Nginx
- **sentry-sdk**: Error reporting/logging tool to catch exceptions raised in production.
