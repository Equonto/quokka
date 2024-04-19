



from typing import List, Union
from FileIo import FileIo
from completion.model.Models import PrompTemplate, PromptMessage
from completion.information_extraction.TaggedNgram import TaggedNgram
from completion.information_extraction.TaggedSentence import TaggedSentence
import openai
import os

class OpenAIRunner:

    def __init__(self, template_path, open_ai_model_name):
        self.prompt_templates = self.read_prompt_templates(template_path)
        self.open_ai_model_name = open_ai_model_name

    def read_prompt_templates(self, template_path: str) -> PrompTemplate:
        return FileIo.read_json_prompt_templates(template_path)

    def load_api_key(self) -> Union[str, None]:
        key = os.environ.get("OPENAI_API_KEY")
        return key
    
    def run_prompt_chain_from_template(self, prompt_question) -> str:
        self.wait(1)
        for index, prompt in enumerate(self.prompt_templates):

            if index == 0:
                messages = self.replace_template_with_input(prompt.messages, prompt.template, prompt_question)
            else:
                pass
            response_message = self.perform_completion(messages)
            if index == len(self.prompt_templates) -1:
                return response_message.content
            else:
                messages = self.replace_template_with_input(prompt.messages, prompt.template, response_message.content)
    
    def perform_completion(self, messages) -> str:
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
            return TaggedSentence([])
        return response["choices"][0]["message"] # type: ignore

    def set_input(self, input: str):
        self.input = input

    def replace_template_with_input(self, messages: List[PromptMessage], template: str, input: str) -> List[PromptMessage]:
        output_messages = []
        for message in messages:
            new_message = PromptMessage(message.role, message.content)
            new_message.content = new_message.content.replace(template, input)
            output_messages.append(new_message)
        return output_messages
    
    # for debugging    
    def wait(self, number_of_seconds):
        import time
        time.sleep(number_of_seconds)


        

