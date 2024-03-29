
from FileIo import FileIo
from completion.model.Models import CompletionConfig

class Config:

    def __init__(self, config_path: str):
        self.config : CompletionConfig = self.load(config_path)

    def load(self, config_path: str) -> CompletionConfig:
       return FileIo.read_json_config(config_path)
    
    # todo: write config validation