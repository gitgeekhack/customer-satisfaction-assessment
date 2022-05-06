import time
from transformers import pipeline
import pandas as pd


data = pd.read_csv('bert_emotion_detection.csv')

# BERT Model
model = pipeline('sentiment-analysis', model="finiteautomata/bertweet-base-sentiment-analysis")
x = time.time()
predicted_emotion = model(data['message'].tolist(), truncation=True)

roberta_emotion = []
roberta_confidence = []
for i in range(len(predicted_emotion)):
    fetched_label = predicted_emotion[i]['label']
    fetched_confidence = predicted_emotion[i]['score']
    if fetched_label == "LABEL_2":
        label = "Positive"
    elif fetched_label == "LABEL_0":
        label = "Negative"
    else:
        label = "Neutral"
    roberta_emotion.append(label)
    roberta_confidence.append(fetched_confidence)
print(time.time() - x)

data['roberta_emotion'] = roberta_emotion
data['roberta_confidence'] = roberta_emotion
data.to_csv('bert_emotion_detection.csv', index=False)


# # DistilBERT Model
#
# # define tokenize function that tokenize sentences and converting them into tensors
# def tokenize(sentences, tokenizer):
#     input_ids, input_masks = [], []
#     for sentence in sentences:
#         inputs = tokenizer.encode_plus(sentence, add_special_tokens=True, max_length=128, truncation=True,
#                                        pad_to_max_length=True, return_attention_mask=True, return_token_type_ids=True)
#         input_ids.append(inputs['input_ids'])
#         input_masks.append(inputs['attention_mask'])
#
#     return np.asarray(input_ids, dtype='int32'), np.asarray(input_masks, dtype='int32')
#
#
# # load sentiment analysis model
# def load_model():
#     # init distilbert model
#     distilbert = TFDistilBertModel.from_pretrained('distilbert-base-uncased')
#
#     # load model with distilbert custom object
#     loaded_model = keras.models.load_model(
#         '/home/vivek/Files/customer-satisfaction-assesment-poc/model_training_app/model/sentiment-analysis.h5',
#         custom_objects={'TFDistilBertModel': distilbert})
#     return loaded_model
#
#
# def predict_sentiment(test):
#     # define distilbert tokenizer
#     tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
#     length = len(test)
#     # call load_model for prediction
#     model = load_model()
#
#     # tokenize the data
#     test = tokenize(test, tokenizer)
#     test_input_ids = test[0]
#     test_attention_mask = test[1]
#
#     predicted_value = model.predict([test_input_ids, test_attention_mask])
#
#     # predict in whole dataset
#     predicted_values = []
#     for i in range(0, length):
#         predicted_values.append(tf.argmax(predicted_value[i].reshape(1, -1), axis=1).numpy()[0])
#     return predicted_values
#
#
# predicted_list = predict_sentiment(data['message'].tolist())
#
# x = time.time()
# data['distil-result'] = predicted_list
#
# data['distil-result'] = data['distil-result'].apply(
#     lambda x: "Positive" if x == 0 else ("Negative" if x == 1 else "Neutral"))
#
# print(time.time() - x)
# data.to_csv('compare_models.csv', index=False)
