import os
import requests
import schedule
import random
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BOT_SETTINGS = {
    "TOKEN": os.getenv("BOT_TOKEN", ""),
    }

GOOGLE_API_CREDENTIALS = {
    "type": "service_account",
    "project_id": "bot-ekaterina",
    "private_key_id": "9619e65c3bd6f5998927da848513cc37e22039cc",
    "private_key": os.getenv("GOOGLE_KEY", ""),
    "client_email": "bot-ekaterina@bot-ekaterina.iam.gserviceaccount.com",
    "client_id": "104806137571143810652",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bot-ekaterina%40bot-ekaterina.iam.gserviceaccount.com"
    }

TEST_ROM = {
    "NAME": "KateWhiteTeacher_Roomtest",
    "ID": "-1001332357265",
    }
PROD_ROM = {
    "NAME": "KateWhiteTeacher",
    "ID": "-477351197",
    }


def get_spreadsheet_records(filename, sheetname):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
                GOOGLE_API_CREDENTIALS,
                scope)
    #
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(filename).worksheet(sheetname)

    return sheet.get_all_records()


def get_quiz_from_spreadsheet(options_num=4):
    """
    Generate a quiz dictionary taking the data from a google spreadsheet
    """
    quiz = {}
    column_question = "English"
    column_answer = "Translation"

    # Get records from spreadsheet
    records = get_spreadsheet_records('BotWords', 'Quiz')
    print("SPREASHEET ALL RECORDS:", records)
    # Get a pool of records that are shuffled
    record_set = random.sample(records, k=options_num)
    # Get a random number whicit will be the quiz question
    record_index = random.randrange(0, options_num-1)

    quiz['correct_option_id'] = str(record_index)
    quiz['question'] = record_set[record_index][column_question]
    quiz['options'] = [a[column_answer] for a in record_set]
    return quiz


def bot_send_text(chat_id, bot_message):
    bot_token = BOT_SETTINGS["TOKEN"]
    bot_chatID = chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    print(response.text)
    return response


def bot_send_poll(chat_id, bot_question, bot_options, bot_correct_option_id, type="quiz"):
    bot_token = BOT_SETTINGS["TOKEN"]
    bot_chatID = chat_id

    # Build the query
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendPoll?chat_id=' + bot_chatID + '&question=' + bot_question + '&options=' + json.dumps(bot_options) + '&correct_option_id=' + str(bot_correct_option_id) + '&type=' + type

    # Send the query and get the answer
    response = requests.get(send_text)

    print(response.text)
    return response


def quiz(room_settings):
    quiz = get_quiz_from_spreadsheet()
    print("QUIZ", quiz)

    msg = "------- Daily Quiz Game --------------\n"
    msg += "📣🔔 Welcome to WhiteKate group 👩‍🏫\n"
    msg += "-------------------------------------\n"
    msg += "Can you guess the correct Russian translation of ( %s )" % (quiz['question'])

    bot_send_poll(room_settings["ID"],
                  msg,
                  quiz['options'],
                  quiz['correct_option_id'])


if __name__ == '__main__':
    env = os.getenv('ENV', "TEST")
    room = ""
    if env == "TEST":
        room = TEST_ROM
    elif env == "PROD":
        room = PROD_ROM
    else:
        print("Wrong ENV variable %s" % (env))
        exit()

    schedule.every().day.at("15:50").do(quiz, room)

    while True:
        schedule.run_pending()
