"""File that store all the global variables"""

# pylint: disable=C0103
# pylint: disable=C0301

accept_content_datatestid:str = "apply-form-consent"
accept_cookies_xpath:str = "/html/body/div[2]/div/div/div[1]/div[2]/button[3]"
apply_form_datatestid:str = "apply-form-modal"
apply_to_the_job_datatestid:str = "apply-form-submit"
apply_button_data_testid:str = "job_header-button-apply"
all_jobs_of_the_page_datatestid:str = "search-results-list-item-wrapper"
button_to_triger_login_page_datatestid:str = "not-logged-visible-login-button"
clear_localisation_datatestid:str = "clear-dropdown-search"
cover_letter_datatestid:str = "apply-form-field-cover_letter"
current_post_datatestid:str = "apply-form-field-subtitle"
discord_stat = 0
discord_job_inside = 1
discord_job_outside = 2
discord_job_banned = 3
discord_job_error = 4
discord_apply_sucess = 5
discord_question = 6
found_offer_datatestid:str = "search-results"
grid_view_xpath:str = "/html/body/div[1]/div/div/div/div[3]/div/div[2]/div[2]/div[2]/button[2]"
info_of_the_job_datatestid:str = "job-metadata-block"
job_page_url:str = "https://www.welcometothejungle.com/fr/jobs?query="
job_offer_localisation_datatestid:str = "jobs-home-search-field-location"
job_offer_first_localisation_xpath:str = "/html/body/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div[2]/div/p"
job_offer_question_xpath:str = "/html/body/div[17]/div[2]/div/section/form/fieldset[3]"
job_offer_question_xpath2:str = "/html/body/div[22]/div[2]/div/section/form/fieldset[3]"
job_offer_question_xpath3:str = "/html/body/div[18]/div[2]/div/section/form/fieldset[3]"
job_offer_question_xpath4:str = "/html/body/div[12]/div[2]/div/section/form/fieldset[3]"
job_offer_question_xpath5:str = "/html/body/div[13]/div[2]/div/section/form/fieldset[3]"
job_offer_question_xpath_list:list[str] = [job_offer_question_xpath,job_offer_question_xpath2,job_offer_question_xpath3,job_offer_question_xpath4,job_offer_question_xpath5]
job_offer_question_xpath_list_special_nb:list[str] = ["17","22","18","12","13"]
job_offer_text_xpath:str = "/html/body/div[1]/div/div/div/div/div[3]/section/div[4]/div/div[2]"
internship_job_url_typing:str = "&refinementList%5Bcontract_type%5D%5B%5D=internship&refinementList%5Bcontract_type%5D%5B%5D=apprenticeship"
localisation_of_the_job:str = "&aroundQuery="
login_button_email_datatestid:str = "login-field-email"
login_button_password_datatestid:str = "login-field-password"
login_button_submit_datatestid:str = "login-button-submit"
login_page_url:str = "https://www.welcometothejungle.com/fr/"
next_page_button_xpath:str = "/html/body/div[1]/div/div/div/div[3]/div/div[3]/div/div/nav/ul/li[9]/a/svg"
permanent_job_url_typing:str = "&refinementList%5Bcontract_type%5D%5B%5D=full_time&refinementList%5Bcontract_type%5D%5B%5D=temporary&refinementList%5Bcontract_type%5D%5B%5D=freelance"
profile_dissmiss_button_datatestid:str = "dismiss-profile-visibility-block"
question_in_several_language_list: str = [
    "question",       # English
    "frage",          # German
    "pregunta",       # Spanish
    "questione",      # Italian
    "question",       # French
    "pergunta",       # Portuguese
    "spørgsmål",      # Danish
    "vraag",          # Dutch
    "pytanie",        # Polish
    "вопрос",         # Russian
    "otázka",         # Czech
    "kysymys",        # Finnish
    "pytanie",        # Slovak (same as Polish)
    "domanda",        # Italian (alternative form)
    "ερώτηση",        # Greek
    "질문",            # Korean
    "質問",            # Japanese
    "问题",            # Chinese (Simplified)
    "سؤال",           # Arabic
    "सवाल",           # Hindi
    "வினா",           # Tamil
    "ప్రశ్న",          # Telugu
    "প্রশ্ন",          # Bengali
    "soru",           # Turkish
    "שאלה",           # Hebrew
    "sual",           # Azerbaijani
]
sort_by_date:str = "&sortBy=mostRecent"
sort_by_relevance:str = "&sortBy=mostRelevant"
view_more_text_datatestid:str = "view-more-btn"
wait_time:int = 10
wait_time2:int = 5
wait_time3:int = 15