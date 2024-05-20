from typing import List, Optional
from completion.model.Enums import ModelType
from completion.information_extraction.OpenAIRelations import OpenAIRelationExtraction
from completion.information_extraction.TaggedSentence import TaggedSentence

class RelationExtraction:

    def __init__(self, model_name: str, model_type: ModelType, template_path: Optional[str] = None):
        if model_type == ModelType.OPENAI_RELATIONS:
            self.tagger = OpenAIRelationExtraction(template_path, model_name)
        else :
            raise ValueError("Invalid model type: " + model_type)

    def tag_relations(self, pre_tagged_sentence: TaggedSentence) -> TaggedSentence:
        text = pre_tagged_sentence.get_preprocessed_text()
        entities = pre_tagged_sentence.get_tagged_ngrams_as_string(["ITEM", "ACTIVITY", "TOOL", "MATERIAL"]) # todo: remove hardcoding
        pre_tagged_sentence.relations = self.tagger.tag_relations(text, entities)
        ngrams = pre_tagged_sentence.get_ngrams_with_tags(["ITEM", "ACTIVITY", "TOOL", "MATERIAL"])
        pre_tagged_sentence.relations = pre_tagged_sentence.filter_relations_on_source_or_target(ngrams) # todo: remove hardcoding, exists becase openai sometimes returns relations with entities not in the input text
        return pre_tagged_sentence