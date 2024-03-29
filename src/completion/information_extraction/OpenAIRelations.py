

from typing import List, Union
from FileIo import FileIo
from completion.information_extraction.Relation import Relation
from completion.model.Models import PrompTemplate, PromptMessage
from completion.information_extraction.TaggedNgram import TaggedNgram
from completion.information_extraction.TaggedSentence import TaggedSentence
import openai
import os
from dotenv import load_dotenv

class OpenAIRelationExtraction():
    
    def __init__(self, template_path, open_ai_model_name):
        self.prompt_template = self.read_prompt_template(template_path)
        self.open_ai_model_name = open_ai_model_name
        openai.api_key = self.load_api_key()

    def read_prompt_template(self, template_path: str) -> PrompTemplate:
        return FileIo.read_json_prompt_template(template_path)

    def load_api_key(self) -> Union[str, None]:
        load_dotenv('.env') 
        return os.getenv("OPENAI_API_KEY")

    def tag_relations(self, text: str, entities: str) -> List[Relation]:
        self.wait(2) # todo: remove for final app
        prompt_question = "Entities to use: " + entities + "\nContext: " + text 
        messages = self.replace_template_with_input(self.prompt_template.messages
                                                    , self.prompt_template.template
                                                    , prompt_question)
        json_messages = [message.get_json() for message in messages]
        try: 
            response = openai.ChatCompletion.create(
               model=self.open_ai_model_name,
               messages = json_messages,
               temperature = 0.001
            )
            response_message = response["choices"][0]["message"] # type: ignore
            return self.format_response(text, response_message.content)
        except:
            print('exception thrown on ChatComplation')
            return []

    def replace_template_with_input(self, messages: List[PromptMessage], template: str, input: str) -> List[PromptMessage]:
        output_messages = []
        for message in messages:
            new_message = PromptMessage(message.role, message.content)
            new_message.content = new_message.content.replace(template, input)
            output_messages.append(new_message)
        return output_messages
    
    def format_response(self, raw_text: str, response: str) -> List[Relation]:
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

    # for debugging    
    def wait(self, number_of_seconds):
        import time
        time.sleep(number_of_seconds)


        

