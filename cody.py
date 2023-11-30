import re
import os
import subprocess

def answer_question(input_text):
    # Your existing logic to answer questions
    return "Answering other questions... " + input_text


def create_file(file_name, folder_name='.'):
    file_name = file_name.strip().replace(" ", "_")

    if folder_name != '.':
        folder_name = folder_name.strip().replace(" ", "_") + "/"
        print("Creating file", file_name, "in folder", folder_name)
    else:
        print("Creating file", file_name)
        folder_name = folder_name + '/'

    try:
        with open(folder_name + file_name, 'w') as file:
            file.write("")
        print(f"Created file named '{file_name}' in '{folder_name}'")
    except OSError as e:
        print(f"Error creating file: {e}")

def add_context(file_name, context):
    print("Opening file ", file_name)
    # Strip any leading/trailing spaces from the file name
    file_name = file_name.strip()

    # Create a file in write mode
    try:
        with open(file_name, 'w') as file:
            file.write("")
        with open(file_name, 'a') as file:
            context = context.replace(" new line ", "\n")
            file.write(context)
            pass
        print(f"Saved file named '{file_name}'")
    except OSError as e:
        print(f"Error creating file: {e}")


###     --- Open a file and run ---     ###

def run_file(file_name):
    print("Runing file ", file_name)
    # Strip any leading/trailing spaces from the file name
    file_name = file_name.strip()

    # Create a file in write mode
    try:
        # run file code.
        result = subprocess.run(['python', file_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Output the result of running the file
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
        else:
            print("No errors.\n")
        print(f"Ran file named '{file_name}' successfully.")

        pass
        
    except OSError as e:
        print(f"Error creating file: {e}")




###      --- USEFUL FUNCTIONS ---       ###

# CALCULATE INDENTATION
def calculate_indentation(line_number, lines, indent):
    
    # Debug code
    print('calculate_indentation - line_number: ', line_number)
    print('calculate_indentation - indent: ', indent)
    
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
        print('calculate_indentation - loop #: ', i)
        stripped_line = lines[i].rstrip()
        print('calculate_indentation - stripped_line #: ', stripped_line)
        
        # If the line is not blank
        if stripped_line:
            indentation = len(stripped_line) - len(stripped_line.lstrip())
            
            # Check if the first word is an indenting word
            first_word = stripped_line.lstrip().split(' ')[0]
            if first_word in indenting_words:
                # Increase indentation by 4 spaces
                indentation += 4  
            
            print('calculate_indentation - indentation #: ', indentation)
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

    print("var_code:", var_code)

    # TODO: "detect variable type better."
    # Check if the line number is beyond the current file length
    if line_number > len(lines) or line_number == -1:
        print("line_number", line_number, "len(lines)", len(lines))
        with open(file_name, 'a') as file:
            file.write("\n\n" + var_code)
    else:
        # Find the indentation of the previous non-blank line
        print("insert_variable_at_line - indent: ", indent)
        indentation = calculate_indentation(line_number, lines, indent)
        print("insert_variable_at_line - indentation: ", indentation)

        # Prepare the new content with the same indentation
        indented_code = " " * indentation + var_code.replace("\n", "\n" + " " * indentation)

        print("line_number", line_number)

        # Insert the new code
        lines.insert(line_number - 1, indented_code + "\n")

        # Write back to the file
        with open(file_name, 'w') as file:
            file.writelines(lines)

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
    pattern = r"(?:Add a new comment line|Add a comment line|Add a new comment|Add a comment|Add comment) (?:on|at) (?:line|line number) (\d+).(.*)"
    match = re.search(pattern, text, re.IGNORECASE)

    return match.group(1).strip(), match.group(2).strip() if match else None

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

###        --- OPEN THE FILE ---        ###

def open_file(file_name):

    while True:

        file_input_text = input("\n\nFile Contents: ")

        if file_input_text.lower() == 'close the file':
            print(f"Closing the file {file_name} Goodbye!")
            break

        # Detect line number match and indentation specifications.
        line_number = match_line_number(file_input_text)
        indent = match_indentation(file_input_text)
        
        
        
        # CODE MATCHES
        
        # Declare variable
        match = match_variable_declaration(file_input_text)
        if match:

            variable_type = match_variable_type(file_input_text)

            insert_variable_at_line(file_name, match, variable_type, line_number, indent)

        # Add a simple loop
        match = match_loop_pattern(file_input_text)
        if match:

            item, items = match_loop_items(file_input_text)

            print("Got: item:", item, ", items:" , items, ", line number:", line_number, ", indent:", indent)
            insert_loop_code_at_line(file_name, item, items, line_number, indent)

        # Add a conditional IF
        match = match_conditional(file_input_text)
        if match:
        
            var_one, operator, var_two = match_conditional_items(file_input_text)
            print("Got: var_one:", var_one, ", operator:" , operator, ", var_two:" , var_two, ", line number:", line_number, ", indent:", indent)

            insert_conditional_code_at_line(file_name, var_one, operator, var_two, line_number, indent)

            print(f"Uni: Added for loop code at the end of the file: '{file_name}'")

        # Remove one line of code
        match = match_remove_lines(file_input_text)
        if match:
            
            remove_code_at_line(file_name, match)
            
        # Remove multiple lines of code.
        match = match_remove_multi_lines(file_input_text)
        if match:
            
            line_start, line_end = get_remove_multi_lines(file_input_text)
            remove_code_between_lines(file_name, line_start, line_end)
            
        # Add a blank line.
        match = match_add_blank_line(file_input_text)
        if match:
        
            add_blank_line_at_line(file_name, match)
        
        # Add a comment line.
        match1, match2 = match_add_comment_line(file_input_text)
        if match1 and match2:
            
            line_number, comment = match_add_comment_line(file_input_text)
            add_comment_at_line(file_name, line_number, comment)
        
        # Create a function
        match = match_create_function(file_input_text)
        if match:
            
            parameters = match_function_parameters(file_input_text)
            
            ceate_function(file_name, match, parameters, line_number, indent)


while True:
    input_text = input("\n\n--------\nUser: ")

    if input_text.lower() == 'goodbye' or input_text.lower() == 'good bye' :
        print("Goodbye!")
        break

    # Pattern for making a file with optional folder.
    pattern_create_file = r"(?:(?:I want to|I'd like to|I need to) )?(?:make a file|create a file) (?:(?:in the) (.+?) (?:folder|directory) )?(?:named|by the name of|and name it) (.+)"
    # Test against file creation
    match_create_file = re.search(pattern_create_file, input_text, re.IGNORECASE)

    pattern_create_folder = r"(?:(?:I want to|I'd like to|I need to)) ?(?:make a folder|create a folder) (?:named|by the name of|and name it) (.+) "
    # Test against file creation
    match_create_flder = re.search(pattern_create_folder, input_text, re.IGNORECASE)

    pattern_add_context = r"(?:Open file|Open the file) (.+) (?:and add the following content.|and add the following text.|and add this.) (.+)"
    match_add_context = re.search(pattern_add_context, input_text, re.IGNORECASE)

    pattern_run_file = r"(?:Run the file|Execute the file) (.+)"
    match_run_file = re.search(pattern_run_file, input_text, re.IGNORECASE)

    pattern_open_file = r"(?:Open the file named|Open the file by the name of|Open the file by the name|Open the file|Open file) (.+)"
    # (Open the|Open) (.+) (?:file and edit.|file for editing.|file.)"
    match_open_file = re.search(pattern_open_file, input_text, re.IGNORECASE)

    if match_create_file:
        # Folder name is optional, so check if it's present
        folder_name = match_create_file.group(1).strip() if match_create_file.group(1) else '.'

        # File name is mandatory and always present
        file_name = match_create_file.group(2).strip()

        create_file(file_name, folder_name)
        print(f"Uni: Created file named '{file_name}' in '{folder_name}'")
        # break
    elif match_add_context:
        # Extract file name and context from the matched pattern
        file_name = match_add_context.group(1).strip()
        context = match_add_context.group(2).strip()
        add_context(file_name, context)
        print(f"Uni: Added context to file named '{file_name}'")
        # break
    elif match_run_file:
        # Esecute code in file name from the matched pattern
        file_name = match_run_file.group(1).strip()
        run_file(file_name)
        print(f"Uni: Ran file named '{file_name}'")
        # break
    elif match_open_file:
        # Open file name from the matched pattern
        file_name = match_open_file.group(1).strip()
        print(f"Uni: Opening the file named '{file_name}'")
        open_file(file_name)
        # break
    else:
        answer = answer_question(input_text)
        print("Uni: ", answer)




