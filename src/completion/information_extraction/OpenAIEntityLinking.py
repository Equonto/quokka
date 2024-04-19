
from typing import List, Union
from FileIo import FileIo
from completion.model.Models import PrompTemplate, PromptMessage

import openai
from dotenv import load_dotenv

class OpenAIEntityLinking:

    def __init__(self, template_path, open_ai_model_name):
        self.prompt_templates = self.read_prompt_templates(template_path)
        self.open_ai_model_name = open_ai_model_name

    def read_prompt_templates(self, template_path: str) -> PrompTemplate:
        return FileIo.read_json_prompt_templates(template_path)

    def load_api_key(self) -> Union[str, None]:
        load_dotenv('.env') 
        return "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" # todo: remove for final app

    def link_entity(self, text: str) -> str:
        self.wait(2) # todo: remove for final app
        
        for index, prompt in enumerate(self.prompt_templates):

            if index == 0:
                messages = self.replace_template_with_input(prompt.messages, prompt.template, text)
            else:
                pass

            json_messages = [message.get_json() for message in messages]
            try: 
                openai.api_key = self.load_api_key()
                response = openai.ChatCompletion.create(
                    model=self.open_ai_model_name,
                    messages = json_messages,
                    temperature = 0.001
                )
            except Exception as e:
                print('exception thrown on ChatCompletion')
                return None
        
            response_message = response["choices"][0]["message"] # type: ignore
            if index == len(self.prompt_templates) -1:
                return self.format_response(text, response_message.content)
            else:
                messages = self.replace_template_with_input(prompt.messages, prompt.template, response_message.content)
    
    def set_input(self, input: str):
        self.input = input

    def replace_template_with_input(self, messages: List[PromptMessage], template: str, input: str) -> List[PromptMessage]:
        output_messages = []
        for message in messages:
            new_message = PromptMessage(message.role, message.content)
            new_message.content = new_message.content.replace(template, input)
            output_messages.append(new_message)
        return output_messages
    
    def format_response(self, raw_text: str, response: str) -> str:
        if self.check_legal_linked_entity():
            return response
    
    def check_legal_linked_entity(self):
        return True

    # for debugging    
    def wait(self, number_of_seconds):
        import time
        time.sleep(number_of_seconds)


        

