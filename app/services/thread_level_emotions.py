import pandas as pd
import json
from bs4 import BeautifulSoup  # for removing html contents
import os
from prepare_model import PrepareModel

files_path = "../data/dataset1"  # path contains all the threads
lst_dir = os.listdir(files_path)  # list of thread name

customer_responses = [None] * len(lst_dir)
thread_ids = [None] * len(lst_dir)


def extract_data(file_path):
    customer_response = ""
    with open(file_path) as file:
        data = json.load(file)  # load file data into data var
    for item in data['hits']['hits']:  # iterate over the data list
        thread_id = item['_source']['thread_id']
        try:
            created_by = item['_source']['created_by']  # if created_by has numeric value then we consider as bot
        except KeyError:
            created_by = None  # if created_by has None value then we consider as customer

        if created_by is None:
            try:
                message = item['_source']['message']  # extract message feature
                msg_data = json.loads(message)  # reload json message in msg_data
                msg = BeautifulSoup(msg_data['text'], "lxml").text  # removing html contents
                customer_response += msg + " "
            except KeyError:
                pass

    return customer_response, thread_id


print("Extracting threads from JSON and Clubbing Customer's responses...")
for i in range(len(lst_dir)):
    customer_responses[i], thread_ids[i] = extract_data(files_path + '/' + lst_dir[i], i)

data = pd.DataFrame()  # creating empty list
data['thread_id'] = thread_ids  # add thread_id column
data['message'] = customer_responses  # add customer's response column

print("Preparing Emotion Detection Model...")
model_obj = PrepareModel(data)  # initialize object of BuildModel

print("Training of Model...")
data = model_obj.predict_emotion

# print value counts of each labels
print(data['emotion'].value_counts())

print("Data Saved in CSV File.")
data.to_csv('../data/processed_files/thread_level_emotions_data.csv', index=False)
