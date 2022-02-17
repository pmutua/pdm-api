############
Settings
############

Also following the environments and modes premise, the settings are setup in multiple settings modules. Those are going to serve as the entry point to determine in which mode you running the project.

Inside the simple project package, there is a directory called settings broken down into the following files like this:

```markdown

workspace/                       (1)
├── pdm/                   (2)
│   ├── .git/
│   ├── manage.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── local.txt
│   │   ├── production.txt
│   │   └── tests.txt
│   └── pdm/              (3)
│       ├--- __init__.py
│       ├── settings/
│           ├── __init__.py
│           ├── base.py
│           ├── local.py
│           ├── production.py
│           └── tests.py
│       
│       
│       
│       
│       
│       
└── venv/

```