from enum import Enum

class ColumnType(Enum):
    IRI = 1,
    TEXT = 2,
    CONSTRUCTED_IRI = 3,
    CONSTRUCTED_TEXT = 4,
    LINKED_IRI = 3,
    LITERAL = 5

class ModelType(Enum):
    FLAIR = 1,
    OPENAI_NER = 2,
    OPENAI_RELATIONS = 3
    OPENAI_ENTITY_LINKING = 4

class TextPreprocessingTaskType(Enum):
    LOWER = 1,
    SPELLING_CORRECTION = 2,
    LEMMATIZATION = 3,
    STEMMING = 4,
    REMOVE_PUNCTUATION = 5
