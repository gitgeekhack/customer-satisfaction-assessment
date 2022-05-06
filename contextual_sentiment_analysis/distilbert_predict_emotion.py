import time
import pandas as pd
import numpy as np
from transformers import DistilBertTokenizer, TFDistilBertModel
from tensorflow import keras
import tensorflow as tf

data = pd.read_csv('pairs_emotion_detection.csv')


def tokenize(sentences, tokenizer):
    input_ids, input_masks = [], []
    for sentence in sentences:
        inputs = tokenizer.encode_plus(sentence, add_special_tokens=True, max_length=128, truncation=True,
                                       pad_to_max_length=True, return_attention_mask=True, return_token_type_ids=True)
        input_ids.append(inputs['input_ids'])
        input_masks.append(inputs['attention_mask'])

    return np.asarray(input_ids, dtype='int32'), np.asarray(input_masks, dtype='int32')


# load sentiment analysis model
def load_model():
    # init distilbert model
    distilbert = TFDistilBertModel.from_pretrained('distilbert-base-uncased')

    # load model with distilbert custom object
    loaded_model = keras.models.load_model(
        '/home/vivek/Files/customer-satisfaction-assesment-poc/model_training_app/model/sentiment-analysis.h5',
        custom_objects={'TFDistilBertModel': distilbert})
    return loaded_model

model = load_model()
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

def predict_sentiment(test):
    length = len(test)

    # tokenize the data
    test = tokenize(test, tokenizer)
    test_input_ids = test[0]
    test_attention_mask = test[1]

    predicted_value = model.predict([test_input_ids, test_attention_mask])

    # predict in whole dataset
    predicted_values = []
    for i in range(0, length):
        predicted_values.append(tf.argmax(predicted_value[i].reshape(1, -1), axis=1).numpy()[0])
    return predicted_values


x = time.time()
predicted_list = predict_sentiment(data['message'].tolist())
print(time.time() - x)

data['distil-result'] = predicted_list
data.to_csv('compare_models.csv', index=False)
