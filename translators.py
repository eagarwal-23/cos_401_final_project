import googletrans
import deepl
import openai

def main():
    sample_poem = """Demain, dès l’aube, à l’heure où blanchit la campagne,
                    Je partirai. Vois-tu, je sais que tu m’attends.
                    J’irai par la forêt, j’irai par la montagne.
                    Je ne puis demeurer loin de toi plus longtemps.

                    Je marcherai les yeux fixés sur mes pensées,
                    Sans rien voir au dehors, sans entendre aucun bruit,
                    Seul, inconnu, le dos courbé, les mains croisées,
                    Triste, et le jour pour moi sera comme la nuit.

                    Je ne regarderai ni l’or du soir qui tombe,
                    Ni les voiles au loin descendant vers Harfleur,
                    Et quand j’arriverai, je mettrai sur ta tombe
                    Un bouquet de houx vert et de bruyère en fleur."""

    print("Poem translated by Google Translate:\n", translate_poem_google(sample_poem))
    print("Poem translated by DeepL:\n", translate_poem_deepl(sample_poem))

def translate_poem_google(poem, lang='en'):
    # translate poem from French to English
    translator = googletrans.Translator()
    poem_en = translator.translate(poem, dest=lang)
    return poem_en.text

def translate_poem_deepl(poem, lang='EN-GB'):
    # translate poem from French to English
    translator = deepl.Translator('0c9c56f4-ef9d-0179-33a1-c1dde6e7ec9a:fx') 
    poem_en = translator.translate_text(poem, target_lang=lang) 
    return poem_en.text

def translate_poem_openai(poem, lang = 'English'):
    openai.api_key = 'tfvQfDrGL6qp4cOveI5CT3BlbkFJ5AiIZCfxKfyUPqxoZfsL'
    model = openai.Model.create(
    engine="text-davinci-002",
    prompt="Translate the following poem into, " + lang + ":\n\n" + poem + "\n\n1.",
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)


if __name__ == '__main__':
    main()
