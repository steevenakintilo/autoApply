"""File that handle utility functions"""

import pickle

def write_into_file(path, x):
    """Write data into a file"""
    with open(path, "ab") as f:
        f.write(str(x).encode("utf-8"))

def reset_file(path):
    "Reset a file"
    f = open(path, "w",encoding="utf8")
    f.write("")
    f.close()        

def print_file_content(path):
    "Print the content of a file"
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return(content)

def print_pkl_file_content():
    """Print the content of a pkl file"""
    file_path = "cookies.pkl"
    with open(file_path, 'rb') as file:
        try:
            content = pickle.load(file)
        except:
            return ""
    return content

def convert_list_to_correct_url_typing(words):
    "Converting a list of words to the correct typing of welcome to the jungle job search url"
    list_of_words = words.split(" ")
    correct_string = ""

    for word in list_of_words:
        correct_string+="%20"+word

    return correct_string
