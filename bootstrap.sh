#!/bin/sh

#-----------Execute recipe_API-----------------:
export FLASK_APP=./recipe/index.py


#-----------Execute registration_API-----------:
#export FLASK_APP=./recipe/registration.py
pipenv run flask --debug run -h 0.0.0.0
