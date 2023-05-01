import config
import googletrans
import deepl
import openai
import sys

def main():
    with open(sys.argv[1], 'r') as f:
        poem_fr = f.read()
    with open(sys.argv[2], 'r') as f:
        poem_en = f.read()

    print("Original poem:\n", poem_fr, "\n")
    print("Poem translated by a human:\n", poem_en, "\n")
    print("Poem translated by Google Translate:\n", translate_poem_google(poem_fr), "\n")
    print("Poem translated by DeepL:\n", translate_poem_deepl(poem_fr), "\n")
    print("Poem translated by OpenAI:\n", translate_poem_openai(poem_fr), "\n")

def translate_poem_google(poem, lang='en'):
    # translate poem from French to English with Google Translate API
    translator = googletrans.Translator()
    poem_en = translator.translate(poem, dest=lang)
    return poem_en.text

def translate_poem_deepl(poem, lang='EN-GB'):
    # translate poem from French to English with deepl API
    translator = deepl.Translator(config.api_key_deepl) 
    poem_en = translator.translate_text(poem, target_lang=lang) 
    return poem_en.text

def translate_poem_openai(poem, lang = 'English'):
    # translate poem from French to English with OpenAI API
    openai.api_key = config.api_key_openai
    response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Translate the following poem into, " + lang + ":\n" + poem + "\n.",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    return response['choices'][0]['text'].strip()

if __name__ == '__main__':
    main()
