import json
import pandas as pd

with open('Chat.json') as file:  # open 'Chat.json' as file
    data = json.load(file)  # load file data into data var


def extract_data_into_dataframe():
    extracted_list = []  # contains extracted attributes
    for item in data['hits']['hits']:  # iterate over the data list
        thread_id = item['_source']['thread_id']  # extract thread_id feature
        created_at = item['_source']['created_at']  # extract created_at feature
        try:
            message = item['_source']['message']  # extract message feature
            msg_data = json.loads(message)  # reload json message in msg_data
            msg = msg_data['text']  # extract key
        except KeyError:
            msg = None

        try:
            created_by = item['_source']['created_by']  # if id is there then we consider as bot
        except KeyError:
            created_by = None  # if id is not there then we consider as customer

        if created_by is None:
            agent = 'Customer'
        else:
            agent = 'Bot'

        extracted_list.append([thread_id, created_at, msg, agent])
        data_frame = pd.DataFrame(extracted_list, columns=['thread_id', 'created_at', 'message', 'created_by'])
        data_frame.to_csv("extract_conversation.csv")


extract_data_into_dataframe()
