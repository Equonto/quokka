from typing import List
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from autocorrect import Speller
from completion.model.Enums import TextPreprocessingTaskType

class TextPreprocessor:

    def __init__(self, tasks):
        #nltk.download('punkt') 
        #nltk.download('wordnet') 
        self.tasks : List[TextPreprocessingTaskType] = tasks

    def preprocess_text(self, text: str) -> str:
        for task in self.tasks:
            if (task == TextPreprocessingTaskType.LOWER):
                text = self.lower(text)
            elif (task == TextPreprocessingTaskType.SPELLING_CORRECTION):
                text = self.spelling_correction(text)
            elif (task == TextPreprocessingTaskType.LEMMATIZATION):
                text = self.lemmatization(text)
            elif (task == TextPreprocessingTaskType.STEMMING):
                text = self.stemming(text)
            elif (task == TextPreprocessingTaskType.REMOVE_PUNCTUATION):
                text = self.remove_punctuation(text)
            else:
                raise ValueError("Invalid text preprocessing task: " + task)
        return text

    def lower(self, text) -> str:
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        return text.replace("/", " or ")
    
    def spelling_correction(self, text: str) -> str:
        spell = Speller(lang='en')
        words = nltk.word_tokenize(text)
        corrected_words = [spell(word) for word in words]
        return " ".join(corrected_words)

    def lemmatization(self, text: str) -> str:
        lemmatizer = WordNetLemmatizer()
        words = nltk.word_tokenize(text)
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        return " ".join(lemmatized_words)
    
    def stemming(self, text: str) -> str:
        stemmer = LancasterStemmer()
        words = nltk.word_tokenize(text)
        stemmed_words = [stemmer.stem(word) for word in words]
        return " ".join(stemmed_words)  
    

