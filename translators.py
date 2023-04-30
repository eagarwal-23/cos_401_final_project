import config
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

    sample_poem_2 = """Sous le pont Mirabeau coule la Seine
                        Et nos amours
                        Faut-il qu’il m’en souvienne
                        La joie venait toujours après la peine

                        Vienne la nuit sonne l’heure
                        Les jours s’en vont je demeure

                        Les mains dans les mains restons face à face
                        Tandis que sous
                        Le pont de nos bras passe
                        Des éternels regards l’onde si lasse

                        Vienne la nuit sonne l’heure
                        Les jours s’en vont je demeure

                        L’amour s’en va comme cette eau courante
                        L’amour s’en va
                        Comme la vie est lente
                        Et comme l’Espérance est violente

                        Vienne la nuit sonne l’heure
                        Les jours s’en vont je demeure

                        Passent les jours et passent les semaines
                        Ni temps passé
                        Ni les amours reviennent
                        Sous le pont Mirabeau coule la Seine

                        Vienne la nuit sonne l’heure
                        Les jours s’en vont je demeure"""

    poem_2_human_translation = """Under the Mirabeau Bridge
                        there flows the Seine
                        And our loves recall how then
                        After each sorrow joy came back again

                        Let night come on bells end the day
                        The days go by me still I stay

                        Hands joined and face to face let's stay just so
                        While underneath
                        The bridge of our arms shall go
                        Weary of endless looks the river's flow

                        Let night come on bells end the day
                        The days go by me still I stay

                        All love goes by as water to the sea
                        All love goes by
                        How slow life seems to me
                        How violent the hope of love can be

                        Let night come on bells end the day
                        The days go by me still I stay

                        The days the weeks pass by beyond our ken
                        Neither time past
                        Nor love comes back again
                        Under the Mirabeau Bridge there flows the Seine

                        Let night come on bells end the day
                        The days go by me still I stay"""

    print("Original poem:\n", sample_poem_2)
    print("Poem translated by a human:\n", poem_2_human_translation)
    print("Poem translated by Google Translate:\n", translate_poem_google(sample_poem_2))
    print("Poem translated by DeepL:\n", translate_poem_deepl(sample_poem_2))
    print("Poem translated by OpenAI:\n", translate_poem_openai(sample_poem_2))

def translate_poem_google(poem, lang='en'):
    # translate poem from French to English
    translator = googletrans.Translator()
    poem_en = translator.translate(poem, dest=lang)
    return poem_en.text

def translate_poem_deepl(poem, lang='EN-GB'):
    # translate poem from French to English
    translator = deepl.Translator(config.api_key_deepl) 
    poem_en = translator.translate_text(poem, target_lang=lang) 
    return poem_en.text

def translate_poem_openai(poem, lang = 'English'):
    openai.api_key = config.api_key_deepl
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
