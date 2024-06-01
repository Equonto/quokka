
from completion.information_extraction.OpenAIRunner import OpenAIRunner

class OpenAIEntityLinking:

    def __init__(self, template_path, open_ai_model_name):
        self.open_ai_runner = OpenAIRunner(template_path, open_ai_model_name)

    def link_entity(self, text: str) -> str:
        response = self.open_ai_runner.run_prompt_chain_from_template(text)
        return self.format_response(text, response)
    
    def format_response(self, raw_text: str, response: str) -> str:
        if self.check_legal_linked_entity():
            return response
