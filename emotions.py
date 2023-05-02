import pandas as pd
import numpy as np
import spacy
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import Poem_Emotions

# constants
nlp_fr = spacy.load('fr_core_news_md')
emotions = ['joy', 'fear', 'sadness', 'anger', 'surprise', 'disgust']

def main():
    pass

def fr_preprocess_emotions_df(feel_df):
    # preprocess feel df, change polarity to numerical values
    # and lemmatize all individual tokens
    feel_df.loc[feel_df['polarity'] == "positive", 'polarity'] = 1
    feel_df.loc[feel_df['polarity'] == "negative", 'polarity'] = -1

    feel_df_multiple = feel_df[(feel_df['word'].str.split().apply(len)) > 1]
    feel_df_single = feel_df[(feel_df['word'].str.split().apply(len)) == 1]
    feel_df_single['word'] = feel_df_single['word'].apply(lambda x: nlp_fr(x)[0].lemma_)
    return pd.concat(feel_df_single, feel_df_multiple)

def fr_create_phrase_tokenizer(feel_df, mwe_tokenizer):
    feel_df_multiple = feel_df[(feel_df['word'].str.split().apply(len)) > 1]

    # add all multi-word phrases in FEEL to tokenizer corpus
    for row in feel_df_multiple['word']:
        mwe_tokenizer.add_mwe(row.split())
    return mwe_tokenizer

def fr_preprocess_poem(poem_fr, mwe_tokenizer):
    # tokenize poem
    poem_fr_tokens_no_phrase = word_tokenize(poem_fr, language = 'french')

    # remove punctuation
    punctuation = string.punctuation
    poem_fr_tokens_no_punc = [token for token in poem_fr_tokens_no_phrase if token not in punctuation]

    # lemmatize each token if single token else keep as is
    poem_fr_lemmatized = [nlp_fr(token)[0].lemma_ if "_" not in token else token for token in poem_fr_tokens_no_punc]

    # remove stopwords
    stopwords = stopwords.words('french')
    poem_fr_lemmatized_no_stopwords = [token for token in poem_fr_lemmatized if token not in stopwords]
    
    # tokenize poem accounting for phrases
    poem_fr_tokens_phrasal = mwe_tokenizer.tokenize(" ".join(poem_fr_lemmatized_no_stopwords))

    return poem_fr_tokens_phrasal

def fr_poem_emotions(cleaned_poem_fr, feel_df):
    # given a poem in french, return the emotions of the poem
    poem_emotions_vector = [0 for elem in range(len(emotions))]
    emotions_dict = {}
    poem_polarity = 0

    for token in cleaned_poem_fr:
        token_row = (feel_df[feel_df['word'] == token])
        for column in token_row:
            if column == 'id' or column == 'word':
                pass
            elif column == 'polarity':
                # calculating poem polarity
                poem_polarity += (token_row[column].values[0])
            else:
                # creating emotions vector
                if token_row[column].values[0] == 1:
                    index = emotions.index(column)
                    poem_emotions[index] += 1

                    # creating emotions dictionary
                    if column in emotions_dict:
                        emotions_dict[column] += 1
                    else:
                        emotions_dict[column] = 1
    poem_emotions = Poem_Emotions('FR', poem_polarity, poem_emotions_vector, poem_emotions)
    return poem_emotions

def en_preprocess_emotions_df(lrc_lexicon):
    pass

if __name__ == '__main__':
    main()


# # import pandas as pd
# # from nrclex import NRCLex
# # import sys
# # from nltk.tokenize import word_tokenize
# def main():
#     # with open(sys.argv[1], 'r') as f:
#     #     poem_fr = f.read()
#     # with open(sys.argv[2], 'r') as f:
#     #     poem_en = f.read()
#     data = np.load('feel.npy', allow_pickle=True)
#     print(data)
#     # sentiment_poem_fr(poem_fr)

# # def sentiment_poem_fr(poem_fr):
# #     feel_df = pd.read_csv('FEEL.csv')
# #     poem_fr_tokens = word_tokenize(poem_fr)
# #     for token in poem_fr_tokens:
# #         if token in feel_df["word"]:
# #             print(feel_df["word"] == token)


