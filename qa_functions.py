import re
import os
import subprocess
import inspect

def get_qa_obj():
    frame = inspect.currentframe()
    function_name = inspect.getframeinfo(frame).function
    line_number = frame.f_lineno
    
    return function_name, line_number


def verify_variable_insertion_at_line(file_name, indented_code, line_number):

    # QA things:
    qa_obj = get_qa_obj()
    
    # inspect the file and see if the variable "variable_name" has been declaed on line "line_number"
    
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        if line_number <= len(lines):

            # The true test.
            if indented_code in lines[line_number - 1]:
                return True
                
        else:
            # Exceeded line numbers.
            return False
    
    except FileNotFoundError:
        pass  # Handle file not found error
        
    # Default to False if conditions are not met.
    print(f"No condition met: {qa_obj[0]} on line {qa_obj[1]}")
    return False  # You need to add this return statement