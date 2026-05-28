# Install Instructions

## Requirements

- Linux
- python3

## Setup

1. Open a terminal in the project root.
2. Create a virtual environment:
   python3 -m venv .venv
3. Activate it:
   source .venv/bin/activate
4. Install Django:
   pip install Django

## Initialize Database And Admin

1. Run:
   ./install.sh


- username: admin
- password: admin


## Run The App

1. Start server:
   python3 manage.py runserver
2. Open:
   http://127.0.0.1:8000/
