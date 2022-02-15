import pandas as pd

df = pd.read_csv('threads_ids.csv')

print(df.head())

# # threads = set(df['thread_id'].tolist())
#
# threads = df['thread_id'].unique()
# print(type(threads))
# print(len(threads))
#
# thrd = pd.DataFrame(threads, columns=['thread_id'])
# thrd.to_csv('threads_ids.csv')