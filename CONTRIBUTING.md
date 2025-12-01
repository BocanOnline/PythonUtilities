# PythonUtilities Developer and Contributing Guide

This project is written in Python using the Python Virtual Environment.
The project includes the project files as well as config files located at your 
config home directory.

## Quick Start
Run the following in separate panes or processes:

```bash
# ../ProjectUtilities
nvim . # open editor at project root
nvim ~/.config/bo # open editor at config root
source .venv/bin/venv
```

## TODO

## Additional Notes

Using these utility commands globally will require a global setup in the future.
The current best practice is to setup a global virtual environment to install
this package into, to be able to use the commands anywhere on the system.

Initialize the Python virtual environment in the project root:

```bash
# ../ProjectUtilities
python -m venv .venv
#python3 -m venv .venv
```

Install dependencies in the virtual environment:

```bash
# ../ProjectUtilities
pip install -r requirements.txt
#pip3 install -r requirements.txt
```

Install to system while linking to project directory:

```bash
# ../ProjectUtilities
pip install --user -e .
#pip3 install --user -e .
#pip install -e .
#pip3 install -e .
```

Test or use commands:

```bash
# ../ProjectUtilities
bo_open
#python bo_open/cli:app
#python3 bo_open/cli:app
```

Deactivate virtual environment and exit project:
```bash
deactivate
```
