from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.constants import model_name

sentiment_pipeline = pipeline('sentiment-analysis', model=model_name)
sid_obj = SentimentIntensityAnalyzer()


class PrepareModel:
    def __init__(self, dataframe):
        self.data_frame = dataframe

    def predict_emotion(self):
        # get "vader" library scores
        vader_scores = []
        length = len(self.data_frame)
        for i in range(length):
            fetch_dict = get_vader_scores(self.data_frame['message'][i])  # fetching scores from vader
            vader_scores.append(fetch_dict)  # appending it into 'vader_scores' list

        # get "hugging face" library scores
        hugging_face_scores = sentiment_pipeline(list(self.data_frame['message']), truncation=True)

        # getting better emotion with higher confidence
        emotions = []
        confidence = []
        cnt_neg = cnt_pos = cnt_neu = 0
        for i in range(length):
            if vader_scores[i]['score'] > hugging_face_scores[i]['score']:  # check for higher confidence
                confidence.append(vader_scores[i]['score'])
                if vader_scores[i]['label'] == "POS":
                    emotions.append("Positive")
                    cnt_pos += 1
                elif vader_scores[i]['label'] == "NEG":
                    emotions.append("Negative")
                    cnt_neg += 1
                else:
                    emotions.append("Neutral")
                    cnt_neu += 1
            else:
                confidence.append(hugging_face_scores[i]['score'])
                if hugging_face_scores[i]['label'] == "POS":
                    emotions.append("Positive")
                    cnt_pos += 1
                elif hugging_face_scores[i]['label'] == "NEG":
                    emotions.append("Negative")
                    cnt_neg += 1
                else:
                    emotions.append("Neutral")
                    cnt_neu += 1

        emotion_count = {"Positive": cnt_pos, "Negative": cnt_neg, "Neutral": cnt_neu}
        self.data_frame['emotion'] = emotions
        self.data_frame['confidence'] = confidence
        return self.data_frame, emotion_count


# method that provides 'emotion' & 'confidence for vader
def get_vader_scores(sentence):
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
