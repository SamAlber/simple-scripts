#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - AVERAGE TRANSACTION IN ms CALCULATION 

This script prompts the user for a file path and calculates the average transaction time
+ Path check (OS module)
"""

import os
import re
from datetime import datetime

# Compiling a regex pattern to match the log entries for transaction begun and done
pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}).*?transaction (\d+) (begun)|(\d{2}:\d{2}:\d{2}\.\d{3}).*?transaction (done), id=(\d+)')

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


def calculate_transaction_times(transactions):

    """
    # Second Step: Organizing all transaction durations in a dictionary for calculation in the next function
    """
     
    transaction_times = {}
    
    for transaction_id, times in transactions.items():

        if 'begun' in times and 'done' in times:
            duration = (times['done'] - times['begun']).total_seconds() * 1000

            transaction_times[transaction_id] = duration # No need to worry about duplicates because the parse_log took care of it
    
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

