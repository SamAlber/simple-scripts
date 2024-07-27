#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - FASTEST TRANSACTION IN ms EXTRACTION 

This script prompts the user for a file path and extracts the fastest executed transaction
+ Path check (OS module)
"""

import os
import re
from datetime import datetime # Importing datetime class from the datetime module (for strptime function which is located within the class )

pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}).*?transaction (\d+) (begun)|(\d{2}:\d{2}:\d{2}\.\d{3}).*?transaction (done), id=(\d+)')  # We will use .compile to create a regex pattern object that we will use in parse_log 

def parse_log(file_path):
    """
    First step: Parsing the log to create a dictionary for future calculations.
    This function reads the log file, matches entries using the regex pattern,
    and stores the start and end times of each transaction in a dictionary.
    """
    transactions = {}

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)  # Creates a match object from the search

            if match:  # None is considered False
                timestamp_str1, transaction_id1, begun, timestamp_str2, done, transaction_id2 = match.groups() 
                
                # Creating a tuple from the match object and passing the elements captured with () with REGEX in a sequence to the variables 
                # If it's a begun line , timestamp_str2, done, transaction_id2 will be None and the ( if begun: ) will be true because it's not None 

                if begun: 
                    timestamp = datetime.strptime(timestamp_str1, '%H:%M:%S.%f')  # Will create a datetime object from the time string that we have in timestamp_str (%f represents ms)
                    transaction_id = transaction_id1
                    action = 'begun'

                elif done:
                    timestamp = datetime.strptime(timestamp_str2, '%H:%M:%S.%f')  # Creating a datetime object from the timestamp string
                    transaction_id = transaction_id2
                    action = 'done'
                
                if transaction_id not in transactions:  # Adding only new logs during the iteration
                    transactions[transaction_id] = {}
                
                transactions[transaction_id][action] = timestamp  # Adding the datetime object to the dictionary
                
                # Example structure of the transactions dictionary:
                # transactions = {
                #     '123': {'begun': datetime_object1, 'done': datetime_object2},
                #     '124': {'begun': datetime_object3, 'done': datetime_object4},
                #     ...
                # }

    return transactions

def find_fastest_transaction(transactions):
    """
    Second step: Calculation
    This function calculates the duration of each transaction and finds the one with the shortest duration.
    """
    min_time = None
    fastest_id = None
    
    for transaction_id, times in transactions.items():

        """
            #Creates a view object (tuple-like but not the exact tuple like in .groups() ) of the key and it's corresponding value 
            (In this case another dictionary {'start': datetime_object1, 'end': datetime_object2} per key (id)
            #Those will be passed in a sequence for transaction_id and times 

         """

        # Checking if both 'begun' and 'done' keys are present 
        
        if 'begun' in times and 'done' in times:
            duration = (times['done'] - times['begun']).total_seconds() * 1000  # convert to milliseconds with total_seconds() that retrives the numerical value from the datetime object (after calculation between objects)

            if min_time is None or duration < min_time:
                min_time = duration 
                fastest_id = transaction_id 
                
                # Iterating through all transaction IDs and updating the min_time if a shorter duration is found
                # The new fastest transaction ID is saved
    
    return fastest_id

while True:
    # Iterating endlessly until we decide to stop by pressing 'q' and break the loop
    path = input("Please enter the path to the log file (q for quit): ")  # Don't forget to add the file extension if needed (.txt)

    if path.lower() == 'q':
        break 

    if os.path.exists(path):  # Checking if the path exists to avoid errors or permission problems
        try: 
            transactions = parse_log(path)
            fastest_id = find_fastest_transaction(transactions)
            if fastest_id:
                print(f"The fastest transaction is: {fastest_id}")
            else:
                print("No complete transactions found.")
        except Exception as e:  # Catching any error and showing it for analysis
            print(f"Error: {e}")
    else:
        print("Wrong path, please try again.")