import pandas as pd
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from translator import translate_text



class SentimentAlgorithm:
    def __init__(self):
        self.custom_lexicon = {
            # Positive sentiment words
            "good": 2,
            "happy": 3,
            "pleasant": 3,
            "suprisingly": 3,
            "great": 4,
            "fantastic": 4,
            "love": 4,
            "joyful":4,
            "delightful": 4,
            "strong":4,
            "excellent": 5,
            "wonderful": 5,
            "amazing": 5,
            "marvelous": 5,
            "highly":5,
            "high":5,
            "positive": 5,
            

            # Negative sentiment words
            "bad": -2,
            "sad": -3,
            "disappointing": -3,
            "unpleasant": -3,
            "terrible": -4,
            "awful": -4,
            "miserable": -4,
            "hate": -4,
            "low":-4,
            "weak":-4,
            "horrible": -5,
            "disgusting": -5,
            "negative":-5,
            
        }
        
        self.custom_amplifiers = {
            # Modifiers (amplifiers/diminishers)
            # Amplifier Increases sentiment score, the value will be greater than 0.
            # Diminishers: Decreases the sentiment score, value between 0 & 1
            "barely": 0.3,
            "slightly": 0.5,
            "somewhat": 0.7,
            "true": 0.8,
            "quite": 1.2,
            "very": 1.5,
            "right":1.5,
            "flavourful":1.5,
            "extremely": 2,
            "recommend":2,
            
            
        }

        self.custom_negations ={
            # Negations (Negates the sentiment of the following word, the value will be less than 0)
            "hardly": -0.7,
            "barely": -0.8,
            "False":-0.8,
            "not": -1,
            "never": -1,
            "no": -1,
            "wrong":-1,
        }



    def preprocess_paragraph(self, paragraph):
        # Preprocess the text, before that we need to check whether the text is in english or else we are going to translate it to english
        #translated_text = translate_text(paragraph)
        Cleaned_text = re.sub(r'http\S+|www\S+|https\S+|href\S+', ' ', paragraph, flags=re.MULTILINE)
        soup = BeautifulSoup(Cleaned_text, 'html.parser')
        Cleaned_text = soup.get_text(separator=' ')
        Cleaned_text = re.sub(r'[<>=,.()/!]+', ' ', Cleaned_text)
        Cleaned_text = re.sub('[^a-zA-Z]', ' ', Cleaned_text)
        Cleaned_text = re.sub(r'\s+', ' ', Cleaned_text).strip()
        Cleaned_text = Cleaned_text.lower()
        Cleaned_text = word_tokenize(Cleaned_text)
        return Cleaned_text

    def preprocess_dataframe(self, data):
        corpus = []
        for i in range(len(data)):
            Cleaned_text = re.sub(r'http\S+|www\S+|https\S+|href\S+', ' ', data["Text"][i], flags=re.MULTILINE)
            soup = BeautifulSoup(Cleaned_text, 'html.parser')
            Cleaned_text = soup.get_text(separator=' ')
            Cleaned_text = re.sub(r'[<>=,.()/!]+', ' ', Cleaned_text)
            Cleaned_text = re.sub('[^a-zA-Z]', ' ', Cleaned_text)
            Cleaned_text = re.sub(r'\s+', ' ', Cleaned_text).strip()
            Cleaned_text = Cleaned_text.lower()
            Cleaned_text = word_tokenize(Cleaned_text)
            corpus.append(" ".join(Cleaned_text))
        data['Cleaned_Text'] = corpus
        return data

    def preprocess(self, input_data):
        if isinstance(input_data, pd.DataFrame):
            return self.preprocess_dataframe(input_data)
        elif isinstance(input_data, str):
            return self.preprocess_paragraph(input_data)
        else:
            raise ValueError("Input data must be a pandas DataFrame or a string representing a paragraph.")

    def calculate_sentiment(self, text):
        words = self.preprocess(text)
        score = 0
        i = 0
        
        while i < len(words):
            word = words[i]
            if word in self.custom_lexicon:
                current_score = self.custom_lexicon[word]
                
                # Check for modifiers or negations before the sentiment word
                if i > 0:
                    prev_word = words[i-1]
                    if prev_word in self.custom_negations:
                        current_score *= self.custom_negations[prev_word]
                    elif prev_word in self.custom_amplifiers:
                        current_score *= self.custom_amplifiers[prev_word]
                        
                    # Handle the case where negation and amplifier are combined
                    if i > 1:
                        prev_prev_word = words[i-2]
                        if prev_prev_word in self.custom_negations:
                            current_score *= self.custom_negations[prev_prev_word]

                score += current_score
            i += 1
        
        return score


    def classify_sentiment(self, text):
        score = self.calculate_sentiment(text)
        if score > 1:
            return "positive"
        elif score < -1:
            return "negative"
        else:
            return "neutral"


    def sentiment_distribution(self, text):
        # Break down the text into sentences
        sentences = sent_tokenize(text)
        
        # Analyze sentiment for each sentence
        sentiment_scores = []
        sentiment_labels = []

        for sentence in sentences:
            score = self.calculate_sentiment(sentence)
            label = self.classify_sentiment(sentence)
            sentiment_scores.append((sentence, score))
            sentiment_labels.append((sentence, label))
        
        return sentiment_scores, sentiment_labels
