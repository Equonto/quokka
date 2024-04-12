
from FileIo import FileIo
from completion.model.Models import CompletionConfig

class Config:

    def __init__(self, input_files_location: str, config_location: str) -> list[CompletionConfig]:
        self.configs : list[CompletionConfig] = self.load_configuation_files(self.read_input_CSV_names(input_files_location), config_location)

    def read_input_CSV_names(self, input_files_location: str) -> list[str]:
        input_csv_names = []
        filenames = FileIo.get_file_names(input_files_location)
        for filename in filenames:
            if filename.endswith('.csv'):
                input_csv_names.append(filename.replace('.csv', ''))
        return input_csv_names
    
    def load_configuation_files(self, input_csv_names: list[str], config_location) -> list[CompletionConfig]:
        return [self.load(f'{config_location}/config-{input_csv_name}.json') for input_csv_name in input_csv_names]
    
    def load(self, config_path: str) -> CompletionConfig:
       return FileIo.read_json_config(config_path)
    
    # todo: write config validation (and handle errors if configuration files don't exist)