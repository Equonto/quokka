from typing import List, Optional
from pandas import DataFrame, Series
from FileIo import FileIo
from completion.RelationExtraction import RelationExtraction
from completion.EntityLinking import EntityLinking
from completion.model.Config import Config
from completion.EntityRecognition import EntityRecognition
from completion.OutputSerializer import OutputSerializer
from completion.TextPreprocessor import TextPreprocessor
from completion.model.Models import CompletionConfig, OutputSchema, InformationExtractionDetails
from completion.information_extraction.TaggedSentence import TaggedSentence

class CompletionTask:

    def __init__(self, input_data_folder: str, output_data_folder: str, config_location: str, staging_dir: str):
        self.input_data_folder: str = input_data_folder
        self.output_data_folder: str = output_data_folder
        self.config_files: List[CompletionConfig] = Config(input_data_folder, config_location).configs
        self.staging_dir: str = staging_dir
    
    def setup(self):
        FileIo.clear_directory(self.output_data_folder)
        FileIo.create_directory(self.staging_dir)
        FileIo.clear_directory(self.staging_dir)
    
    def cleanup(self):
        FileIo.delete_directory(self.staging_dir)
    
    def execute(self):
        self.setup()
        for config in self.config_files:
            input_data : DataFrame = FileIo.read_csv(self.input_data_folder + config.config_name + ".csv")
            tagged_sentences = None
            if (config.information_extraction_details != None):
                tagged_sentences = self.perform_entity_recognition(config.information_extraction_details, input_data)
            self.perform_output_serialization(config.prefix, self.output_data_folder
                                                    , input_data, config.output_schema, tagged_sentences)
        self.cleanup()

    def perform_entity_recognition(self
                                   , ie_details: InformationExtractionDetails
                                   , input_data: DataFrame) -> List[TaggedSentence]:
            tagged_sentences : List[TaggedSentence] = []
            if ie_details.ner_model != None:

                for index, row in input_data.iterrows():
                    if (ie_details.text_field != None):
                        text = row[ie_details.text_field] # warn dynamic code
                        # if the row is a candidate for extraction, then extract entities
                        if self.pass_condition(ie_details.extraction_conditional_on_field, row):
                            print(row)
                            
                            if (ie_details.text_preprocessing_tasks != None):
                                 text = self.run_preprocessing_tasks(text, ie_details.text_preprocessing_tasks)
                                
                            tagged_sentence = self.run_ner_model(ie_details.ner_model, text, row)
                            
                            # relations can only be extracted if entities extracted
                            if (ie_details.relationship_model != None and tagged_sentence.get_tagged_ngrams() != []):
                                tagged_sentence = self.run_relation_model(ie_details.relationship_model, tagged_sentence)
                            
                            # if entity linking models exist
                            if (ie_details.entity_linking_models != None and tagged_sentence.get_tagged_ngrams() != []):
                                for model in ie_details.entity_linking_models:
                                    tagged_sentence = self.run_entity_linking_model(model, tagged_sentence)

                            tagged_sentences.append(tagged_sentence)
            
            self.write_to_analysis_folder(tagged_sentences) # for debugging
            return tagged_sentences
    
    def run_preprocessing_tasks(self, text, text_preprocessing_tasks) -> str:
        text_preprocessor = TextPreprocessor(text_preprocessing_tasks)
        return text_preprocessor.preprocess_text(text) 
    
    def run_ner_model(self, ner_model, text, row) -> TaggedSentence:
        entity_recognition = EntityRecognition(ner_model.name, 
                                ner_model.type,
                                ner_model.template_path)
        tagged_sentence = entity_recognition.tag_text(text)
        tagged_sentence.set_preprocessed_text(text) 
        tagged_sentence.set_raw_input_data(row) # need this for formatting output object
        return tagged_sentence

    def run_relation_model(self, relationship_model, tagged_sentence) -> TaggedSentence:
        relationship_extraction = RelationExtraction(relationship_model.name,
            relationship_model.type,
            relationship_model.template_path)
        return relationship_extraction.tag_relations(tagged_sentence)

    def run_entity_linking_model(self, entity_linking_model, tagged_sentence) -> TaggedSentence:
        entity_linking = EntityLinking(entity_linking_model.name
                                       , entity_linking_model.type
                                       , entity_linking_model.entity
                                       , entity_linking_model.template_path)
        return entity_linking.link_entities(tagged_sentence) 
    
    def perform_output_serialization(self, prefix: str, output_data_folder: str, data: DataFrame
                                     , output_schema : List[OutputSchema], tagged_sentences : List[TaggedSentence]) -> None:
            serialized_files_as_dict = OutputSerializer(prefix, data, output_schema, tagged_sentences).get_serialized_dictionary()
            FileIo.write_dict_to_csvs(output_data_folder, serialized_files_as_dict, output_schema)


    def pass_condition(self, extraction_conditional_on_field: Optional[str], row: Series) -> bool:
        if (extraction_conditional_on_field != None):
            if (row[extraction_conditional_on_field] == None or row[extraction_conditional_on_field] == "" or row[extraction_conditional_on_field] == False):
                return False
        return True
    
    # for debugging
    def write_to_analysis_folder(self, tagged_sentences):
            FileIo.write_tagged_sentences_to_txt_file(tagged_sentences, "data/analysis/tagged_sentences.txt") 
            FileIo.write_tagged_relations_to_txt_file(tagged_sentences, "data/analysis/tagged_relations.txt") 
            FileIo.write_preprocessed_txt_to_txt_file(tagged_sentences, "data/analysis/preprocessed_texts.txt") 
