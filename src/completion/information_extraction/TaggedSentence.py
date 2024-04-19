
from typing import List, Optional

from pandas import DataFrame, Series
from completion.information_extraction.Relation import Relation
from completion.information_extraction.TaggedNgram import TaggedNgram

class TaggedSentence:

    def __init__(self, tagged_ngrams: Optional[List[TaggedNgram]]) -> None:
        # the relevant row from the input data
        self.raw_input_data : Series = Series()
        self.preprocessed_text : str = ""
        self.relations : List[Relation] = []
        if (tagged_ngrams == None):
            self.tagged_ngrams : List[TaggedNgram] = []
        else:
            self.tagged_ngrams : List[TaggedNgram] = tagged_ngrams
    
    def get_tagged_ngrams(self) -> List[TaggedNgram]:
        return self.tagged_ngrams
    
    def set_raw_input_data(self, raw_input_data: Series) -> None:
        self.raw_input_data = raw_input_data
    
    def get_raw_input_data(self) -> Series:
        return self.raw_input_data
    
    def set_preprocessed_text(self, preprocessed_text: str) -> None:
        self.preprocessed_text = preprocessed_text

    def get_preprocessed_text(self) -> str:
        return self.preprocessed_text
    
    def add_tagged_ngram(self, tagged_ngram: TaggedNgram) -> None:
        self.tagged_ngrams.append(tagged_ngram)

    def set_tagged_ngrams(self, tagged_ngrams: List[TaggedNgram]) -> None:
        self.tagged_ngrams = tagged_ngrams

    def get_ngrams_with_tag(self, tag: str) -> List[TaggedNgram]:
        return [ngram for ngram in self.tagged_ngrams if ngram.get_tag() == tag]
    
    def get_ngrams_with_tags(self, tags: List[str]) -> List[TaggedNgram]:
        return [ngram for ngram in self.tagged_ngrams if ngram.get_tag() in tags]
    
    def add_relation(self, relation: Relation) -> None:
        self.relations.append(relation)

    def get_relations_of_type(self, relation: str) -> List[Relation]:
        return[rel for rel in self.relations if rel.get_relation() == relation]
    
    def get_relations(self) -> List[Relation]:
        return self.relations
    
    def get_tagged_ngrams_as_string(self, types) -> str:
        tagged_ngrams = ""
        for ngram in self.tagged_ngrams:
            if (ngram.get_tag() in types):
                tagged_ngrams += ngram.get_ngram() + "/" + ngram.get_tag() + ", "
        
        # # if the last characters are a comma and space, remove them
        if (tagged_ngrams[-2:] == ", "):
            tagged_ngrams = tagged_ngrams[:-2]
        return "[" + tagged_ngrams + "]"
    
    def filter_relations_on_source_or_target(self, allowed_ngrams) -> List[Relation]:
        ngrams = [ngram.get_ngram() for ngram in allowed_ngrams]
        return [relation for relation in self.relations if relation.get_source() in ngrams and relation.get_target() in ngrams]