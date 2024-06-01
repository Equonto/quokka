
import re
from types import SimpleNamespace
from typing import Dict, List, Union
from pandas import DataFrame, Series
from completion.Utils import Utils
from completion.model.Enums import ColumnType
from completion.model.Models import OutputColumn, OutputSchema
from completion.information_extraction.TaggedNgram import TaggedNgram

from completion.information_extraction.TaggedSentence import TaggedSentence

class OutputSerializer:

    def __init__(self, prefix : str, input_data: DataFrame, output_schema : List[OutputSchema], tagged_sentences : List[TaggedSentence] ):

        self.prefix : str = prefix
        self.input_data : DataFrame = input_data
        self.output_schema : List[OutputSchema] = output_schema
        self.tagged_sentences : List[TaggedSentence] = tagged_sentences
        self.output_dict : Dict[str, List[SimpleNamespace]] = {}
        for output_item in self.output_schema:
            self.populate_data_structure(output_item)

    def get_serialized_dictionary(self) -> Dict[str, List[SimpleNamespace]]:
        return self.output_dict
    
    def populate_data_structure(self, data_structure: OutputSchema) -> None:
        if data_structure.extractable_from_entity != None:
            self.populate_extractable_data_structure(data_structure)
            pass
        elif data_structure.extractable_from_relation != None:
            self.populate_extractable_data_structure(data_structure)
            pass
        else:
            self.populate_non_extractable_data_structure(data_structure)

    def populate_extractable_data_structure(self, data_structure: OutputSchema) -> None:
        output_list = []
        for tagged_sentence in self.tagged_sentences:
            if (data_structure.extractable_from_entity != None):
                extracted_items = tagged_sentence.get_ngrams_with_tag(data_structure.extractable_from_entity)
                for (index, extracted_item) in enumerate(extracted_items):
                        output = {}
                        for column in data_structure.columns:
                            output[column.name] = self.create_value( tagged_sentence.get_raw_input_data()
                                                                    , column
                                                                    , extracted_item
                                                                    , index + 1)
                            output_list.append(output)
                self.output_dict[data_structure.filename] = Utils.make_objects_in_list_unique(output_list)
            if (data_structure.extractable_from_relation != None):
                extracted_relations = tagged_sentence.get_relations_of_type(data_structure.extractable_from_relation)
                for (index, extracted_relation) in enumerate(extracted_relations):
                           output = {}
                           for (index, column) in enumerate(data_structure.columns):
                                if (index == 0):
                                    output[column.name] = self.create_value( tagged_sentence.get_raw_input_data()
                                                                            , column
                                                                            , extracted_relation.get_source()
                                                                            , index + 1)
                                if (index == 1):
                                    output[column.name] = self.create_value( tagged_sentence.get_raw_input_data()
                                                                            , column)
                                if (index == 2):
                                    output[column.name] = self.create_value( tagged_sentence.get_raw_input_data()
                                                                            , column
                                                                            , extracted_relation.get_target()
                                                                            , index + 1)
                                output_list.append(output)
        self.output_dict[data_structure.filename] = Utils.make_objects_in_list_unique(output_list)
                                
    def populate_non_extractable_data_structure(self, data_structure: OutputSchema) -> None:
        output_list = []
        for index, row in self.input_data.iterrows():
            output = {}
            for column in data_structure.columns:
                output[column.name] = self.create_value(row, column)
            output_list.append(output)
        self.output_dict[data_structure.filename] = Utils.make_objects_in_list_unique(output_list)

    def create_value(self, row: Series, column: OutputColumn, extracted_item: Union[TaggedNgram, str] = None, extracted_item_number = None):
            columnType = column.type
            template = column.template
            if (columnType == ColumnType.IRI): 
                return self.prefix + self.get_value(row, template) if (self.get_value(row, template)  != "") else None
            elif (columnType == ColumnType.TEXT):
                val = self.get_value(row, template)
                return val
            elif (columnType == ColumnType.CONSTRUCTED_IRI):
                    val = self.create_constructed_value(row, template, extracted_item, column, extracted_item_number)
                    return self.prefix + val if (val != None) else None
            elif (columnType == ColumnType.CONSTRUCTED_TEXT):
                    return self.create_constructed_value(row, template, extracted_item, column)
            elif (columnType == ColumnType.LITERAL):
                    return template
            elif (columnType == ColumnType.LINKED_IRI):
                    val = self.create_constructed_value(row, template, extracted_item, column)
                    return self.prefix + val if (val != None) else None 
            else:
                raise ValueError("Unknown column type: " + str(columnType)) 
            
    def create_constructed_value(self, row: Series, template: str, extracted_item: Union[TaggedNgram, str], column: OutputColumn, extracted_item_number = None):
        
        raw_templates = re.findall('\{([^}]+)\}', template)
        for temp in raw_templates:
            if temp != "EXTRACTED" and temp != "EXTRACTED(F)" and temp != "EXTRACTED(C)" and temp != "LINKED":
                val = self.get_value(row, temp)
                if val is not None:
                    template = template.replace("{" + temp + "}", val)
                
            else:
                if isinstance(extracted_item, str):
                    if temp == "EXTRACTED" and extracted_item != None:
                        template = template.replace("{" + temp + "}", 
                            self.get_tagged_value(extracted_item, False, extracted_item_number))
                    if temp == "EXTRACTED(F)" and extracted_item != None:
                        template = template.replace("{" + temp + "}", 
                            self.get_tagged_value(extracted_item, True, extracted_item_number))
                else:
                    if temp == "EXTRACTED" and extracted_item.get_ngram() != None:
                        template = template.replace("{" + temp + "}", 
                            self.get_tagged_value(extracted_item.get_ngram(), False, extracted_item_number))
                    if temp == "EXTRACTED(F)" and extracted_item.get_ngram() != None:
                        template = template.replace("{" + temp + "}", 
                            self.get_tagged_value(extracted_item.get_ngram(), True, extracted_item_number))
                    if temp == "LINKED" and extracted_item.get_linked_entity() != None:
                        template = template.replace("{" + temp + "}", 
                            self.get_tagged_value(extracted_item.get_linked_entity(), True))
        return template

    def get_value(self, row: Series, template: str) -> str:
        if row[template] != None and str(row[template]) != "nan":
             return str(row[template])
        return "" 
    
    def get_tagged_value(self, extracted_item: str, formatted: bool, extracted_item_number = None):
        if formatted:
             extracted_item = extracted_item.replace(" ", "_").lower()
        return extracted_item