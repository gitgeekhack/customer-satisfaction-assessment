from transformers import DistilBertTokenizer, TFDistilBertModel
from tensorflow import keras, Graph
from keras import backend as K
import tensorflow as tf
import numpy as np
from app.common.utils import MonoState


# load sentiment analysis model
def load_model():
    print("Loading Model")
    # init distilbert model
    distilbert_model = TFDistilBertModel.from_pretrained('distilbert-base-uncased')

    thread_graph = Graph()
    with thread_graph.as_default():
        thread_session = K.get_session()
        with thread_session.as_default():
            fine_tune_model = keras.models.load_model('app/model/sentiment-analysis.h5',
                                                      custom_objects={'TFDistilBertModel': distilbert_model})
            graph = tf.compat.v1.get_default_graph()
    return [fine_tune_model, graph, thread_session]


def tokenize(sentences, tokenizer):
    input_ids, input_masks = [], []
    for sentence in sentences:
        inputs = tokenizer.encode_plus(sentence, add_special_tokens=True, max_length=128, truncation=True,
                                       pad_to_max_length=True, return_attention_mask=True,
                                       return_token_type_ids=True)
        input_ids.append(inputs['input_ids'])
        input_masks.append(inputs['attention_mask'])

    return np.asarray(input_ids, dtype='int32'), np.asarray(input_masks, dtype='int32')


class SentimentPredictor(MonoState):
    _internal_state = {'model': load_model()}

    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

    # define tokenize function that tokenize sentences and converting them into tensors
    def predict(self, sentences):
        # tokenize the data
        test = tokenize(sentences, self.tokenizer)
        model, graph, session = self.model
        # predict messages
        with graph.as_default():
            with session.as_default():
                predicted_value = model.predict([test[0], test[1]])
        confidence = [x[np.argmax(x)] for x in predicted_value]
        predicted_labels = [tf.argmax(x.reshape(1, -1), axis=1).numpy()[0] for x in predicted_value]

        return confidence, predicted_labels
