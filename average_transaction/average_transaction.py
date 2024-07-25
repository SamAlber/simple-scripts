#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - AVERAGE TRANSACTION IN ms CALCULATION 

This script prompts the user for a file path and calculates the average transaction time
+ Path check (OS module)
"""

import os
import re
from datetime import datetime # Importing datetime class from the datetime module (we need the strptime function which is located within the class )

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
                    
                transactions[transaction_id][action.lower()] = timestamp # .lower() for consistency 

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


def calculate_transaction_times(transactions):

    """
    # Second Step: Organizing all transaction durations in a dictionary for calculation in the next function
    """
     
    transaction_times = {}
    
    for transaction_id, times in transactions.items():

        if 'start' in times and 'end' in times:
            duration = (times['end'] - times['start']).total_seconds() * 1000
            transaction_times[transaction_id] = duration
    
    return transaction_times



def calculate_average_transaction_time(transaction_times): 

    """
    # Third Step: Calculating the average using the sum of the all the values (sum) attached to the keys (.values())
    """

    total_time = sum(transaction_times.values()) 

    if transaction_times: # If transaction_times is not empty 
        average_time = total_time / len(transaction_times)
    else:
        average_time = None 

    return average_time






while True: # Iterating endlessly until we decide to stop by pressing q and break the loop

    path = input("Please enter the path to the log file (q for quit): ") # Don't forget to add the extension of file if needed (.txt)

    if path.lower() == 'q': 
        break 

    if os.path.exists(path): # Will help us see if there are errors or permission problems with the path 
        try: 

            transactions = parse_log(path)
            transaction_times =  calculate_transaction_times(transactions)
            average_time = calculate_average_transaction_time(transaction_times)

            print(f"The average transaction time is: {average_time} ms")

        except Exception as e: # Will catch any error and show it for us for analysis 
            print(f"{e}")
    else:
        print("Wrong path, please try again") 
