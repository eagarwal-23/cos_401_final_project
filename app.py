# TERMINAL COMMANDS:
## pip install flash
## pip install -r requirements.txt
## python3 -m nltk.downloader punkt
## python3 -m nltk.downloader wordnet
## python3 -m nltk.downloader omw-1.4
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
def page1():
    return render_template('page1.html')

@app.route('/translate', methods=['POST'])
def translate():
    og_poem = request.form['og_poem']
    human_trans = request.form['human_trans']
    pref = request.form.get('preference')
    dropdown_option = pref
    print(pref)
    # translation function
    [google_trans, deepl_trans, openai_trans, human_trans] = generate_translations(og_poem, human_trans)
    trans_poem = [human_trans, google_trans, deepl_trans, openai_trans]
    for i in range(4):
        trans_poem[i] = trans_poem[i].replace("\n", "<br>")

    ## init
    semantic = [0,0,1,0]
    struct = [0,0,1,0]
    emotion = [0,0,1,0]
    polarity = [0,0,0,0]
    lexical = [0,-20,-1,-1]

    ## testing
    # sad = "sad"
    # angry = "angry"
    # love = "love"
    # emo_ranked = [{sad:0.010101010101, angry:.01010101, love:2},{sad:0, angry:1.2020202, love:2},{sad:0, angry:1, love:2.10200302},{sad:0, angry:1, love:2}] 
    # og_poem_emotions = [og_poem, 0.01, {sad:0, angry:1, love:2}]
    # for i in range(len(emo_ranked)):
    #     for key in emo_ranked[i]:
    #         emo_ranked[i][key] = round(emo_ranked[i][key], 2)

    ### actual
    # semantic score for each translation
    for i in range(4):
        semantic[i] = round(calculate_semantic_similarity(og_poem, trans_poem[i]), 4)

    # structural score for each translation
    for i in range(4):
        struct[i] = round(calculate_syntactic_similarity(og_poem, trans_poem[i]), 4)

    # emotional score for each translation
    emo_ranked = [{},{},{},{}]
    for i in range(4):
        emo = calc_emotional_similarity(og_poem, trans_poem[i])
        emotion[i] = round(emo[0], 4)
        polarity[i] = round(emo[2].polarity(), 4)
        emo_ranked[i] = emo[2].emotions_ranked()
    # round all values in ranked dictionaries
    for i in range(len(emo_ranked)):
        for key in emo_ranked[i]:
            emo_ranked[i][key] = round(emo_ranked[i][key], 2)

    #emotional score for og french poem
    og_poem_emotions = [og_poem, round(emo[1].polarity(), 4), emo[1].emotions_ranked()]

    # emotional score for each translation
    for i in range(4):
        lexical[i] = abs(round(calculate_lexical_similarity(og_poem, trans_poem[i]), 4))

    # handle preference
    prefs = ["No Preference", "Semantic", "Syntactic", "Emotional", "Lexical"]
    if (pref==prefs[0]): pref = 10
    elif (pref==prefs[1]): pref = semantic.index(max(semantic))
    elif (pref==prefs[2]): pref = struct.index(max(struct))
    elif (pref==prefs[3]): pref = emotion.index(max(emotion))
    elif (pref==prefs[4]): pref = lexical.index(max(lexical))
    print(pref)

    return render_template('page2.html', og_poem = og_poem_emotions, human_trans = human_trans, 
        translation=trans_poem, semantic = semantic, struct = struct, emotion = emotion, lexical = lexical,
        emo_ranked = emo_ranked, polarity = polarity, pref = pref, dropdown_option = dropdown_option, prefs = prefs)

if __name__ == '__main__':
    app.run(debug=True)
