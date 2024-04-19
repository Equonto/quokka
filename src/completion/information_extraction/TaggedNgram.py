from typing import Optional

class TaggedNgram:

    def __init__(self, ngram: str, tag: str, linked_entity: Optional[str] = None) -> None:
        self.ngram : str = ngram
        self.tag : str = tag
        self.linked_entity : str = linked_entity

    def get_ngram(self) -> str:
        return self.ngram
    
    def get_tag(self) -> str:
        return self.tag
    
    def add_linked_entity(self, linked_entity: str) -> None:
        if linked_entity != None and linked_entity.strip() != "":
            self.linked_entity = linked_entity

    def get_linked_entity(self) -> Optional[str]:
        return self.linked_entity
    
    def __str__(self) -> str:
        return self.ngram + "/" + self.tag

    def __eq__(self, other) -> bool:
        return self.ngram == other.ngram and self.tag == other.tag
