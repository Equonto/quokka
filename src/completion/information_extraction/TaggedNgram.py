

class TaggedNgram:

    def __init__(self, ngram: str, tag: str) -> None:
        self.ngram : str = ngram
        self.tag : str = tag

    def get_ngram(self) -> str:
        return self.ngram
    
    def get_tag(self) -> str:
        return self.tag
    
    def __str__(self) -> str:
        return self.ngram + "/" + self.tag

    def __eq__(self, other) -> bool:
        return self.ngram == other.ngram and self.tag == other.tag
