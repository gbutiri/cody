import re
import os
import subprocess


###      --- USEFUL FUNCTIONS ---       ###

# CALCULATE INDENTATION
def calculate_indentation(line_number, lines, indent):
    
    if indent:
        indent = int(indent)
    else:
        indent = 0
    
    # Initializing the indentation
    indentation = 0
    
    # List the indenting words
    indenting_words = ['if', 'while', 'for', 'with', 'def', 'class']  
    # Add other keywords as needed
    
    # Iterate backwards from the insertion point
    for i in range(line_number - 2, -1, -1):  
        stripped_line = lines[i].rstrip()
        
        # If the line is not blank
        if stripped_line:
            indentation = len(stripped_line) - len(stripped_line.lstrip())
            
            # Check if the first word is an indenting word
            first_word = stripped_line.lstrip().split(' ')[0]
            if first_word in indenting_words:
                # Increase indentation by 4 spaces
                indentation += 4  
            
            break
    return int(indentation + indent)







###       --- MAIN FUNCTIONS ---        ###


# ADD VARIABLE
def insert_variable_at_line(file_name, var_name, var_type, line_number, indent):
    line_number = int(line_number)

    with open(file_name, 'r') as file:
        lines = file.readlines()

    if var_type == "array" or var_type == "list":
        var_val = "[]"
    elif var_type == "integer" or var_type == "whole number":
        var_val = "0"

    var_code = var_name + " = " + var_val
    # Find the indentation of the previous non-blank line
    indentation = calculate_indentation(line_number, lines, indent)

    # TODO: "detect variable type better."
    # Check if the line number is beyond the current file length
    if line_number > len(lines) or line_number == -1:
        
        indented_code = " " * indentation + var_code.replace("\n", "\n" + " " * indentation)

        with open(file_name, 'a') as file:
            file.write("\n\n" + indented_code)
        
    else:

        # Prepare the new content with the same indentation
        indented_code = " " * indentation + var_code.replace("\n", "\n" + " " * indentation)

        print("line_number", line_number)

        # Insert the new code
        lines.insert(line_number - 1, indented_code + "\n")

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)
    return indented_code

# ADD LOOP
def insert_loop_code_at_line(file_name, item, items, line_number, indent):
    line_number = int(line_number)

    # The rest of the code can be reused later.
    context = "for " + item + ' in ' + items + ":\n    print(" + item + ")"

    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Check if the line number is beyond the current file length
    print("line_number", line_number, "len(lines)", len(lines))
    
    # Compare if we're adding at the end, or splitting the lines and adding between?
    if line_number > len(lines):

        with open(file_name, 'a') as file:
            # TODO: indent here if indent is detected in the 3rd parameter.
            context.replace("\n\n", "\n\n" + " " * indentation)
            file.write(" " * indentation + context)
    else:
        # Find the indentation of the previous non-blank line
        indentation = calculate_indentation(line_number, lines, indent)

        # Prepare the new content with the same indentation
        indented_code = " " * indentation + context.replace("\n", "\n" + " " * indentation)

        # Insert the new code
        lines.insert(line_number - 1, indented_code + "\n")

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)

# ADD CONDITION
def insert_conditional_code_at_line(file_name, var_one, operator, var_two, line_number, indent):

    line_number = int(line_number)
    
    context = "if " + var_one + " " + operator + " " + var_two + ":\n    print('# Condition is True')\nelse:\n    print('# Condition is False')"

    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Check if the line number is beyond the current file length
    print("line_number", line_number, "len(lines)", len(lines))

    # Compare if we're adding at the end, or splitting the lines and adding between?
    if line_number > len(lines):

        with open(file_name, 'a') as file:
            # TODO: indent here if indent is detected in the 3rd parameter.
            context.replace("\n\n", "\n\n" + " " * indentation)
            file.write(" " * indentation + context)
    else:
        # Find the indentation of the previous non-blank line
        indentation = calculate_indentation(line_number, lines, indent)
        print("calculated indentation:", indentation)

        # Prepare the new content with the same indentation
        indented_code = " " * indentation + context.replace("\n", "\n" + " " * indentation)

        # Insert the new code
        lines.insert(line_number - 1, indented_code + "\n")

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)

# REMOVE LINE
def remove_code_at_line(file_name, line_number):
    line_number = int(line_number)

    with open(file_name, 'r') as file:
        lines = file.readlines()
        
    # Check if line number is valid
    if 0 < line_number <= len(lines):
        # Store the line for potential undo
        undo_line = lines[line_number - 1]
        print("Line to undo: ", undo_line)
        
        # Remove the line (line numbers in the request are likely 1-based, not 0-based)
        lines.pop(line_number - 1)
        
    with open(file_name, 'w') as file:
        file.writelines(lines)
    print("Removed line", line_number)

# REMOVE CODE BETWEEN LINES
def remove_code_between_lines(file_name, line_start, line_end):
    
    line_start = int(line_start)
    line_end = int(line_end)
    undo_lines = []
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    # Check if line number is valid
    if 0 < line_start <= len(lines) and 0 < line_end <= len(lines):
        
        # Adjusted indices for 1-based to 0-based
        for i in range(line_end - 1, line_start - 2, -1):
            # Remove line and add to undo_lines
            undo_lines.append(lines.pop(i))  
        
    with open(file_name, 'w') as file:
        file.writelines(lines)
    print("Removed lines from ", line_start, "to", line_end)
    # Return the removed lines for undo functionality
    return undo_lines  

# ADD LINE
def add_blank_line_at_line(file_name, line_number):
    line_number = int(line_number)

    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Check if line number is valid
    # Allow adding at the end of the file
    if 0 < line_number <= len(lines) + 1: 
        # Insert a blank line at the specified line number
        lines.insert(line_number - 1, "\n")

    with open(file_name, 'w') as file:
        file.writelines(lines)
    print("Added a new line at line", line_number)

# ADD COMMENT
def add_comment_at_line(file_name, line_number, comment):
    line_number = int(line_number)

    comment_code = "# " + comment + "\n"

    with open(file_name, 'r') as file:
        lines = file.readlines()
        
    # Check if line number is valid
    # Allow adding at the end of the file
    if 0 < line_number <= len(lines) + 1: 
        # Insert a blank line at the specified line number
        lines.insert(line_number - 1, comment_code)
    else:
        lines.insert(len(lines), comment_code)

    with open(file_name, 'w') as file:
        file.writelines(lines)
    print("Added a new comment at line", line_number)

# CREATE A FUNCTION
def ceate_function(file_name, function_name, parameters, line_number, indent):

    func_code = "def " + function_name + "(" + parameters + "):\n    pass\n\n"
    print("func_code:", func_code)
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    if line_number is None:
        line_number = 0

    if 0 < line_number <= len(lines) + 1: 
        # Insert a blank line at the specified line number
        lines.insert(line_number - 1, func_code)
    else:
        lines.insert(len(lines), func_code)
        
    with open(file_name, 'w') as file:
        file.writelines(lines)
    print("Added a new function at line", line_number)

