from typing import Optional
from completion.model.Enums import ModelType
from completion.information_extraction.OpenAINer import OpenAIEntityRecognition
from completion.information_extraction.Flair import FlairEntityRecognition
from completion.information_extraction.TaggedSentence import TaggedSentence

class EntityRecognition:

    def __init__(self, model_name: str, model_type: ModelType, template_path: Optional[str] = None):
        if model_type == ModelType.FLAIR:
            self.tagger = FlairEntityRecognition()
            self.tagger.load(model_name)
        elif model_type == ModelType.OPENAI_NER:
            self.tagger = OpenAIEntityRecognition(template_path, model_name)
        elif model_type == ModelType.OPENAI_RELATIONS:
            raise ValueError("Relation extraction model incorrectly used for entity recognition")
        else :
            raise ValueError("Invalid model type: " + model_type)


    def tag_text(self, text: str) -> TaggedSentence:
        return self.tagger.tag_text(text)


    