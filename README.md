[![CircleCI](https://circleci.com/gh/pmutua/pdm-api/tree/main.svg?style=svg&circle-token=e518c17c9f0a1469f8d4521d44ea72a005ad0cd6)](https://circleci.com/gh/pmutua/pdm-api/tree/main)
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


# Contributing 

1. Fork this repository. This will create a fork of the project under your user account.

2. Next, clone your local version down to your local machine.

3. In order to make it easy to keep your fork in sync with the original, add the original as a remote:

    **NOTE:**This is your forked project repository.

    run `git remote add upstream https://github.com/<yourforkedrepository>.git`

    Note: If you check your remotes (**git remote -v**), you can now see that you have two "remotes" that your local repo is pointed towards: **origin**, which points to your repo, and upstream, which points to the **original**.

Since you want to branch from whatever the project's default branch is (this is often master, but in the case it's **main**), make sure you're on the default branch and it's up-to-date with the **source repo**. If you just forked it, it always will be—but if there have been a lot of changes to the original repo since you forked it, yours might be out of sync. Here's how to get yours in sync on a project where the default branch is **main**:

    1. Run `git fetch upstream`

    2. Run `git merge upstream/main`

    3. Run `git push origin main`


Now you can spin up your new branch:

    1. Run `git checkout -b <newbranch>`

    2. Run `git push origin <newbranch>`


Now, you can create a pull request in the GitHub user interface. Visit your repo on GitHub and click the "New Pull Request" button, and you can create your PR from there. Make sure to explain the purpose, context, and anything else necessary for reviewers to understand the PR. See GitHub's "[How to write the perfect pull request](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)".

<!-- Security scan triggered at 2025-09-01 20:11:59 -->

<!-- Security scan triggered at 2025-09-09 05:51:58 -->

<!-- Security scan triggered at 2025-09-28 16:00:58 -->