

from typing import List
from completion.information_extraction.Relation import Relation
from completion.information_extraction.OpenAIRunner import OpenAIRunner

class OpenAIRelationExtraction():

    def __init__(self, template_path, open_ai_model_name):
        self.open_ai_runner = OpenAIRunner(template_path, open_ai_model_name)

    def tag_relations(self, text: str, entities: str) -> List[Relation]:
        prompt_question = "Entities to use: " + entities + "\nContext: " + text 
        response = self.open_ai_runner.run_prompt_chain_from_template(prompt_question)
        return self.format_response(response)

    def format_response(self, response: str) -> List[Relation]:
        return self.interperet_string_as_list_of_relations(response)
    
    def interperet_string_as_list_of_relations(self, input:str) -> List[Relation]:
        relations = []
        if (input == "" or input == "[]" or "[" not in input):
            return []
        input = input.strip()
        input = input.replace("\n", "")
        input = input.replace("[", "")
        input = input.replace("]", "")
        input_list = input.split(",")
        for item in input_list:
            triple = item.split("\\")
            if (len(triple) != 3):
                print("Invalid triple: " + item)
                return []
            processed_triple = [self.remove_symbols(node).strip() for node in triple]
            relation = Relation(processed_triple[0], processed_triple[1], processed_triple[2])
            relations.append(relation)
        return relations

    def remove_symbols(self, text: str) -> str:
        symbols_to_replace = ["[", "]", ",", "'", "(", ")", "{", "}", ":", '"', "\n"]
        for symbol in symbols_to_replace:
            text = text.replace(symbol, "")
        return text.strip()


        

