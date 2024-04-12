from typing import List, Optional
from pandas import DataFrame, Series
from FileIo import FileIo
from completion.RelationExtraction import RelationExtraction
from completion.model.Config import Config
from completion.DataPreprocessor import DataPreprocessor
from completion.EntityRecognition import EntityRecognition
from completion.OutputSerializer import OutputSerializer
from completion.TextPreprocessor import TextPreprocessor
import numpy as np
from completion.model.Models import CompletionConfig, DataPreprocessingTask, DataTransformationItem, OutputSchema
from completion.information_extraction.TaggedSentence import TaggedSentence

class CompletionTask:

    def __init__(self, config_location: str, staging_dir: str):
        self.config: CompletionConfig = Config(config_location).config
        self.staging_dir: str = staging_dir
    
    def setup(self):
        FileIo.clear_directory(self.config.output_data_folder)
        FileIo.create_directory(self.staging_dir)
        FileIo.clear_directory(self.staging_dir)
    
    def cleanup(self):
        FileIo.delete_directory(self.staging_dir)
    
    def execute(self):
        self.setup()
        # todo: update to handle separated configuration files
        for data_transformation_item in self.config.data_transformation_items:
            input_data : DataFrame = FileIo.read_csv(data_transformation_item.input_data_filepath)
            if data_transformation_item.data_preprocessing_tasks != None and len(data_transformation_item.data_preprocessing_tasks) > 0:
                input_data = self.perform_data_preprocessing(data_transformation_item.data_preprocessing_tasks, input_data, data_transformation_item.input_data_filepath)
            tagged_sentences = self.perform_entity_recognition(data_transformation_item, input_data)
            self.perform_output_serialization(self.config.prefix, self.config.output_data_folder
                                              , input_data, data_transformation_item.output_schema, tagged_sentences)
        self.cleanup()

    def perform_data_preprocessing(self
                                   , data_preprocessing_tasks: List[DataPreprocessingTask]
                                   , input_data: DataFrame
                                   , input_data_filepath: str) -> DataFrame:
            input_data = DataPreprocessor(input_data, data_preprocessing_tasks).run()    
            # TODO: set as debug only (environment)
            data_filename = input_data_filepath.split("/")[-1]
            FileIo.write_csv(np.vstack([input_data.columns, input_data.values]), "staging/" + data_filename)
            return input_data

    def perform_entity_recognition(self
                                   , data_transformation_item: DataTransformationItem
                                   , input_data: DataFrame) -> List[TaggedSentence]:
            tagged_sentences : List[TaggedSentence] = []
            if data_transformation_item.ner_model != None:
                entity_recognition = EntityRecognition(data_transformation_item.ner_model.name, 
                                                       data_transformation_item.ner_model.type,
                                                       data_transformation_item.ner_model.template_path)
                for index, row in input_data.iterrows():
                    if (data_transformation_item.text_field != None):
                        text = row[data_transformation_item.text_field] # warn dynamic code
                        if (data_transformation_item.data_preprocessing_tasks != None):
                            text_preprocessor = TextPreprocessor(data_transformation_item.text_preprocessing_tasks)
                            text = text_preprocessor.preprocess_text(text) 

                        # if the row passes the condition in the config, then extract entities
                        if self.pass_condition(data_transformation_item.extraction_conditional_on_field, row):
                            tagged_sentence = entity_recognition.tag_text(text)
                            tagged_sentence.set_preprocessed_text(text) 
                            tagged_sentence.set_raw_input_data(row) # need this for formatting output object
                            # relations can only be extracted if entities extracted
                            if (data_transformation_item.relationship_model != None and tagged_sentence.get_tagged_ngrams() != []):
                                relationship_extraction = RelationExtraction(data_transformation_item.relationship_model.name,
                                                                                data_transformation_item.relationship_model.type,
                                                                                data_transformation_item.relationship_model.template_path)
                                tagged_sentence = relationship_extraction.tag_relations(tagged_sentence)
                            tagged_sentences.append(tagged_sentence)
            FileIo.write_tagged_sentences_to_txt_file(tagged_sentences, "data/analysis/tagged_sentences.txt") # for analysis
            FileIo.write_tagged_relations_to_txt_file(tagged_sentences, "data/analysis/tagged_relations.txt") # for analysis
            FileIo.write_preprocessed_txt_to_txt_file(tagged_sentences, "data/analysis/preprocessed_texts.txt") # for analysis
            return tagged_sentences
    
    def perform_output_serialization(self, prefix: str, output_data_folder: str, data: DataFrame
                                     , output_schema : List[OutputSchema], tagged_sentences : List[TaggedSentence]) -> None:
            serialized_files_as_dict = OutputSerializer(prefix, data, output_schema, tagged_sentences).get_serialized_dictionary()
            FileIo.write_dict_to_csvs(output_data_folder, serialized_files_as_dict, output_schema)

    def pass_condition(self, extraction_conditional_on_field: Optional[str], row: Series) -> bool:
        if (extraction_conditional_on_field != None):
            if (row[extraction_conditional_on_field] == None or row[extraction_conditional_on_field] == "" or row[extraction_conditional_on_field] == False):
                return False
        return True