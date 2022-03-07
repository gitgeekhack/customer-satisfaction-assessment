from data_preparation import ETL
from data_preprocessing import PreProcessor

# extract specific thread and detect emotion
files_path = "../data/dataset/8b8c697f82ce40e4a04138383676ef5a.json"  # path contains all the threads
etl_obj = ETL()  # initialize object of ETL

# extracting data from the threads
print("Extracting JSON data...")
data = etl_obj.extract_data(files_path)  # extracting data

print("Transforming data...")
data = etl_obj.transform_data(data)  # transformed data

preprocessor_obj = PreProcessor(data)  # initialize object of Preprocessor
print("Tokenizing a data...")
data = preprocessor_obj.tokenize_texts()

print("Lemmatizing a data...")
data = preprocessor_obj.lemmatize_texts()

print("Data Saved in CSV File.")
data.to_csv('../data/processed_files/processed_thread.csv', index=False)
