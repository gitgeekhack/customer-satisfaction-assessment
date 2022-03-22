from data_preparation import ETL
from prepare_model import PrepareModel
import pandas as pd
import os

# extract all the threads and detect emotion
files_path_dataset1 = "../data/dataset1"  # path contains all the threads of dataset1
files_path_dataset2 = "../data/dataset2"  # path for dataset2
lst_dir = os.listdir(files_path_dataset1)  # list of thread name of dataset1
etl_obj = ETL()  # initialize object of ETL

# extracting data from the threads
print("Extracting dataset1...")
data = pd.DataFrame()
for i in range(len(lst_dir)):
    df = etl_obj.extract_data(files_path_dataset1 + "/" + lst_dir[i])  # extracting data
    data = pd.concat([data, df])  # concat data into dataframe

print("Extracting dataset2...")
data2 = etl_obj.extract_data("../data/dataset2/WOTNOT chat response.json")
data = pd.concat([data, data2])  # concat data into dataframe

print("Transforming data...")
data = etl_obj.transform_data(data)  # transformed data

print("Extracting Customer's responses from the data...")
data = etl_obj.extract_customer_responses()

# distinct message of the customer's responses.
msg_set = set(data['message'])
msg_list = list(msg_set)

# creating new dataframe
distinct_df = pd.DataFrame()
distinct_df['thread_id'] = list(data["thread_id"])
distinct_df['message'] = msg_list  # add column of message in the dataframe

print("Preparing Emotion Detection Model...")
model_obj = PrepareModel(data)  # initialize object of BuildModel

print("Predicting an Emotion...")
distinct_df = model_obj.predict_emotion

# print value counts of each labels
print(distinct_df['emotion'].value_counts())

print("Data Saved in CSV File.")
distinct_df.to_csv('../data/processed_files/all_threads_customer_data3.csv', index=False)
