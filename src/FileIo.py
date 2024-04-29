from typing import Dict, List
import pandas as pd
import csv
import json
import os
import glob
import shutil
from types import SimpleNamespace

from completion.model.Models import CompletionConfig, OutputSchema, PrompTemplate
from completion.information_extraction.TaggedSentence import TaggedSentence

class FileIo:
    
    @staticmethod
    def read_csv(file_path):
        return pd.read_csv(file_path, header=0, encoding='utf-8') 
    
    @staticmethod
    def write_csv(csv_data, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in csv_data:
                row = ["" if pd.isna(value) else value for value in row]
                csv_writer.writerow(row)
    
    @staticmethod
    def read_txt(file_path) -> List[str]:
        lines = []
        with open(file_path, 'r') as f:
            for line in f:
                lines.append(line.strip())
        return lines
    
    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
        
    @staticmethod
    def read_json_prompt_templates(file_path) -> List[PrompTemplate]:
        with open(file_path, 'r') as f:
            loaded_json = json.load(f)
            return [PrompTemplate.from_json(item) for item in loaded_json]

    @staticmethod
    def read_json_config(file_path) -> CompletionConfig:
        with open(file_path, 'r') as f:
            loaded_json = json.load(f)
            return CompletionConfig.from_json(loaded_json)
    
    @staticmethod
    def write_json_to_file(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def write_dict_to_csvs(file_location: str, data_dict: Dict[str, List[SimpleNamespace]], schema: List[OutputSchema]):    
        for filename, list in data_dict.items():
            with open(f'{file_location}/{filename}', 'w', newline='') as f:
                writer = csv.writer(f)
                if (len(list) == 0): # if there is no data, get the headers from the config file
                    headers = []
                    for d in schema:
                        if d.filename == filename:
                            for col in d.columns:
                                headers.append(col.name)
                    writer.writerow(headers) 
                else:
                    writer.writerow(list[0].keys())
                for item in list:
                    writer.writerow(item.values())
 
    @staticmethod
    def clear_directory(folder_location) -> None:
        files = glob.glob(folder_location+"/*")
        for f in files:
            os.remove(f)

    @staticmethod
    def create_directory(folder_location) -> None:
        if not os.path.exists(folder_location):
            os.makedirs(folder_location)
    
    @staticmethod
    def move_files(src_folder, dst_folder):
        files = glob.glob(src_folder+"/*")
        for f in files:
            shutil.copy(f, dst_folder)
    
    @staticmethod
    def delete_directory(folder_location) -> None:
        shutil.rmtree(folder_location)
    
    @staticmethod
    def get_file_names(folder_location):
        return glob.glob(folder_location+"/*")

    # methods for analysis
    @staticmethod 
    def write_tagged_sentences_to_txt_file(list: List[TaggedSentence], file_path: str):
        with open(file_path, 'w') as f:
            for item in list:
                f.write("Raw Text:" +  item.get_raw_input_data()["text_value"] + '\n')
                f.write("Preprocessed Text:" +  item.get_preprocessed_text() + '\n')
                tagged_ngram_string = ""
                for ngram in item.get_tagged_ngrams():
                    tagged_ngram_string += str(ngram) + ", "
                f.write(tagged_ngram_string + "\n\n")

        # also write to csv where column 1 is preprocessed text and column 2 is tagged ngrams
        with open(file_path.replace(".txt", ".csv"), 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["preprocessed_text", "tagged_ngrams"])
            for item in list:
                tagged_ngram_string = ""
                for ngram in item.get_tagged_ngrams():
                    tagged_ngram_string += str(ngram) + ", "
                csv_writer.writerow([item.get_preprocessed_text(), tagged_ngram_string])

    @staticmethod
    def write_tagged_relations_to_txt_file(list: List[TaggedSentence], file_path: str):
        with open(file_path, 'w') as f:
            for item in list:
                f.write("Raw Text:" +  item.get_raw_input_data()["text_value"] + '\n')
                f.write("Preprocessed Text:" +  item.get_preprocessed_text() + '\n')
                tagged_relation_string = ""
                for relation in item.get_relations(): # todo: remove hardcoding
                    tagged_relation_string += str(relation) + ", "
                f.write(tagged_relation_string + "\n\n")

        # also write to csv where column 1 is preprocessed text and column 2 is tagged relations
        with open(file_path.replace(".txt", ".csv"), 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["preprocessed_text", "tagged_relations"])
            for item in list:
                tagged_relation_string = ""
                for relation in item.get_relations():
                    tagged_relation_string += str(relation) + ", "
                csv_writer.writerow([item.get_preprocessed_text(), tagged_relation_string])        

    @staticmethod
    def write_preprocessed_txt_to_txt_file(list: List[TaggedSentence], file_path: str):
        with open(file_path, 'w') as f:
            for item in list:
                f.write(item.get_preprocessed_text() + '\n')

