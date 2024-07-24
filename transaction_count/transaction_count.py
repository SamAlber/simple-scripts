#!/usr/bin/env python3

"""
SAMUEL ALBERSHTEIN - TRANSACTION COUNT EXTRACTION

This script prompts the user for a file path and extracts the number of transations (we will count the completed ones)
+ Path check
"""
import os 

def count_end_transactions(path):

    count_start = 0 
    count_end = 0 
    
    with open(path, 'r') as file:

        for line in file:
            if 'Transaction Start' in line:
                count_start += 1
            
            if 'Transaction End' in line:
                count_end += 1
    
    transactions_count = min(count_start, count_end) # We will take only the successful, so if there are more start than end we will take the end count. 

    return transactions_count 



while True: # Iterating endlessly until we decide to stop by pressing q and break the loop

    path = input("Please enter the path to the log file (q for quit): ") # Don't forget to add the extension of file if needed (.txt)

    if path.lower() == 'q': 
        break 

    if os.path.exists(path): # Will help us see if there are errors or permission problems with the path 
        try: 
            transactions_count = count_end_transactions(path)
            print(f"This log contains: {transactions_count} Completed transactions")
        except Exception as e: # Will catch any error and show it for us for analysis 
            print(f"{e}")
    else:
        print("Wrong path, please try again") 