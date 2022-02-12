import pandas as pd

data = pd.read_csv("extract_conversation.csv")  # read csv file

data = data.iloc[:, 1:]  # remove index first column
data.head()

print(type(data))  # type of data
print(data.shape)  # shape of our data

print(data.isnull().sum())  # checking for null value
data.dropna(inplace=True)

sorted_df = data.sort_values(by='created_at', ascending=True)
sorted_df.sort_index()
sorted_df.to_csv('tranformed_conversation.csv')

ef remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())