import spacy
import string
import re
from g2p import make_g2p
from g2p_en import G2p

# SYNTAX ANALYSIS
    # Maybe just collect nouns using POS tagger?
    # Take to pronunciation alphabet
    # Compare

# These are the deeper pipelines. If performance becomes an issue we can switch
# to more optimized ones.
nlp_en = spacy.load("en_core_web_trf")
nlp_fr = spacy.load("fr_dep_news_trf")

def compare_syntax_trees(src_en, src_fr):
    # Split source on full stops.
    satze_en = src_en.split('.')
    satze_fr = src_fr.split('.')

    # POS tag every sentence, then compare the tag structure.
    for s_en, s_fr in zip(satze_en, satze_fr):
        doc_en = nlp_en(s_en)
        doc_fr = nlp_fr(s_fr)
        for t in doc_en:
            print(t, t.pos_)
        for t in doc_fr:
            print(t, t.pos_)

# PHONEME ANALYSIS
# Possibly weight the end of a sentence or line?
phones = {"AA" : 0,
          "AE" : 1,
          "AH" : 2,
          "AO" : 3,
          "AW" : 4,
          "AY" : 5,
          "B"  : 6,
          "CH" : 7,
          "D"  : 8,
          "DH" : 9,
          "EH" : 10,
          "ER" : 11,
          "EY" : 12,
          "F"  : 13,
          "G"  : 14,
          "HH" : 15,
          "IH" : 16,
          "IY" : 17,
          "JH" : 18,
          "K"  : 19,
          "L"  : 20,
          "M"  : 21,
          "N"  : 22,
          "NG" : 23,
          "OW" : 24,
          "OY" : 25,
          "P"  : 26,
          "R"  : 27,
          "S"  : 28,
          "SH" : 29,
          "T"  : 30,
          "TH" : 31,
          "UH" : 32,
          "UW" : 33,
          "V"  : 34,
          "W"  : 35,
          "Y"  : 36,
          "Z"  : 37,
          "ZH" : 38}

# Returns the ARPAbet phoneme vector of the given French sentence.
def g2p_fr(src_fr):
    transducer = make_g2p('fra', 'eng-arpabet')
    # Get the ARPAbet symbols of the French sentence.
    arpas = transducer(src_fr).output_string
    arpas = arpas.split()
    # Vectorize the occurrences of each phoneme.
    v = [0] * len(phones)
    for sym in arpas:
        if sym != ".":
            old_value = v[phones[sym]]
            v.insert(phones[sym], old_value+1)
    return v

# Returns the ARPAbet phoneme vector of the given English sentence.
g2p = G2p()
def g2p_en(src_en):
    # Get the ARPAbet symbols of the English sentence.
    arpas = g2p(src_en)
    arpas_s = ' '.join(arpas)
    # Remove any stressor symbols.
    arpas_s = re.sub(r'\d+', '', arpas_s)
    arpas_s = arpas_s.split()
    # Vectorize the occurrences of each phoneme.
    v = [0] * len(phones)
    for sym in arpas_s:
       if sym != ".":
           old_value = v[phones[sym]]
           v.insert(phones[sym], old_value+1)
    return v

def l2_norm(v0, v1):
    return sum((p-q)**2 for p, q in zip(v0, v1)) ** 0.5

def phonetic_dist(src_fr, src_en):
    return l2_norm(g2p_fr(src_fr), g2p_en(src_en))

# src_en = "Where there is smoke there is unpredictability."
# src_fr = "Où il y a fumée il y a changement."
src_en = "Under the Mirabeau Bridge there flows the Seine And our loves recall how then After each sorrow joy came back again"
src_fr = "Sous le pont Mirabeau coule la Seine Et nos amours Faut-il qu’il m’en souvienne La joie venait toujours après la peine"

print(phonetic_dist(src_fr, src_en))
