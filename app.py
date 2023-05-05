# TERMINAL COMMANDS:
## pip install flash
## pip install -r requirements.txt
## python -m nltk.downloader punkt
## python3 -m spacy download en_core_web_md
## pip install pyphen 
## pip install spacy_lefff
## pip install g2p
## pip install g2p_en     
## python3 app.py

from flask import Flask, render_template, request
from translators import generate_translations
from semantic import calculate_semantic_similarity
from emotions import calc_emotional_similarity
import Poem_Emotions 
from lexical import calculate_lexical_similarity
from syntactic import calculate_syntactic_similarity
# emotions_ranked returns dictionary: keys = emotions, values = percentage (keys already ranked)
# polarity returns one value of poem polarity


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    og_poem = request.form['og_poem']
    human_trans = request.form['human_trans']
    pref = request.form.get('preference')
    print(pref)
    # translation function
    [google_trans, deepl_trans, openai_trans, human_trans] = generate_translations(og_poem, human_trans)
    trans_poem = [human_trans, google_trans, deepl_trans, openai_trans]
    for i in range(4):
        trans_poem[i] = trans_poem[i].replace("\n", "<br>")

    # semantic score for each translation
    semantic = [0,0,1,0]
    for i in range(4):
        semantic[i] = round(calculate_semantic_similarity(og_poem, trans_poem[i]), 5)

    # structural score for each translation
    struct = [0,0,1,0]
    for i in range(4):
        struct[i] = round(calculate_syntactic_similarity(og_poem, trans_poem[i]), 5)

    # emotional score for each translation
    emotion = [0,0,1,0]
    polarity = [0,0,0,0]
    # for testing
    # sad = "sad"
    # angry = "angry"
    # love = "love"
    # emo_ranked = [{sad:0, angry:1, love:2},{sad:0, angry:1, love:2},{sad:0, angry:1, love:2},{sad:0, angry:1, love:2}] 
    emo_ranked = [{},{},{},{}]
    for i in range(4):
        emo = calc_emotional_similarity(og_poem, trans_poem[i])
        emotion[i] = round(emo[0], 5)
        polarity[i] = emo[2].polarity()
        emo_ranked[i] = emo[2].emotions_ranked()

    # emotional score for og french poem
    og_poem_emotions = [og_poem, emo[1].polarity(), emo[1].emotions_ranked()]
    # og_poem_emotions = [og_poem, 0.01, {sad:0, angry:1, love:2}] # for testing

    # emotional score for each translation
    lexical = [0,0,1,0]
    for i in range(4):
        lexical[i] = round(calculate_lexical_similarity(og_poem, trans_poem[i]), 5)

    # handle preference
    if (pref=="no_pref"): pref = 10
    elif (pref=="sem"): pref = semantic.index(max(semantic))
    elif (pref=="syn"): pref = struct.index(max(struct))
    elif (pref=="emote"): pref = emotion.index(max(emotion))
    elif (pref=="lex"): pref = lexical.index(max(lexical))
    print(pref)

    return render_template('result.html', og_poem = og_poem_emotions, human_trans = human_trans, 
        translation=trans_poem, semantic = semantic, struct = struct, emotion = emotion, lexical = lexical,
        emo_ranked = emo_ranked, polarity = polarity, pref = pref)

if __name__ == '__main__':
    app.run(debug=True)
