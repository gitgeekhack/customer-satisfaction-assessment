import pandas as pd

data = pd.read_csv("transformed_conversation.csv")  # read csv file
data = data.iloc[:, 1:]

thread_ids_index = []
count = 0
length = len(data)
temp_idx = -1

for i in range(length):
    for j in range(temp_idx + 1, length):
        if len(thread_ids_index) == 0:
            thread_ids_index.append(j)
        else:
            if data['thread_id'][j] == data['thread_id'][thread_ids_index[0]]:
                thread_ids_index.append(j)
            else:
                for k in range(len(thread_ids_index)):
                    if data['created_by'][thread_ids_index[k]] == 'Customer':
                        count = 1
                        break
                    else:
                        count = 0
                if count == 0:
                    temp = data['thread_id'][thread_ids_index[0]]
                    temp_idx = thread_ids_index[-1]
                    thread_ids_index.clear()
                    data.drop(data.index[data['thread_id'] == temp], inplace=True)
                    break
                else:
                    temp_idx = thread_ids_index[-1]
                    thread_ids_index.clear()
                    break

data.to_csv('Cleaned.csv')
