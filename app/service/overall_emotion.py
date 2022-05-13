import pandas as pd


class OverallEmotion:
    def __init__(self, df):
        self.data_frame = df

    def prepare_adjacency_pair(self, dataframe):
        self.data_frame = dataframe
        messages = self.data_frame['message'].tolist()  # convert pandas series into the list

        # list that stores the adjacency pairs
        adj_pairs = []
        for idx in range(len(messages) - 1):
            adj_pairs.append(messages[idx] + " " + messages[idx + 1])  # prepare an adjacency pair

        adjacency_pair_df = pd.DataFrame()  # convert adjacency pairs into the dataframe
        adjacency_pair_df['message'] = adj_pairs
        return adjacency_pair_df

    def perform_arithmetic_average(self, emotion_count, dataframe):
        self.data_frame = dataframe
        total_positive_sequence = 0  # total of positive sequence number
        total_negative_sequence = 0  # total of negative sequence number
        total_neutral_sequence = 0  # total of neutral sequence number

        # sum the sequence number according to the class labels
        for i in range(len(self.data_frame)):
            if self.data_frame['final_result'][i] == 'Positive':
                total_positive_sequence += self.data_frame['sequence_number'][i]
            elif self.data_frame['final_result'][i] == 'Negative':
                total_negative_sequence += self.data_frame['sequence_number'][i]
            else:
                total_neutral_sequence += self.data_frame['sequence_number'][i]

        # if any labels class count has 0, then arithmetic average provides an ZeroDivision exception, Convert 0 into 1
        if emotion_count['Positive'] == 0:
            emotion_count['Positive'] = 1

        if emotion_count['Negative'] == 0:
            emotion_count['Negative'] = 1

        if emotion_count['Neutral'] == 0:
            emotion_count['Neutral'] = 1

        # perform arithmetic average
        avg_positive = total_positive_sequence / emotion_count['Positive']
        avg_negative = total_negative_sequence / emotion_count['Negative']
        avg_neutral = total_neutral_sequence / emotion_count['Neutral']

        # return label class, which has the highest average
        if (avg_positive > avg_negative) and (avg_positive > avg_neutral):
            return "Positive"
        elif (avg_negative > avg_positive) and (avg_negative > avg_neutral):
            return "Negative"
        else:
            return "Neutral"
