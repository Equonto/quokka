
from typing import List, Union
from FileIo import FileIo
from completion.model.Models import PrompTemplate, PromptMessage
from completion.information_extraction.TaggedNgram import TaggedNgram
from completion.information_extraction.TaggedSentence import TaggedSentence
import openai
import os
from dotenv import load_dotenv

class OpenAIEntityRecognition:

    def __init__(self, template_path, open_ai_model_name):
        self.prompt_template = self.read_prompt_template(template_path)
        self.open_ai_model_name = open_ai_model_name
        openai.api_key = self.load_api_key()

    def read_prompt_template(self, template_path: str) -> PrompTemplate:
        return FileIo.read_json_prompt_template(template_path)

    def load_api_key(self) -> Union[str, None]:
        load_dotenv('.env') 
        return os.getenv("OPENAI_API_KEY")

    def tag_text(self, text: str) -> TaggedSentence:
        self.wait(2) # todo: remove for final app
        messages = self.replace_template_with_input(self.prompt_template.messages, self.prompt_template.template, text)
        json_messages = [message.get_json() for message in messages]
        try: 
            response = openai.ChatCompletion.create(
                model=self.open_ai_model_name,
                messages = json_messages,
                temperature = 0.001
            )
        except:
            print('exception thrown on ChatComplation')
            return TaggedSentence([])
        response_message = response["choices"][0]["message"] # type: ignore
        return self.format_response(text, response_message.content)

    def replace_template_with_input(self, messages: List[PromptMessage], template: str, input: str) -> List[PromptMessage]:
        output_messages = []
        for message in messages:
            new_message = PromptMessage(message.role, message.content)
            new_message.content = new_message.content.replace(template, input)
            output_messages.append(new_message)
        return output_messages
    
    def format_response(self, raw_text: str, response: str) -> TaggedSentence:
        tuples = self.interperet_string_as_list_of_tuples(response)
        return TaggedSentence(self.format_tuples_as_tagged_ngrams(tuples))
    
    def interperet_string_as_list_of_tuples(self, input: str) -> List[tuple]:
        if (input == "" or input == "[]" or "[" not in input):
            return []
        input = input.strip()
        input = input.replace("\n", "")
        input = input.replace("[", "")
        input = input.replace("]", "")
        input_list = input.split(",")
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

    # for debugging    
    def wait(self, number_of_seconds):
        import time
        time.sleep(number_of_seconds)


        

