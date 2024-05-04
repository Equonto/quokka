
from typing import List
from completion.information_extraction.TaggedNgram import TaggedNgram
from completion.information_extraction.TaggedSentence import TaggedSentence
from completion.information_extraction.OpenAIRunner import OpenAIRunner

class OpenAIEntityRecognition:

    def __init__(self, template_path, open_ai_model_name):
        self.open_ai_runner = OpenAIRunner(template_path, open_ai_model_name)

    def tag_text(self, text: str) -> TaggedSentence:
        response = self.open_ai_runner.run_prompt_chain_from_template(text)
        return self.format_response(text, response)
    
    def format_response(self, raw_text: str, response: str) -> TaggedSentence:
        tuples = self.interperet_string_as_list_of_tuples(response)
        return TaggedSentence(self.format_tuples_as_tagged_ngrams(tuples))
    
    def interperet_string_as_list_of_tuples(self, input: str) -> List[tuple]:
        if (input == "" or input == "[]" or "[" not in input):
            print(input)
            return []
        input = input.strip()
        input = input.replace("\n", "")
        input = input.replace("[", "")
        input = input.replace("]", "")

        input_list = input.split("},")
        input_list = [x + "}" for x in input_list] # re-add the closing bracket
        input_list = [tuple(x.split("\\")) for x in input_list]
        try:
            input_list = [(self.remove_symbols(x[0]), self.remove_symbols(x[1])) for x in input_list]
        except:
            print('exception thrown in input: '+ input)
            return []
        return input_list
    
    def format_tuples_as_tagged_ngrams(self, tuples: List[tuple]) -> List[TaggedNgram]:
        tagged_ngrams = []
        for tuple in tuples:
            tagged_ngrams.append(TaggedNgram(tuple[0], tuple[1]))
        return tagged_ngrams

    def remove_symbols(self, text: str) -> str:
        symbols_to_replace = ["[", "]", ",", "'", "(", ")", "{", "}", ":", '"', "\n"]
        for symbol in symbols_to_replace:
            text = text.replace(symbol, "")
        return text.strip()


        

