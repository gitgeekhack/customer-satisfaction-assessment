import json
import pandas as pd
from bs4 import BeautifulSoup  # for removing html contents
import re


class ETL:
    def __init__(self):
        self.data_frame = pd.DataFrame()

    # method for extract data from JSON file
    def extract_data(self, data):
        extracted_list = []  # contains extracted attributes
        for item in data['hits']['hits']:  # iterate over the data list
            try:
                created_by = item['_source']['created_by']  # if created_by has numeric value then we consider as bot
            except KeyError:
                created_by = None  # if created_by has None value then we consider as customer

            if created_by is None:
                agent = 'Customer'
            else:
                agent = 'Bot'

            try:
                message = item['_source']['message']
                msg_data = json.loads(message)  # reload json message in msg_data
                msg = BeautifulSoup(msg_data['text'], "lxml").text  # removing html contents
            except KeyError:
                msg = None

            extracted_list.append([agent, msg])  # appending all attributes in list
        self.data_frame = pd.DataFrame(extracted_list, columns=['created_by', 'message'])
        return self.data_frame

    def transform_data(self, dataframe):
        dataframe.dropna(inplace=True)  # dropping null values
        dataframe = dataframe.reset_index()  # reset_index of dataframe
        dataframe = dataframe.iloc[:, 1:]  # removing index

        # removing unwanted symbols and spaces
        for i in range(len(dataframe)):
            dataframe['message'][i] = re.sub('[^a-zA-Z0-9(+*) \n\.]', ' ', dataframe['message'][i])
            dataframe['message'][i] = re.sub("\s+", " ", dataframe['message'][i])

        self.data_frame = dataframe
        return self.data_frame

    def extract_customer_responses(self):
        self.data_frame.dropna(inplace=True)  # drop rows that have null values
        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]
        length = len(self.data_frame)

        for i in range(length):
            if self.data_frame['created_by'][i] != 'Customer':
                self.data_frame.drop(i, inplace=True)

        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]
        length_of_message = len(self.data_frame)
        return self.data_frame, length_of_message
