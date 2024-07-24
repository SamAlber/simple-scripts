#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - FIRST LINE TEXT EXTRACTION

This script prompts the user for a file path and extracts the first line of the specified file.
"""

import os 

def get_first_line(path):
    with open(path, 'r') as file:
        first_line = file.readline().strip()
    return first_line


while True:

    path = input("Please enter the path to the log file (q for quit): ")

    if path.lower() == 'q':
        break

    if os.path.exists(path):
        try:
            print(f"This path exists\nThe first line of the log is: {get_first_line(path)}")
        except Exception as e:
            print(f"{e}")
    else:
        print("Wrong path, please try again")
        
        

