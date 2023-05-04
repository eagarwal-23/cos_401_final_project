from sentence_transformers import SentenceTransformer
from scipy import spatial
import sys

def main():
    with open(sys.argv[1], 'r') as f:
        poem_fr = f.read()
    with open(sys.argv[2], 'r') as f:
        poem_en = f.read()
    print(calculate_semantic_similarity(poem_fr, poem_en))

# calculate semantic similarity between french poem and input english translation
def calculate_semantic_similarity(poem_fr, poem_en):

    # two alternate models we can use
    # model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    fr_embeddings = model.encode(poem_fr)
    en_embeddings = model.encode(poem_en)
    return (1 - spatial.distance.cosine(fr_embeddings, en_embeddings))

if __name__ == '__main__':
    main()