from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    poem = request.form['poem']
    og_poem = poem
    # translation function
    poem1 = poem
    poem2 = poem
    poem3 = poem
    trans_poem = [poem1, poem2, poem3]

    # semantic score for each translation
    semantic = [len(poem1), len(poem2), len(poem3)]

    # structural score for each translation
    struct = [len(poem1)-1, len(poem2)-2, len(poem3)-3]

    # emotional score for each translation
    emotion = [len(poem1)+1, len(poem2)+2, len(poem3)+3]

    return render_template('result.html', og_poem = og_poem, translation=trans_poem, semantic = semantic, struct = struct, emotion = emotion)

if __name__ == '__main__':
    app.run(debug=True)
