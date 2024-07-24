#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - FIRST LINE TEXT EXTRACTION

This script prompts the user for a file path and extracts the first line of the file.
I also added a path check with the OS module to analyze annoying errors :) 
"""

import os # Importing the os module to check if path exists 

def get_first_line(path): # A function that receives the path, 'with open' gets the file located in this path and opens it in read! 

    with open(path, 'r') as file: 
        first_line = file.readline().strip()

    return first_line



while True: # Iterating endlessly until we decide to stop by pressing q and break

    path = input("Please enter the path to the log file (q for quit): ") # Don't forget to add the extension of file if needed (.txt)

    if path.lower() == 'q': 
        break 

    if os.path.exists(path): # Will help us see if there are errors or permission problems with the path 
        try: 
            print(f"This path exists\nThe first line of the log is: {get_first_line(path)}")
        except Exception as e: # Will catch any error and show it for us for analysis 
            print(f"{e}")
    else:
        print("Wrong path, please try again") 
        
        

