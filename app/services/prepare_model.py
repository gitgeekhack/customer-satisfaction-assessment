import time
from app.services import sentiment_pipeline
from app.services import sid_obj


class PrepareModel:
    def __init__(self, dataframe):
        self.data_frame = dataframe

    def predict_emotion(self):
        # get "vader" library scores
        t1 = time.time()
        self.data_frame['vader_score'] = self.data_frame['message'].apply(lambda x: get_vader_scores(x))
        print("Vader Time : ", time.time() - t1)
        # get "hugging-face"  scores
        t2 = time.time()
        self.data_frame['hugging-face_score'] = sentiment_pipeline(self.data_frame['message'].tolist(), truncation=True)
        print("HuggingFace Time : ", time.time() - t2)

        t3 = time.time()
        abbr = lambda x: "Positive" if x == "POS" else ("Negative" if x == "NEG" else "Neutral")

        # getting better emotion with higher confidence
        self.data_frame['final_result'] = self.data_frame.apply(lambda x: abbr(x['vader_score']['label'])
            if x['vader_score']['score'] > x['hugging-face_score']['score']
            else abbr(x['hugging-face_score']['label']), axis=1)

        print("Comparison time: ", time.time() - t3)
        emotion_count = self.data_frame['final_result'].value_counts().to_dict()

        try:
            emotion_count['Negative']
        except KeyError:
            emotion_count['Negative'] = 0
        try:
            emotion_count['Positive']
        except KeyError:
            emotion_count['Positive'] = 0
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
