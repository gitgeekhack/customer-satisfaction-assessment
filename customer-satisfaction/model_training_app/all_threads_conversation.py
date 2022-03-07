from data_preparation import ETL
from train_model import BuildModel
import pandas as pd
import os

# extract all the threads and detect emotion

files_path = "../data/dataset"  # path contains all the threads
lst_dir = os.listdir(files_path)  # list of thread name
etl_obj = ETL()  # initialize object of ETL

# extracting data from the threads
print("Extracting JSON data...")
data = pd.DataFrame()
for i in range(len(lst_dir)):
    df = etl_obj.extract_data(files_path + "/" + lst_dir[i])  # extracting data
    data = pd.concat([data, df])  # concat data into dataframe

print("Transforming data...")
data = etl_obj.transform_data(data)  # transformed data

print("Extracting Customer's responses from the data...")
data = etl_obj.extract_customer_responses()

# distinct message of the customer's responses.
msg_set = set(data['message'])
msg_list = list(msg_set)

# creating new dataframe
distinct_df = pd.DataFrame()
distinct_df['message'] = msg_list  # add column of message in the dataframe
print("Preparing Emotion Detection Model...")
model_obj = BuildModel(distinct_df)  # initialize object of BuildModel

print("Training of Model...")
distinct_df = model_obj.train_and_predict()

# print value counts of each labels
print(distinct_df['emotion'].value_counts())

print("Data Saved in CSV File.")
distinct_df.to_csv('../data/processed_files/all_threads_customers_data.csv', index=False)
