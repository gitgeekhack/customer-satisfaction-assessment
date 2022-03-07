from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


class BuildModel:
    def __init__(self, dataframe):
        self.data_frame = dataframe
        self.data_frame.dropna(inplace=True)  # drop rows that have null values
        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]

    def train_and_predict(self):
        # get "vader" library scores
        vader_scores = []
        length = len(self.data_frame)
        for i in range(length):
            fetch_dict = get_vader_scores(self.data_frame['message'][i])  # fetching scores from vader
            vader_scores.append(fetch_dict) # appending it into 'vader_scores' list

        # get "hugging face" library scores
        sentiment_pipeline = pipeline('sentiment-analysis', model="finiteautomata/bertweet-base-sentiment-analysis")
        hugging_face_scores = sentiment_pipeline(list(self.data_frame['message']))

        # getting better emotion with higher confidence
        emotions = []
        confidence = []
        for i in range(length):
            if vader_scores[i]['score'] > hugging_face_scores[i]['score']: # check for higher confidence
                emotions.append(vader_scores[i]['label'])
                confidence.append(vader_scores[i]['score'])
            else:
                emotions.append(hugging_face_scores[i]['label'])
                confidence.append(hugging_face_scores[i]['score'])

        self.data_frame['emotion'] = emotions
        self.data_frame['confidence'] = confidence
        return self.data_frame


# method that provides 'emotion' & 'confidence for vader'
def get_vader_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05:
        confidence = sentiment_dict['pos']
        emotion_dict = {'label': 'POS', 'score': confidence}
    elif sentiment_dict['compound'] <= -0.05:
        confidence = sentiment_dict['neg']
        emotion_dict = {'label': 'NEG', 'score': confidence}
    else:
        confidence = sentiment_dict['neu']
        emotion_dict = {'label': 'NEU', 'score': confidence}
    return emotion_dict
