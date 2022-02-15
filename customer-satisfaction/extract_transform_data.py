import json
import pandas as pd
from bs4 import BeautifulSoup  # for removing html contents

def extract_data():
    with open('0e4dc114998a4ecabf64a1b7aaf07e01.json') as file:
        data = json.load(file)  # load file data into data var

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
        # data_frame.to_csv("extracted_conversation.csv", index=False)  # saving in csv file.
    return data_frame


def transform_data(data_frame):

    # data_frame = data.iloc[:, 1:]  # remove index first column
    # print(data_frame.head())  # print first five rows

    # print(type(data_frame))  # type of data
    # print(data_frame.shape)  # shape of our data

    # print(data_frame.isnull().sum())  # checking for null value
    data_frame.dropna(inplace=True)  # dropping null values

    sorted_df = data_frame.sort_values(by=['thread_id', 'created_at'], ascending=[True, True])  # sort whole dataframe
    sorted_df = sorted_df.reset_index()  # reset_index of dataframe
    sorted_df = sorted_df.iloc[:, 1:]
    # thread_ids_index = []
    # count = 0
    # length = len(sorted_df)
    # temp_idx = -1
    #
    # for i in range(length):
    #     for j in range(temp_idx + 1, length):
    #         if len(thread_ids_index) == 0:
    #             thread_ids_index.append(j)
    #         else:
    #             if sorted_df['thread_id'][j] == sorted_df['thread_id'][thread_ids_index[0]]:
    #                 thread_ids_index.append(j)
    #             else:
    #                 for k in range(len(thread_ids_index)):
    #                     if sorted_df['created_by'][thread_ids_index[k]] == 'Customer':
    #                         count = 1
    #                         break
    #                     else:
    #                         count = 0
    #                 if count == 0:
    #                     temp = sorted_df['thread_id'][thread_ids_index[0]]
    #                     temp_idx = thread_ids_index[-1]
    #                     thread_ids_index.clear()
    #                     data.drop(sorted_df.index[data['thread_id'] == temp], inplace=True)
    #                     break
    #                 else:
    #                     temp_idx = thread_ids_index[-1]
    #                     thread_ids_index.clear()
    #                     break
    sorted_df.to_csv('transformed_data.csv', index=False)
    return sorted_df

# Driver Code

df = extract_data()
cleaned_df = transform_data(df)


