import pandas as pd
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
#from translator import translate_text

label_encoder = LabelEncoder()




class SentimentAlgorithm:
    def __init__(self):
        self.custom_lexicon = {
            # Positive sentiment words
            "good": 2, 
            "nice":2,
            "happy": 3,
            "Big":3,
            "pleasant": 3,
            "suprisingly": 3,
            "great": 4,
            "fantastic": 4,
            "love": 4,
            "fun":4,
            "joyful":4,
            "congratulation":4,
            "delightful": 4,
            "strong":4,
            "awesome":4.75,
            "excellent": 5,
            "wonderful": 5,
            "amazing": 5,
            "marvelous": 5,
            "highly":5,
            "high":5,
            "positive": 5,
            

            # Negative sentiment words
            "bad": -2,
            "mean":-2,
            "sad": -3,
            "Small":-3,
            "problem":-3, "problems":-3,
            "disappointing": -3,
            "unpleasant": -3,
            "abusive":-4,
            "terrible": -4,
            "awful": -4,
            "miserable": -4,
            "hate": -4,
            "low":-4,
            "weak":-4,
            "ruin":-4,
            "worse":-4.75,
            "horrible": -5,
            "disgusting": -5,
            "negative":-5,
            "violence":-5,

            
        }
        
        self.custom_amplifiers = {
            # Modifiers (amplifiers)
            # Amplifier Increases sentiment score, the value will be greater than 0.
            "exact":0.5, "excatly":0.5,
            "barely": 0.10,
            "slightly": 0.10,
            "somewhat": 0.10,
            "unlimited":0.75,
            "lot":0.55,
            "well":0.45,
            "normal":0.5,
            "new":0.55,
            "true": 0.8, "truly":0.8,
            "even":0.55, "evenly":0.55,          
            "attentive":0.8,
            "more":0.85,
            "compliments":0.9,
            "win":0.9, "winning":0.95, "wins":0.99,
            "easy":0.35,
            "fortunately":0.5, "fortunate":0.5,
            "glad":0.8,
            "enjoy":0.85, "enjoyable":0.85, "enjoying":0.85, "enjoyed":0.85,
            "excite":0.95, "excited":0.95, "exciting":0.95,
            "protect":0.75, "protected":0.75, "protecting":0.75, "protects":0.75,
            "quite": 0.25,
            "very": 0.65,
            "right":0.8,
            "flavourful":0.8, "flavour":0.45,
            "praise":0.75, "applause":0.75,
            "motivate":0.90, "motivates":0.90, "motivated":0.90, "motivating":0.90,
            "extremely": 0.75,
            "recommend":0.8, "recommended":0.8, "recommending":0.8,
            
            
        }

        self.custom_negations ={
            # Negations (Negates the sentiment of the following word, the value will be less than 0)
            "different":-0.25, "difference":-0.25,
            "left":-0.5,
            "leave":-0.5,
            "miss":-0.55, "missing":-0.75, "missed":-0.75,
            "old":-0.55,
            "bored":-0.6, "bore":-0.6, "boring":-0.6,
            "hardly": -0.7,
            "lose":-0.75, "losing":-0.95, "losed":-0.75, 
            "barely": -0.8,
            "enough":-0.75,
            "uneven":-0.8,
            "False":-0.8,
            "distractive":-0.8,
            "hard":-0.9,
            "fail":-0.9, "fails":-0.9, "failed":-1.75,
            "unfortunately":-0.95, "unfortunate":-0.95,
            "don't":-0.99,
            "not": -0.99,
            "never": -0.99,
            "no": -0.99,
            "wrong":-0.85,
            "curse":-0.9,
            "insult":-0.9,
            "harras":-0.9, "harrasing":-0.9,            
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
                        elif prev_prev_word in self.custom_amplifiers:
                            current_score *= self.custom_amplifiers[prev_prev_word]
                            
                score += current_score
            
            # Handle the case where amplifiers or negations are alone
            elif word in self.custom_amplifiers or word in self.custom_negations:
                if i == len(words) - 1 or (i < len(words) - 1 and words[i+1] not in self.custom_lexicon):
                    if word in self.custom_negations:
                        score += self.custom_negations[word]  # This could be negative or a small positive number
                    elif word in self.custom_amplifiers:
                        score += self.custom_amplifiers[word]  # This could increase or emphasize the current score
                        
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
    
    def fit(self, X_train, y_train):
        if len(X_train) != len(y_train):
            raise ValueError("Training features and labels must have the same length.")
        
        for text, sentiment in zip(X_train, y_train):
            words = self.preprocess(text)
            for word in words:
                if word not in self.custom_lexicon:
                    # Assign sentiment value to the new word
                    if sentiment == 1:  # Assuming 1 is for 'positive'
                        self.custom_lexicon[word] = 1
                    elif sentiment == -1:  # Assuming -1 is for 'negative'
                        self.custom_lexicon[word] = -1
                    elif sentiment == 0:  # Assuming 0 is for 'neutral'
                        self.custom_lexicon[word] = 0

    def transform(self, X):
        # Transform input data to the form needed for prediction
        return [self.preprocess_paragraph(text) for text in X]

    def predict(self, X_test):
        # Use the transform method to preprocess test data
        cleaned_texts = [' '.join(text) for text in self.transform(X_test)]
        predicted_labels = [self.classify_sentiment(text) for text in cleaned_texts]
        return predicted_labels
    
    def compute_accuracy(self, X_test, y_test):
        predicted_labels = self.predict(X_test)
        accuracy = accuracy_score(y_test, predicted_labels)
        return accuracy

    '''def compute_accuracy(self, X_test, y_test):
        # Ensure that the y_test labels are in the same format as predictions
        y_test_labels = [label_encoder.inverse_transform([label])[0] for label in y_test]
        predicted_labels = self.predict(X_test)
        accuracy = accuracy_score(y_test_labels, predicted_labels)
        return accuracy'''
