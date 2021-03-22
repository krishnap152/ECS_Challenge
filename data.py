"""Routines associated with the application data.
"""
import json
courses = {}

def load_data():
    """Load the data from the json file.
    """
    with open('./json/course.json', 'r') as openfile:
        # Reading from json file
        courses = json.load(openfile)
    return courses


