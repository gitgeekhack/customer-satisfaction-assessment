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
        agent = ""
        for item in data["hits"]["hits"]:
            try:
                if item["_source"]["created_by"] is None:
                    agent = "Customer"
                else:
                    agent = "Bot"
            except KeyError:
                pass

            try:
                message = item["_source"]["message"]
                msg_data = json.loads(message)  # reload json message in msg_data
                msg = BeautifulSoup(msg_data["text"], "lxml").text  # removing html contents
            except KeyError:
                msg = None

            extracted_list.append([agent, msg])  # appending all attributes in list
        self.data_frame = pd.DataFrame(extracted_list, columns=["created_by", "message"])
        return self.data_frame

    def transform_data(self, dataframe):
        dataframe.dropna(inplace=True)  # dropping null values
        dataframe = dataframe.reset_index()  # reset_index of dataframe
        dataframe = dataframe.iloc[:, 1:]  # removing index
        self.data_frame = dataframe

        # removing unwanted symbols or bullets
        self.data_frame['message'] = self.data_frame['message'].apply(lambda x: re.sub('[^a-zA-Z0-9(+*) \n\.]', ' ', str(x)))
        self.data_frame['message'] = self.data_frame['message'].apply(lambda x: re.sub("\s+", " ", str(x)))
        return self.data_frame

    def extract_customer_responses(self):
        self.data_frame.dropna(inplace=True)  # drop rows that have null values
        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]  # removing index column
        self.data_frame = self.data_frame[self.data_frame['created_by'] == 'Customer']
        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]  # removing index column
        return self.data_frame
