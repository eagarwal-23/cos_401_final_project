import nltk
import pandas as pd
import numpy as np
import spacy
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, MWETokenizer
from nltk.tokenize import MWETokenizer
import Poem_Emotions
import sys


# TODO: change punctuation removal to regex method
# constants
# nlp_en = spacy.load("en_core_web_trf")
# nlp_fr = spacy.load("fr_dep_news_trf")

nlp_en = spacy.load("en_core_web_md")
nlp_fr = spacy.load("fr_core_news_md")

emotions = ['joy', 'fear', 'sadness', 'anger', 'surprise', 'disgust']
punctuation = string.punctuation

def main():
    with open(sys.argv[1], 'r') as f:
        poem_fr = f.read()
    with open(sys.argv[2], 'r') as f:
        poem_en = f.read()
    a, b, c = calc_emotional_similarity(poem_fr, poem_en)
    print("french", b.emotions_ranked(), b.polarity())
    print("english", c.emotions_ranked(), c.polarity())

# calculate emotional similarity between french poem and input english translation
def calc_emotional_similarity(poem_fr, poem_en):
    # read in and preprocess emotion lexicons
    feel_df = pd.read_csv('FEEL.csv', sep = ";")
    nrc_df = pd.read_csv('nrc.txt', sep="\t", header=None)
    feel_df_preprocessed = fr_preprocess_emotions_df(feel_df)
    nrc_df_proprocessed = en_preprocess_emotions_df(nrc_df)

    # create tokenizer for french poem
    tokenizer = MWETokenizer()
    tokenizer_fr = fr_create_phrase_tokenizer(feel_df_preprocessed, tokenizer)

    # preprocess poems
    cleaned_poem_fr = fr_preprocess_poem(poem_fr, tokenizer_fr)
    cleaned_poem_en = en_preprocess_poem(poem_en)

    # get emotions for both poems
    poem_fr_emotions = fr_poem_emotions(poem_fr, cleaned_poem_fr, feel_df_preprocessed)
    poem_en_emotions = en_poem_emotions(poem_en, cleaned_poem_en, nrc_df_proprocessed)

    return [poem_fr_emotions.calc_dist(poem_en_emotions), poem_fr_emotions, poem_en_emotions]

def fr_preprocess_emotions_df(feel_df):
    # preprocess feel df, change polarity to numerical values
    # and lemmatize all individual tokens
    feel_df.loc[feel_df['polarity'] == "positive", 'polarity'] = 1
    feel_df.loc[feel_df['polarity'] == "negative", 'polarity'] = -1

    feel_df_multiple = feel_df[(feel_df['word'].str.split().apply(len)) > 1]
    feel_df_single = feel_df[(feel_df['word'].str.split().apply(len)) == 1]
    feel_df_single['word'] = feel_df_single['word'].apply(lambda x: nlp_fr(x)[0].lemma_)
    
    feel_df = pd.concat([feel_df_single, feel_df_multiple])
    feel_df = feel_df.drop(['id'], axis = 1)
    return feel_df

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
    poem_fr_tokens_no_punc = [token for token in poem_fr_tokens_no_phrase if token not in punctuation]

    # lemmatize each token if single token else keep as is
    poem_fr_lemmatized = [nlp_fr(token)[0].lemma_ if "_" not in token else token for token in poem_fr_tokens_no_punc]

    # remove stopwords
    stopwords_fr = stopwords.words('french')
    poem_fr_lemmatized_no_stopwords = [token for token in poem_fr_lemmatized if token not in stopwords_fr]
    # tokenize poem accounting for phrases
    poem_fr_tokens_phrasal = mwe_tokenizer.tokenize(poem_fr_lemmatized_no_stopwords)

    return poem_fr_tokens_phrasal

def fr_poem_emotions(poem_fr, cleaned_poem_fr, feel_df):
    # given a poem in french, return the emotions of the poem
    poem_emotions_vector = [0 for elem in range(len(emotions))]
    emotions_dict = {}
    poem_polarity = 0
    num_words_counted = 0
    for token in cleaned_poem_fr:
        token = token.lower()
        if token in feel_df['word'].values:
            num_words_counted += 1
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
                        poem_emotions_vector[index] += 1

                        # creating emotions dictionary
                        if column in emotions_dict:
                            emotions_dict[column] += 1
                        else:
                            emotions_dict[column] = 1
    poem_emotions = Poem_Emotions.Poem_Emotions('FR', poem_fr, poem_polarity/num_words_counted, poem_emotions_vector, emotions_dict)
    return poem_emotions

# TODO: lemmatize
def en_preprocess_emotions_df(nrc_df):
    # adding column names
    nrc_df.columns = ['word', 'emotion', 'association']

    # changing orientation of df
    nrc_df = nrc_df.pivot(index='word', columns='emotion', values='association')
    nrc_df['word'] = nrc_df.index

    # add column for polarity
    conditions = [(nrc_df['positive'] == 1), (nrc_df['negative'] == 1)]
    polarities = [1, -1]
    nrc_df['polarity'] = np.select(conditions, polarities)
    nrc_df = nrc_df.drop(['positive', 'negative',], axis = 1)
    nrc_df.dropna(inplace = True)
    nrc_df['word'] = nrc_df['word'].apply(lambda x: nlp_en(x)[0].lemma_)

    # drop columns not in french lexicon
    nrc_df = nrc_df.drop(['anticipation', 'trust',], axis = 1)

    return nrc_df

def en_preprocess_poem(poem_en):
    # tokenize poem
    poem_en_tokens_no_phrase = word_tokenize(poem_en, language = 'english')

    # remove punctuation
    poem_en_tokens_no_punc = [token for token in poem_en_tokens_no_phrase if token not in punctuation]

    # lemmatize each token if single token else keep as is
    poem_en_lemmatized = [nlp_en(token)[0].lemma_ for token in poem_en_tokens_no_punc]

    # remove stopwords
    stopwords_en = stopwords.words('english')
    poem_en_lemmatized_no_stopwords = [token for token in poem_en_lemmatized if token not in stopwords_en]
    
    return poem_en_lemmatized_no_stopwords

def en_poem_emotions(poem_en, cleaned_poem_en, nrc_df):
    poem_emotions_vector = [0 for elem in range(len(emotions))]
    emotions_dict = {}
    poem_polarity = 0
    num_words_counted = 0
    for token in cleaned_poem_en:
        token = token.lower()
        if token in nrc_df['word'].values:
            num_words_counted += 1
            token_row = (nrc_df[nrc_df['word'] == token])
            for column in token_row:
                if column == 'word':
                    pass
                elif column == 'polarity':
                    # calculating poem polarity
                    poem_polarity += (token_row[column].values[0])
                else:
                    # creating emotions vector
                    if token_row[column].values[0] == 1:
                        index = emotions.index(column)
                        poem_emotions_vector[index] += 1

                        # creating emotions dictionary
                        if column in emotions_dict:
                            emotions_dict[column] += 1
                        else:
                            emotions_dict[column] = 1
    
    poem_emotions = Poem_Emotions.Poem_Emotions('EN', poem_en, poem_polarity/num_words_counted, poem_emotions_vector, emotions_dict)
    return poem_emotions

if __name__ == '__main__':
    main()