import re
import os
import subprocess

###           --- MATHCES ---           ###

# General coding functions
def match_line_number(text):
    pattern = r"(?: at line|on line) (\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def match_indentation(text):
    pattern = r"(?:and indent) (\d+) spaces"
    match = re.search(pattern, text, re.IGNORECASE)
    return int(match.group(1)) if match else None


###    --- Base coding functions ---    ###

# Declare a variable:
def match_variable_declaration(text):
    pattern = r"(?:Add a variable|Create a variable|Make a variable|Declare a variable) (\w+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

def match_variable_type(text):
    pattern = r"(?:and make it|make it|as) (?:a|an) (\w+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1) if match else None

# Declare a loop:
def match_loop_pattern(text):
    pattern = r"(?:Make a loop|Make a loop for|Add a loop|Create a loop|Add a for loop|Create a for loop)"
    match = re.search(pattern, text, re.IGNORECASE)
    return True if match else None

def match_loop_items(text):
    pattern = r"(?:with|for) (\w+) (?:in) (\w+)"
    match_add_loop = re.search(pattern, text, re.IGNORECASE)

    item = match_add_loop.group(1).strip()
    items = match_add_loop.group(2).strip()

    return item, items if match_add_loop else None

# Declare a condition
def match_conditional(text):
    pattern = r"(?:Make|Add|Create) (?:an if statement|a condition) (?:where)"
    match = re.search(pattern, text, re.IGNORECASE)
    return True if match else None

def match_conditional_items(text):

    pattern = r"(\w+(?:\.\w+)?) (equals|is equal to|does not equal|is not equal to|is greater than and equal to|is less than an equal to|is greater than|is less than|is not in|not in|is in|in|and|or|is not|is) (\w+)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:

        var_one = match.group(1).strip()
        comparison = match.group(2).strip()
        var_two = match.group(3).strip()
        if var_two in ["blank","empty"]:
            var_two = '""'

        operator_map = {
            "equals": "==", 
            "is equal to": "==",
            "does not equal": "!=", 
            "is not equal to": "!=",
            "is greater than and equal to": ">=", 
            "is less than an equal to": "<=",
            "is greater than": ">", 
            "is less than": "<",
            "is not in": "not in",
            "not in": "not in", 
            "is in": "in",
            "in": "in", 
            "and": "and", 
            "or": "or",
            "is not": "is not", 
            "is": "is"
        }
        
        operator = operator_map.get(comparison)

        if operator:
            return var_one, operator, var_two
        else:
            return None

# Remove a line
def match_remove_lines(text):
    pattern = r"(?:Remove line number|Remove line|Remove the code at line) (\d+)"
    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1).strip() if match else None

# Remove a range of lines
def match_remove_multi_lines(text):
    pattern = r"(?:Remove lines from|Remove lines|Remove from line)"
    match = re.search(pattern, text, re.IGNORECASE)

    return True if match else None

def get_remove_multi_lines(text):
    pattern = r"(\d+) (?:through|to|through line|to line) (\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).strip(), match.group(2).strip()
    else:
        return None

# Add a blank line
def match_add_blank_line(text):
    pattern = r"(?:Add a blank line|Add a new line|Add a line|Add line|Add an empty line) (?:on|at) (?:line|line number) (\d+)"
    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1).strip() if match else None

# Add a comment line
def match_add_comment_line(text):
    pattern = r"(?:Add a new comment line|Add a comment line|Add a new comment|Add a comment|Add comment) (?:on|at) (?:line|line number) (\d+)"
    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1).strip() if match else None
    
def match_comment_context(text):
    pattern = r"(?:Add a new comment line|Add a comment line|Add a new comment|Add a comment|Add comment) (?:on|at) (?:line|line number) (\d+). (.*)"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).strip(), match.group(2).strip()
    else:
        return None

# Create a function
def match_create_function(text):
    pattern = r"(?:Make a|Create a|Write a|Add a) (?:function|method) (?:named|by the name of|by the name|with the name|and name it|name it|with the name of) (\w+)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    return match.group(1).strip() if match else None

def match_function_parameters(text):
    pattern = r"(?: and create the|and add the|and give it the|and give it|and include the)(?: following)? (?:parameters|variables) ([\w\s]+)"
    match = re.search(pattern, text, re.IGNORECASE)

    parameters = match.group(1).strip().split()
    result = ", ".join(parameters)
    
    return result
