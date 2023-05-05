import spacy
import string
import re
from nltk import Tree
from g2p import make_g2p
from g2p_en import G2p
from scipy import spatial
from zss import simple_distance, Node

######### CONSTANTS #########

# How important should phonetic similarity be as a proportion of the syntactic
# similarity?
PHONETIC_RATIO = 0.5


########## PARSE TREE ANALYSIS ##########

# These are the deeper pipelines. If performance becomes an issue we can switch
# to more optimized ones.
nlp_en = spacy.load("en_core_web_trf")
nlp_fr = spacy.load("fr_dep_news_trf")

class MyNode(object):

    def __init__(self, label):
        self.label = label
        self.children = list()

    @staticmethod
    def get_children(node):
        return node.children

    @staticmethod
    def get_label(node):
        return node.label

    def addkid(self, node, before=False):
        if before:  self.children.insert(0, node)
        else:   self.children.append(node)
        return self

# Converts a spaCy tree into a tree for Zhang-Shasha.
# (zs_t is the root of the Zhang-Shasha tree, children is a list of nodes to be 
# added.)
def to_zss_tree(children, zs_t):
    # First add all the children to the Zhang-Shasha tree.
    for child in children:
        zs_t.addkid(MyNode(child.pos_))
    # For each child we just added, recursively add its children.
    for child, node in zip(children, MyNode.get_children(zs_t)):
        to_zss_tree(list(child.children), node)
    return zs_t

# Returns 1 minus the Zhang-Shasha edit distance between the parse trees of the 
# French and English texts, normalized on the number of nodes in the larger tree.
def parse_similarity(src_fr, src_en):
    zss_dist = 0

    # Split source on line breaks or full breaks.
    satze_fr = re.split('\n|\.', src_fr)
    satze_en = re.split('\n|\.', src_en)

    # POS tag every sentence, then compare the tag structure.
    for s_en, s_fr in zip(satze_en, satze_fr):
        doc_en = nlp_en(s_en)
        # Form trees from the spaCy dependency graphs.
        # There should only be one sentence here.
        for sent in doc_en.sents:
            t_en = to_zss_tree(sent.root.children, MyNode(sent.root.pos_))
        doc_fr = nlp_fr(s_fr)
        for sent in doc_fr.sents:
            t_fr = to_zss_tree(sent.root.children, MyNode(sent.root.pos_))
        # Compute the Zhang-Shasha edit distance:
        zss_dist = zss_dist + simple_distance(t_fr, t_en)

    return 1-(zss_dist / max(len(doc_en), len(doc_fr)))

########## PHONEME ANALYSIS ##########

# ARPAbet phonemes:
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
    # First strip of all punctuation symbols.
    # TODO Should add special weight to punctuation.
    src_stripped = src_fr.translate(str.maketrans('', '', string.punctuation))
    arpas = transducer(src_stripped).output_string
    arpas = arpas.split()
    # Vectorize the occurrences of each phoneme.
    v = [0] * len(phones)
    for sym in arpas:
        old_value = v[phones[sym]]
        v[phones[sym]] = old_value+1
    return v

# Returns the ARPAbet phoneme vector of the given English sentence.
g2p = G2p()
def g2p_en(src_en):
    # Get the ARPAbet symbols of the English sentence.
    # First strip of all punctuation symbols.
    # TODO Should add special weight to punctuation.
    src_stripped = src_en.translate(str.maketrans('', '', string.punctuation))
    arpas = g2p(src_stripped)
    arpas_s = ' '.join(arpas)
    # Remove any stressor symbols.
    arpas_s = re.sub(r'\d+', '', arpas_s)
    arpas_s = arpas_s.split()
    # Vectorize the occurrences of each phoneme.
    v = [0] * len(phones)
    for sym in arpas_s:
        old_value = v[phones[sym]]
        v[phones[sym]] = old_value+1
    return v

# Returns the cosine similarity between the phoneme embeddings of the French
# and English texts.
def phonetic_similarity(src_fr, src_en):
    u = g2p_fr(src_fr)
    v = g2p_en(src_en)
    return (1 - spatial.distance.cosine(u, v))

# Returns the syntactic similarity between poem_fr and poem_en, computed as a
# weighted sum between the phonetic and parse tree similarity.
def calculate_syntactic_similarity(poem_fr, poem_en):
    return PHONETIC_RATIO * phonetic_similarity(poem_fr, poem_en) + (1-PHONETIC_RATIO) * parse_similarity(poem_fr, poem_en)

######### TESTING #########

src_fr = "Sous le pont Mirabeau coule la Seine Et nos amours Faut il qu il m en souvienne La joie venait toujours après la peine"
src_en = "Under the Mirabeau Bridge there flows the Seine And our loves recall how then After each sorrow joy came back again"

print(calculate_syntactic_similarity(src_fr, src_en))
