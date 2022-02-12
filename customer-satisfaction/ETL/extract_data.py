import json
import pandas as pd
from bs4 import BeautifulSoup  # for removing html contents

with open('Chat.json') as file:  # open 'Chat.json' as file
    data = json.load(file)  # load file data into data var


def extract_data_into_dataframe():
    extracted_list = []  # contains extracted attributes
    for item in data['hits']['hits']:  # iterate over the data list
        thread_id = item['_source']['thread_id']  # extract thread_id feature
        created_at = item['_source']['created_at']  # extract created_at feature
        try:
            created_by = item['_source']['created_by']  # if created_by has numeric value then we consider as bot
        except KeyError:
            created_by = None  # if created_by has None value then we consider as customer

        if created_by is None:
            agent = 'Customer'
        else:
            agent = 'Bot'

        try:
            message = item['_source']['message']  # extract message feature
            msg_data = json.loads(message)  # reload json message in msg_data
            msg = BeautifulSoup(msg_data['text'], "lxml").text  # removing html contents
        except KeyError:
            msg = None

        extracted_list.append([thread_id, created_at, agent, msg])  # appending all features in list
        # prepare dataframe using list and columns
        data_frame = pd.DataFrame(extracted_list, columns=['thread_id', 'created_at', 'created_by', 'message'])
        data_frame.to_csv("extracted_conversation.csv")  # saving in csv file.


extract_data_into_dataframe()
