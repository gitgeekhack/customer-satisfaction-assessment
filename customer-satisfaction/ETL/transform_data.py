import pandas as pd

data = pd.read_csv("extracted_conversation.csv")  # read csv file

data = data.iloc[:, 1:]  # remove index first column
data.head()  # print first five rows

print(type(data))  # type of data
print(data.shape)  # shape of our data

print(data.isnull().sum())  # checking for null value
data.dropna(inplace=True)  # dropping null values

sorted_df = data.sort_values(by='created_at', ascending=True)  # sort whole dataframe
sorted_df.sort_index()  # sort_index of dataframe
sorted_df.to_csv('transformed_conversation.csv')  # saving in csv file
