# autoApply
A bot that will apply to job for yourself on Welcome to the jungle 
https://www.welcometothejungle.com/

To understand the bot and how it works first read all the README file.

## 📘 Summary

- [Welcome to the jungle Requirements](#welcome-to-the-jungle-requirements)
- [Code Requirements](#code-requirements)
- [How to use it](#how-to-use-it)
- [Features](#features)
- [List of questions files](#list-of-questions-files)
- [Discord webhook](#discord-webhook)
- [Configuration file](#configuration-file)
- [Cover letter generation](#cover-letter-generation)
- [Warnings](#warnings)
- [Disclaimers](#disclaimers)

## Welcome to the jungle Requirements
You need to have a working welcome to the jungle account accessible via email + password for login.

Your account must have all the main information filled: First name, last name, telephone number, resume file and LinkedIn otherwise the bot won't be able to apply.

If those info aren't filled go here:
https://www.welcometothejungle.com/fr/me/profile

## Code Requirements

To make the code work you need to have python and pip installed in your computer and you must have the latest version of google chrome otherwise the code won't run

Link to download python: https://www.python.org/downloads/

Link to download pip: https://pip.pypa.io/en/stable/installation/

Link to download google chrome: https://www.google.com/intl/fr_fr/chrome/ 

You also need to do 8 discord webhook to recieve all the info inside discord and put the webhook url in discordWebhookUrl.txt

Here is how to do a discord webhook: https://www.svix.com/resources/guides/how-to-make-webhook-discord/

Download all the modules required for the bot to work using this command:

```bash
    pip install -r requirements.txt
```

## How to use it 
Add the text of your resume inside resume_text.txt and fill the configuration.yml file

On your first use you need to do 

```bash
    python main.py --questions
```
It will go through a lot of job offer and get all the questions each job offer is asking and writing them inside list_of_questions.txt file.

After the first run you can use the bot like this:

```bash
    python main.py
```
Or still do:
```bash
    python main.py --questions
```
to add more question to the list_of_questions.txt file

## Features
- The bot can work in any language
- After the first login it uses cookies to avoid reloging every time you use it 
- The bot search through offer based on the info of the configuration.yml file
- It send all the link offer to discord in 2 separates channel:             
  - job offer where you can apply directly on welcome to the jungle
  - job offer where you need to apply on another website   
- The bot can apply to job inside welcome to the jungle
- It can answer to question based on the answer you put on the list_of_questions.txt file
- It can generate a cover letter by scraping chatgpt and asking him to generate it with using the job offer text and the text of your resume

## List of questions files

The list_of_questions.txt file is one of the key file/feature of this bot.

It's storing all the questions jobs offer are asking.

The goal of it is to be able to answer to all the questions job offer are asking.

You only need to answer once to the question then the bot will always put the answer you delivered if the same question is asked on another job offer

To answer a question just put a space and your answer after the ##### like this:
```text
    Do you know python ?##### Yes I do
```

Inside the file there is 3 types of answer like in the picture:
<img width="405" height="522" alt="image" src="https://github.com/user-attachments/assets/424c04d6-b2b6-4349-83f1-c8b482b822b8" />

* Questions where you know the answer so just answer it
* Questions where you don't know the answer but you want to see the job offer to answer it. In this case just don't write anything and on the next run the bot will send you a discord message with the link of the job offer so you will be able to read the offer text and add the answer of the question
* Questions where you don't want to answer eg: questions that aren't related to your field. If you don't want to answer to this question just put " skip" after ##### like this:
```text
have you built a python service with asyncio that applies backpressure?##### skip
```
If you put skip the bot won't apply to the job offer and he will just send you a discord message with the job offer url so you can still see it

During the run if the bot see a new question that isn't inside the list_of_questions.txt file the bot won't apply to the offer and he will send you a discord message telling you that you need to answer to the question.
After you answer to the specific question the bot will be able to apply to this offer on the next run.

## Discord webhook
In order to have all the right information available anywhere I decided to put them on several discord channels using discord webhook like this:
<img width="421" height="514" alt="image" src="https://github.com/user-attachments/assets/baa82429-b761-4fda-95d2-3baf5c27e3ef" />

* Statistics: This channel will put the number of job offer found and the number of apply the bot did
* Job inside welcome to the jungle: This channel will put all the job offer url where you can directly apply into welcome to the jungle
* Job outside welcome to the jungle: This channel will put all the job offer url where you need to apply on another website outside welcome to the jungle
* Job banned: This channel will put all the offer where the bot didn't applied because they were a forbiden word inside job offer text/question or because the user set skip_question or skip_cover_letter to false inside the configuration.yml file
* Job error: This channel will put all the offer  where the bot didn't applied because an error happend
* Job applied succes: This channel will put all the offer where the bot applied well
* New question to answer: This channel will put all the job offer where you need to answer the question and the question you need to answer too
* Cover letter:  This channel will print the cover letter generated and link of the job offer
You can name each of the 8 channels whatever you want but you should put easy to understand name

## Configuration file 
This file is important because it's where all your login info and filter are.

I will explain  the key feature of the file:
* job_keyword_list
```bash
# Job keyword list (terms used to find / filter job offers)

job_keyword_list:
  - "developpeur python"
  - "ingénieur logiciel python"
  - "développeur backend"
  - "développeur frontend"
  - "développeur fullstack"
```
job_keyword_list contain all the "job name" you are looking for.

The bot will loop through each of them to search job and apply
* Apply

```bash
# If this is set to False the bot will only send job url to discord and won't apply

apply: True
````
If apply is set to False the bot will only look through offer and send the url of the offer to discord channel otherwise if it's set to True the bot will apply and send the url of the offer to discord channel

* apply_to_offer_who_have_job_keyword_list_element_in_their_name
```bash
# If this is set to true the bot will only apply to job that got job_keyword_list inside the job offer name

apply_to_offer_who_have_job_keyword_list_element_in_their_name: False
````
If the apply_to_offer_who_have_job_keyword_list_element_in_their_name is set to True the bot will only apply to offer who got job_keyword_list element inside their name.

Exemple: if your job_keyword_list is composed of "frontend developer" and "backend developer" and the job offer name is "java developer" then the bot won't apply to it because "java developer" is not inside job_keyword_list 

If the offer name is "react frontend developer"
the bot will apply because inside the name there is "frontend developer" which is inside your job_keyword_list

* skip_question
```bash
# If this is set to true the bot won't apply to an offer where a question is needed

skip_question: False
```
If skip_question is set to True the bot won't apply to job offer where questions are required and he will just send the job offer url to discord
* skip_cover_letter
```bash
# If this is set to true the bot won't apply to an offer where a cover letter is needed

skip_cover_letter: False
```
If skip_cover_letter is set to True the bot won't apply to job offer where a cover_letter is required and he will just send the job offer url to discord

* forbiden_words_job_offer_question
```bash
# If those words are in the question of the offer the bot won't apply

forbiden_words_job_offer_question:
  - "devops"
````

If forbiden_words_job_offer_question contains certain words and those words appear inside the question section of a job offer (for example, a question like "Do you have experience in DevOps?"), the bot will skip the application and only send the job offer URL to the Discord channel


* forbiden_words_job_offer_text
```bash
# If those words are in the text of the offer the bot won't apply

forbiden_words_job_offer_text:
  - "java"
```

If any word listed under forbiden_words_job_offer_text is found in the job description text, the bot will skip the application and only send the job offer URL to the Discord channel

## Cover letter generation

To generate the cover letter the bot will scrap into chatgpt and generate the cover letter with all your resume information inside resume_text.txt file and the description of the job offer. 

It will also add the language of the cover letter and it's lenght based off the info you put on the configuration.yml file

If you want to see example of cover letter just put print_cover_letter to True inside the configuration.yml file and the bot will send the cover letter and the link of the job offer to discord and he won't apply to the offer

Then if you like the cover letter generated by the bot just put back print_cover_letter to False

If any error happend during the generation of the cover letter the bot won't apply to the offer and send a discord message to tell you that the cover letter generation failed

## Warnings

I only tested the bot in french and english so it may not work on languages without latin alphabet

If any errors happend during the apply process don't worry the bot won't apply and just send the job offer url into discord

If the bot failed to launch or you see too many mistakes create an issues or dm me on my discord "sangokuhomer"

## Disclaimers

I made this bot for 2 purposes:
* Having a new project to add to my github and resume
* Time saving by auto applying for myself

This project is open source so fell free to modify as you wish the configuration.yml file to have the best jobs offer and fell free to update the code or even add more features to it.

I hope my bot will help you find more job

