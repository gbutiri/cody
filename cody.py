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






import code_functions
import patterns
import qa_functions as qa


###        --- OPEN THE FILE ---        ###

def open_file(file_name):

    while True:

        file_input_text = input("\n\nFile Contents: ")

        if file_input_text.lower() == 'close the file':
            print(f"Closing the file {file_name} Goodbye!")
            break

        # Detect line number match and indentation specifications.
        line_number = patterns.match_line_number(file_input_text)
        indent = patterns.match_indentation(file_input_text)
        
        
        
        # CODE MATCHES
        
        # Declare variable
        match = patterns.match_variable_declaration(file_input_text)
        if match:

            variable_type = patterns.match_variable_type(file_input_text)

            executed_code = code_functions.insert_variable_at_line(file_name, match, variable_type, line_number, indent)
            
            # Verify if variable was declared.
            test = qa.verify_variable_insertion_at_line(file_name, executed_code, line_number)
            
            if test:
                print(f"Your variable '{match}' of '{variable_type}' type was created on line #{line_number}")
            else:
                print("Uni: I was unable to test the creation of the variable.")

        # Add a simple loop
        match = patterns.match_loop_pattern(file_input_text)
        if match:

            item, items = patterns.match_loop_items(file_input_text)

            print("Got: item:", item, ", items:" , items, ", line number:", line_number, ", indent:", indent)
            code_functions.insert_loop_code_at_line(file_name, item, items, line_number, indent)

        # Add a conditional IF
        match = patterns.match_conditional(file_input_text)
        if match:
        
            var_one, operator, var_two = patterns.match_conditional_items(file_input_text)
            print("Got: var_one:", var_one, ", operator:" , operator, ", var_two:" , var_two, ", line number:", line_number, ", indent:", indent)

            code_functions.insert_conditional_code_at_line(file_name, var_one, operator, var_two, line_number, indent)

            print(f"Uni: Added for loop code at the end of the file: '{file_name}'")

        # Remove one line of code
        match = patterns.match_remove_lines(file_input_text)
        if match:
            
            code_functions.remove_code_at_line(file_name, match)
            
        # Remove multiple lines of code.
        match = patterns.match_remove_multi_lines(file_input_text)
        if match:
            
            line_start, line_end = get_remove_multi_lines(file_input_text)
            code_functions.remove_code_between_lines(file_name, line_start, line_end)
            
        # Add a blank line.
        match = patterns.match_add_blank_line(file_input_text)
        if match:
        
            code_functions.add_blank_line_at_line(file_name, match)
        
        # Add a comment line.
        match = patterns.match_add_comment_line(file_input_text)
        if match:
            
            line_number, comment = patterns.match_comment_context(file_input_text)
            code_functions.add_comment_at_line(file_name, line_number, comment)
        
        # Create a function
        match = patterns.match_create_function(file_input_text)
        if match:
            
            parameters = patterns.match_function_parameters(file_input_text)
            
            code_functions.ceate_function(file_name, match, parameters, line_number, indent)


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




