import pyphen
from nltk.tokenize import word_tokenize
from nltk import Counter
import regex as re
import spacy
from spacy_lefff import LefffLemmatizer, POSTagger
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.tag import StanfordPOSTagger
import googletrans
import sys

# for lexical complexity

# nlp_en = spacy.load("en_core_web_trf")
# nlp_fr = spacy.load("fr_dep_news_trf")

nlp_en = spacy.load("en_core_web_md")
nlp_fr = spacy.load("fr_core_news_md")

def main():
    
    with open(sys.argv[1], 'r') as f:
        poem_fr = f.read()
    with open(sys.argv[2], 'r') as f:
        poem_en = f.read()

    print(calculate_lexical_similarity(poem_fr, poem_en))
    
# calculate lexical similarity
def calculate_lexical_similarity(poem_fr, poem_en):
    a = (en_fr_diff_normalized(mean_syllables_poem, poem_en, poem_fr))
    b = (en_fr_diff_normalized(mean_words_per_line, poem_en, poem_fr))
    c = (en_fr_diff_normalized(ttr, poem_en, poem_fr))
    d = (en_fr_diff_normalized(abstract_concrete_ratio, poem_en, poem_fr))
    e = (en_fr_diff_normalized(lexical_density, poem_en, poem_fr))

    return 0.99 - ((a * 0.11 + b * 0.11 + c * 0.11 + d * 0.33 + e * 0.33)/0.99)

# calculate normalized diff given a function, an english poem, and a french poem
def en_fr_diff_normalized(func, poem_en, poem_fr):
    if func(poem_fr, lang = 'fr') != 0:
        return abs(func(poem_en, lang = 'en') - func(poem_fr, lang = 'fr'))/(func(poem_fr, lang = 'fr'))
    else: 
        return abs(func(poem_en, lang = 'en') - func(poem_fr, lang = 'fr'))

# calculate average number of syllables per word for a given poem
def mean_syllables_poem(poem, lang = 'en'):
    dic_fr = pyphen.Pyphen(lang='fr_FR')
    dic_en = pyphen.Pyphen(lang='en_GB')
    syllables = 0

    if lang == 'fr':
        poem_tokens = word_tokenize(poem, language= "french")
        for token in poem_tokens: 
            syllables += len(dic_fr.inserted(token).split('-'))
    else:
        poem_tokens = word_tokenize(poem, language= "english")
        for token in poem_tokens: 
            syllables += len(dic_en.inserted(token).split('-'))
    
    return syllables/len(poem_tokens)

# calculate average number of words per line (defined by linebreaks) 
# for a given poem
def mean_words_per_line(poem, lang = 'en'):
    num_lines = len(poem.split("\n"))

    poem = re.sub(r'[^\w]', ' ', poem)
    if lang == 'fr':
        poem_tokens = word_tokenize(poem, language= "french")
    else:
        poem_tokens = word_tokenize(poem, language= "english")

    return len(poem_tokens)/(num_lines)

# type-token ratio (# of unique words/total # of words)
def ttr(poem, lang = 'en'):
    poem = re.sub(r'[^\w]', ' ', poem)
    if lang == 'fr':
        poem_tokens = word_tokenize(poem, language= "french")
    else:
        poem_tokens = word_tokenize(poem, language= "english")

    return len(Counter(poem_tokens))/len(poem_tokens)

# referenced code from:
# https://en.wikipedia.org/wiki/Lesk_algorithm
# https://github.com/Akirato/Lesk-Algorithm/blob/master/leskAlgorithm.py

# implementation of Lesk algorithm (as described above) for French
def lesk_fr(sentence_tokens, word, synsets):
    max_overlap = 0
    best_sense = synsets[0]
    sentence_tokens = set(sentence_tokens)

    # for every possible meaning of a given word
    for sense in synsets:
        # add definition and example for sense
        signature = set(sense.definition().split())
        for example in sense.examples():
            signature.union(set(example.split()))

        # add definition and example for each of its hyponyms
        for hyp in sense.hyponyms() + sense.hypernyms():
            signature.union(set(hyp.definition().split()))
            for example in hyp.examples():
                signature.union(set(example.split()))
        overlap = len(sentence_tokens.intersection(signature))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense

# single method to calculate abstract-concrete ratio given a poem and a language
def abstract_concrete_ratio(poem, lang = 'en'):
    if lang == 'en':
        return abstract_concrete_ratio_en(poem)
    else:
        return abstract_concrete_ratio_fr(poem)

# calculate abstract concrete ratio for a french poem
def abstract_concrete_ratio_fr(poem):
    # nouns categorized as abstract
    lexical_categories_abs = ['noun.attribute', 'noun.cognition', 'noun.communication', 'noun.event', 'noun.feeling', 'noun.group', 'noun.location', 'noun.motive', 'noun.phenomenon', 'noun.possession', 'noun.quantity', 'noun.relation', 'noun.state', 'noun.time']
    
    # nouns categorized as concrete
    lexical_categories_con = ['noun.animal', 'noun.person', 'noun.artifact', 'noun.body', 'noun.food', 'noun.plant', 'noun.shape', 'noun.substance', 'noun.object']
    doc = nlp_fr(poem)

    # translate poem to english and tokenize for use in lesk algorithm
    translator = googletrans.Translator()
    poem_en = translator.translate(poem).text
    tokens = word_tokenize(poem_en, language= "english")

    tokens = [token.text for token in doc]
    abs = 0
    con = 0
    for word in doc:
        token = word.text
        if word.tag_ == 'NOUN':
            if len(wn.synsets(token,lang='fra')) != 0:
                synset = lesk_fr(tokens, (translator.translate(token)).text, wn.synsets(token,lang='fra'))
                if synset.lexname().startswith('noun.'):
                    if synset.lexname() in lexical_categories_abs:
                        abs += 1
                    elif synset.lexname() in lexical_categories_con:
                        con += 1
    return (abs/con)

# calculate abstract concrete ratio for an english poem
def abstract_concrete_ratio_en(poem):
    # nouns categorized as abstract
    lexical_categories_abs = ['noun.attribute', 'noun.cognition', 'noun.communication', 'noun.event', 'noun.feeling', 'noun.group', 'noun.location', 'noun.motive', 'noun.phenomenon', 'noun.possession', 'noun.quantity', 'noun.relation', 'noun.state', 'noun.time']
    
    # nouns categorized as concrete
    lexical_categories_con = ['noun.animal', 'noun.person', 'noun.artifact', 'noun.body', 'noun.food', 'noun.plant', 'noun.shape', 'noun.substance', 'noun.object']
    noun_pos_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    doc = nlp_en(poem)
    tokens = [token.text for token in doc]

    abs = 0
    con = 0
    for word in doc:
        token = word.text
        # if word is a noun
        if word.tag_ in noun_pos_tags and lesk(tokens, token):
            # proper nouns are always concrete
            if word.tag_ == 'NNP' or word.tag_ == 'NNPS':
                con += 1
            else:
                synset = lesk(tokens, token)
                if synset.lexname().startswith('noun.'):
                    if synset.lexname() in lexical_categories_abs:
                        abs += 1
                    elif synset.lexname() in lexical_categories_con:
                        con += 1
    return (abs/con)

# compute lexical density given a poem and a language (ratio of content words
# to total # of words in the poem)
def lexical_density(poem, lang = 'en'):
    # list of content words
    lexical = ['NOUN', 'VERB', 'ADV', 'ADJ']

    lexical_count = 0
    if lang == 'en':
        doc = nlp_en(poem)
        for word in doc:
            if word.pos_ in lexical:
                lexical_count += 1
        return lexical_count/len([token.text for token in doc])
    else:
        doc = nlp_fr(poem)
        for word in doc:
            if word.pos_ in lexical:
                lexical_count += 1
        return lexical_count/len([token.text for token in doc])

if __name__ == '__main__':
    main()