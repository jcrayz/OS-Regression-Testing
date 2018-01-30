# CBU Capstone Project

# Contributors
Jenna Cray, Blake Gordon, Christopher Chen

# Setting up

By convention, python packages that are dependencies of this project are enumerated in `requirements.txt`. Install them all at once with `pip install -r requirements.txt`

CRITICAL: install pywin32 from here: https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win-amd64-py3.6.exe/download

These installation shenanigans are documented here: https://github.com/mhammond/pywin32/issues/1126

To prepare your environment to use scripts within allamericanregress, run `python3 allamericanregress/setup.py develop` from the root of the repo.

# Command Line Interface

Execute `python -m allamericanregress` from the root of the repository to use the command line interface.

The GUI is launched by executing `python3 -m allamericanregress --webapp`

# Web App

To initialize the Flask web app for the first time:
```
# add program file to path
export FLASK_APP=allamericanregress/webapp/__init__.py
# initialize database
flask db init
# detect schema changes
flask db migrate
# apply schema changes
flask db upgrade
```

To run it every other future:
```
export FLASK_APP=allamericanregress/webapp/__init__.py
flask run

```


