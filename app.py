# TERMINAL COMMANDS:
## pip install flash
## pip install -r requirements.txt
## python -m nltk.downloader punkt
## python3 app.py

from flask import Flask, render_template, request
from translators import generate_translations
from semantic import calculate_semantic_similarity
from emotions import calc_emotional_similarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    og_poem = request.form['og_poem']
    human_trans = request.form['human_trans']
    # translation function
    [google_trans, deepl_trans, openai_trans, human_trans] = generate_translations(og_poem, human_trans)
    trans_poem = [human_trans, google_trans, deepl_trans, openai_trans]

    # semantic score for each translation
    semantic = [0,0,0,0]
    for i in range(4):
        semantic[i] = round(calculate_semantic_similarity(og_poem, trans_poem[i]), 5)

    # structural score for each translation
    struct = [1,1,1,1]

    # emotional score for each translation
    emotion = [0,0,0,0]
    for i in range(4):
        emo = calc_emotional_similarity(og_poem, trans_poem[i])
        emotion[i] = round(emo[0], 5)

    lexical = [0,0,0,0]

    return render_template('result.html', og_poem = og_poem, translation=trans_poem, semantic = semantic, struct = struct, emotion = emotion, lexical = lexical)

if __name__ == '__main__':
    app.run(debug=True)
