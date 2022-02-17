#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="pdm",
    version="1.0",
    packages=find_packages(),
    description="A Django app to for Parish Developement Model REST API.",
    long_description="file: README.rst",
    url="https://www.nouveta.tech",
    author="Philip Mutua",
    author_email="philip@nouveta.tech",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "Django==4.0",
        "dj-database-url==0.5.0",
        "psycopg2-binary==2.9.3",
        "python-decouple==3.5",
        "pytz==2021.3",
    ],
    scripts=["manage.py"],
)
