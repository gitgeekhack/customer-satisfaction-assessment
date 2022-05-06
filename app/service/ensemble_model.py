from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app.service.prepare_distilbert_model import SentimentPredictor
import time

vader_obj = SentimentIntensityAnalyzer()  # init vader object
distilbert_obj = SentimentPredictor()  # init distilbert predictor object


class EnsembleModel:
    def __init__(self, dataframe):
        self.data_frame = dataframe

    def ensemble_predicted_emotion(self):
        # get "vader" library scores
        self.data_frame['vader_score'] = self.data_frame['message'].apply(lambda x: get_vader_scores(x))

        x = time.time()
        # get distilbert results
        distilbert_confidence, distilbert_labels = distilbert_obj.predict(self.data_frame['message'].tolist())
        self.data_frame['distilbert_confidence'] = distilbert_confidence
        self.data_frame['distilbert_labels'] = distilbert_labels

        print("Predicting time : {}".format(time.time() - x))

        # converting abbreviations like 'Positive', 'Negative'
        abbr = lambda x: "Positive" if x == 0 else ("Negative" if x == 1 else "Neutral")

        # ensemble for getting better emotion with higher confidence
        self.data_frame['final_result'] = self.data_frame.apply(lambda x: abbr(x['vader_score']['label'])
        if x['vader_score']['score'] > x['distilbert_confidence']
        else abbr(x['distilbert_labels']), axis=1)

        # creating by default keys and initialize with 0
        emotion_count = dict.fromkeys(['Positive', 'Negative', 'Neutral'], 0)

        # converting final_result of emotion count into dictionary
        result_count = self.data_frame['final_result'].value_counts().to_dict()

        # filling emotion_count dictionary from the result_count dictionary
        for key in result_count.keys():
            emotion_count[key] = result_count[key]

        return self.data_frame, emotion_count


# method that provides 'emotion' & 'confidence of vader library
def get_vader_scores(sentence):
    sentiment_dict = vader_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05:
        confidence = sentiment_dict['pos']
        emotion_dict = {'label': 0, 'score': confidence}
    elif sentiment_dict['compound'] <= -0.05:
        confidence = sentiment_dict['neg']
        emotion_dict = {'label': 1, 'score': confidence}
    else:
        confidence = sentiment_dict['neu']
        emotion_dict = {'label': 2, 'score': confidence}
    return emotion_dict
