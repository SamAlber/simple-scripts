#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - FASTEST TRANSACTION IN ms EXTRACTION 

This script prompts the user for a file path and extracts fastest executed transaction
+ Path check (OS module)
"""

import os
import re
from datetime import datetime # Importing datetime class from the datetime module (for strptime function which is located within the class )

pattern = re.compile(r'\[(.*?)\] Transaction (Start|End) ID: (\d+)') # We will use .compile to create a regex pattern object that we will use in parse_log 

def parse_log(file_path): # First step: Parsing the log to create a disctionary for future calculations 

    transactions = {}

    with open(file_path, 'r') as file:

        for line in file:

            match = pattern.search(line) # Creates a match object of the search 

            if match: # Match = true, None = False  

                timestamp_str, action, transaction_id = match.groups() # Creating a tuple from the match object and passing the elemnts in a sequence to the variables 

                timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f') # Will create a datetime object from the time that we had in [] timestamp_str (%f represents ms)
                    
                if transaction_id not in transactions: # Adding new logs during the iteration

                    transactions[transaction_id] = {}
                    
                transactions[transaction_id][action.lower()] = timestamp # Explanation below

                """
                # Attaching the datetime object correlated to start/end in each iteration after we have the main id key for the specific transaction 
                # Creating a dictionary inside a dictionary 
                

                transactions = {
                    '123': {'start': datetime_object1, 'end': datetime_object2},
                    '124': {'start': datetime_object3, 'end': datetime_object4},
                    ...
                }

                """

    return transactions


def find_fastest_transaction(transactions): # Second step : Calculation 
    min_time = None
    fastest_id = None
    
    for transaction_id, times in transactions.items(): 
        """
            #Creates a view object (tuple-like but but not the exactly a tuple like in .groups() ) of the key and it's corresponding value 
            (In this case another dictionary with start and end that contain the datetime object each)

         """

        if 'start' in times and 'end' in times:

            duration = (times['end'] - times['start']).total_seconds() * 1000  # convert to milliseconds with total_seconds() that retrives the numerical value from the datetime object

            if min_time == None or duration < min_time: 
                min_time = duration 
                fastest_id = transaction_id 
            """
            We will iterate all transaction id's and update the min_time if duration < min_time and the new fastest 
            transaction will be saved. 

            """
    
    return fastest_id





while True: # Iterating endlessly until we decide to stop by pressing q and break the loop

    path = input("Please enter the path to the log file (q for quit): ") # Don't forget to add the extension of file if needed (.txt)

    if path.lower() == 'q': 
        break 

    if os.path.exists(path): # Will help us see if there are errors or permission problems with the path 
        try: 

            transactions = parse_log(path)
            fastest_id = find_fastest_transaction(transactions)
            print(f"The fastest transaction is: {fastest_id}")

        except Exception as e: # Will catch any error and show it for us for analysis 
            print(f"{e}")
    else:
        print("Wrong path, please try again") 
