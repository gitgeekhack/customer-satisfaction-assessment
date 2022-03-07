from nltk.tokenize import WhitespaceTokenizer  # tokenization of texts
import spacy  # lemmatization of texts


class PreProcessor:
    def __init__(self, dataframe):
        self.data_frame = dataframe
        self.data_frame.dropna(inplace=True)  # drop rows that have null values
        self.data_frame = self.data_frame.reset_index()  # reset the index for the dataframe
        self.data_frame = self.data_frame.iloc[:, 1:]

    def tokenize_texts(self):
        tokens = []  # list for storing tokenized Words
        length_data = len(self.data_frame)  # length of dataframe
        wst = WhitespaceTokenizer()
        for idx in range(length_data):
            tokens.append(wst.tokenize(self.data_frame['message'][idx]))
        self.data_frame['tokens'] = tokens  # add column of tokens
        return self.data_frame

    def lemmatize_texts(self):
        lemma_texts = []
        length_data = len(self.data_frame)  # length of dataframe
        spacy_obj = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        for idx in range(length_data):
            lemma_texts.append(
                [token.lemma_ for token in spacy_obj((self.data_frame['message'][idx])) if not token.is_punct])

        clean_list = []  # combining into one string
        for idx in range(len(lemma_texts)):
            clean_list.append(" ".join(lemma_texts[idx]))

        self.data_frame['lemma_texts'] = clean_list  # add columns for lemma_texts
        return self.data_frame
