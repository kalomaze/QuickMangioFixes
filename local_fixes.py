import os
import sys
import time

def insert_new_line(file_name, line_to_find, text_to_insert):
    lines = []
    with open(file_name, 'r', encoding='utf-8') as read_obj:
        lines = read_obj.readlines()
    already_exists = False
    with open(file_name + '.tmp', 'w', encoding='utf-8') as write_obj:
        for i in range(len(lines)):
            write_obj.write(lines[i])
            if lines[i].strip() == line_to_find:
                # If next line exists and starts with sys.path.append, skip
                if i+1 < len(lines) and lines[i+1].strip().startswith("sys.path.append"):
                    print('Already fixed! Skipped adding a line...')
                    already_exists = True
                    break
                else:
                    write_obj.write(text_to_insert + '\n')
    # If no existing sys.path.append line was found, replace the original file
    if not already_exists:
        os.replace(file_name + '.tmp', file_name)
        return True
    else:
        # If existing line was found, delete temporary file
        os.remove(file_name + '.tmp')
        return False

def replace_in_file(file_name, old_text, new_text):
    with open(file_name, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    if old_text in file_contents:
        file_contents = file_contents.replace(old_text, new_text)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(file_contents)
            return True

    return False

if __name__ == "__main__":
    current_path = os.getcwd()
    file_name = 'extract_f0_print.py'
    line_to_find = 'import numpy as np, logging'
    text_to_insert = "sys.path.append(r'" + current_path + "')"

    success_1 = insert_new_line(file_name, line_to_find, text_to_insert)
    if success_1:
        print('The first operation was successful!')
    else:
        print('Skipped first operation as it was already fixed!')

    file_name = 'infer-web.py'
    old_text = 'with gr.Blocks(theme=gr.themes.Soft()) as app:'
    new_text = 'with gr.Blocks() as app:'

    success_2 = replace_in_file(file_name, old_text, new_text)
    if success_2:
        print('The second operation was successful!')

    if success_1 and success_2:
        print('Local fixes successful! You should now be able to infer and train locally on crepe RVC.')
    else:
        print("Local fixes didn't apply? You shouldn't be seeing this if you ran it in the correct folder. Otherwise, contact kalomaze#2983 in AI HUB")

    time.sleep(5)
