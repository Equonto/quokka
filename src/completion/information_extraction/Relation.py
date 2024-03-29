

class Relation:

    def __init__(self, source: str, relation: str, target: str) -> None:
        self.source : str = source
        self.relation : str = relation
        self.target : str = target

    def get_source(self) -> str:
        return self.source
    
    def get_target(self) -> str:
        return self.target
    
    def get_relation(self) -> str:
        return self.relation
    
    def __str__(self) -> str:
        return self.source + "/" + self.relation + "/" + self.target

    def __eq__(self, other) -> bool:
        return self.source == other.source and self.relation == other.relation and self.target == other.target
