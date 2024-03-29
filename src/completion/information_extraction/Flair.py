from flair.models import SequenceTagger
from flair.data import Sentence
from completion.information_extraction.TaggedNgram import TaggedNgram
from completion.information_extraction.TaggedSentence import TaggedSentence

class FlairEntityRecognition:

    def __init__(self):
        self.tagger : SequenceTagger

    def load(self, flair_model_name: str):
        self.tagger = SequenceTagger.load(flair_model_name)

    def tag_text(self, text: str) -> TaggedSentence:
        sentence = Sentence(text)
        self.tagger.predict(sentence)
        return self.format_tagged_sentence(sentence)
    
    def format_tagged_sentence(self, sentence: Sentence) -> TaggedSentence: 
        formatted_sentence = TaggedSentence(None)
        for label in sentence.labels:
            formatted_sentence.add_tagged_ngram(
                TaggedNgram(
                label.data_point.text,
                label.value)
                )
        return formatted_sentence
    