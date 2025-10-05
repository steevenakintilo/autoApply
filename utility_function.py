"""File that handle utility functions"""
import pickle
from discord_webhook import DiscordWebhook
from unidecode import unidecode

def write_into_file(path:str, data:str) -> None:
    """Write data into a file"""
    with open(path, "ab") as f:
        f.write(str(data).encode("utf-8"))

def reset_file(path:str) -> None:
    "Reset a file"
    f = open(path, "w",encoding="utf8")
    f.write("")
    f.close()     

def print_file_content(path:str) -> str:
    "Print the content of a file"
    f = open(path, 'r',encoding="utf-8")
    content = f.read()
    f.close()
    return content

def print_pkl_file_content() -> str:
    """Print the content of a pkl file"""
    file_path = "cookies.pkl"
    with open(file_path, 'rb') as file:
        try:
            content = pickle.load(file)
        except:
            return ""
    return content

def convert_list_to_correct_url_typing(words:list[str]) -> str:
    "Converting a list of words to the correct typing of welcome to the jungle job search url"
    list_of_words = words.split(" ")
    correct_string = ""

    for word in list_of_words:
        correct_string+="%20"+word

    return correct_string

def remove_doublon_from_list_of_question_file() -> None:
    """Removing lines that are present several time on the list_of_questions.txt file"""
    question_file_with_only_text = print_file_content("list_of_questions.txt").replace("#####","").replace("?","").lower().split("\n")
    question_file = print_file_content("list_of_questions.txt").lower().split("\n")
    list_of_lines = []
    reset_file("list_of_questions.txt")
    for i , text in enumerate(question_file_with_only_text):
        if text.lower() not in list_of_lines:
            list_of_lines.append(text.lower())
            write_into_file("list_of_questions.txt",question_file[i]+"\n")

def send_message_discord(msg:str,weebhook_nb:int=0) -> None:
    """Send a message to a discord server using weebhook"""
    # nb = 0 for statistics
    # nb = 1 for job inside welcome to the jungle
    # nb = 2 for job outside welcome to the jungle
    # nb = 3 for job banned word inside offer
    # nb = 4 for job apply error
    # nb = 5 for job apply success
    # nb = 6 for new questions

    discord_url = print_file_content("discordWebhookUrl.txt").split("\n")
    try:
        webhook = DiscordWebhook(url=discord_url[weebhook_nb], content=msg)
        webhook.execute()
    except IndexError:
        pass

def get_answer_from_question_list(question_to_search:str) -> str:
    """Get the right answer to the question from the list_of_questions.txt file"""
    list_of_questions_found:list[str] = print_file_content("list_of_questions.txt").lower().split("\n")
    question_to_search = question_to_search.lower()
    for question in list_of_questions_found:
        if question_to_search in question:
            if question.split("#####")[1][0] == " ":
                return question.split("#####")[1][1:]
            return question.split("#####")[1]
    return ""

def are_words_inside_list_of_words(text,list_of_text) -> bool:
    """Check if words are inside a list of words"""
    list_ = []
    word_inside = False
    text = text.replace("-","")
    for txt in (list_of_text):
        words = unidecode(txt).split(" ")
        for word in words:
            if word.lower().replace("-","") in unidecode(text).replace("-","").lower():
                list_.append(word.replace("-",""))

        if " ".join(list_).lower().strip().replace("-","") == unidecode(txt).lower().strip().replace("-",""):
            word_inside = True
        list_ = []

    return word_inside
