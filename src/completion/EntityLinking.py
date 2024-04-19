from typing import List, Optional
from completion.model.Enums import ModelType
from completion.information_extraction.OpenAIEntityLinking import OpenAIEntityLinking
from completion.information_extraction.TaggedSentence import TaggedSentence

class EntityLinking:

    def __init__(self, model_name: str, model_type: ModelType, entity: str, template_path: Optional[str] = None):
        self.entity = entity
        if model_type == ModelType.OPENAI_ENTITY_LINKING:
            self.tagger = OpenAIEntityLinking(template_path, model_name)
        else :
            raise ValueError("Invalid model type: " + model_type)

    def link_entities(self, pre_tagged_sentence: TaggedSentence) -> TaggedSentence:
        tagged_ngrams = pre_tagged_sentence.get_tagged_ngrams()
        for tagged_ngram in tagged_ngrams:
            if (tagged_ngram.get_tag() == self.entity):
                linked_entity = self.tagger.link_entity(tagged_ngram.get_ngram())
                tagged_ngram.add_linked_entity(linked_entity)
        pre_tagged_sentence.set_tagged_ngrams(tagged_ngrams)
        return pre_tagged_sentence