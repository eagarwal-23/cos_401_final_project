class Poem_Emotions():

    def __init__(self, lang, poem, polarity, emotions_vector, emotions_dict):
        self.lang = lang
        self.poem = poem
        self.poem_polarity = polarity
        self.emotions_vector = emotions_vector
        self.emotions_dict = emotions_dict
    
    def __str__(self):
        emotions = ['joy', 'fear', 'sadness', 'anger', 'surprise', 'disgust']
        str_emotions = "Poem:\n" + self.poem + "\n"
        str_emotions += "Emotions Dictionary: " +  str(self.emotions_dict) + "\n"
        str_emotions += "Universal Emotions Vector: " + str(emotions) + "\n"
        str_emotions += "Emotions Vector: " + str(self.emotions_vector) + "\n"
        str_emotions += "Polarity: " + str(self.poem_polarity)
        return str_emotions

    def emotions_normalized(self):
        emotions_normalized = {}
        num_emotions = sum((self.emotions_dict).values())
        for emotion, count in (self.emotions_dict).items():
            emotions_normalized[emotion] = count/num_emotions
        return emotions_normalized

    def polarity(self):
        return self.poem_polarity
    
    def emotions_ranked(self):
        return dict(sorted(self.emotions_normalized().items(), key=lambda item: item[1]))
    
    def calc_dist(self, emotions_other):
        return sum((p-q)**2 for p, q in zip(self.emotions_vector, emotions_other.emotions_vector)) ** 0.5