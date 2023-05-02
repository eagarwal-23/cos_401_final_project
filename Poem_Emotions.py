class Poem_Emotions():
    def __init__(self, lang, polarity, emotions_vector, emotions_dict):
        self.lang = lang
        self.poem_polarity = polarity
        self.emotions_vector = emotions_vector
        self.emotions_dict = emotions_dict

    def emotions_normalized(self):
        emotions_normalized = {}
        num_emotions = sum((self.emotions_dict).values())
        for emotion, count in (self.emotions_dict).items():
            emotions_normalized[emotion] = count/num_emotions
        return emotions_normalized