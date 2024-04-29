from typing import List, Dict, Any, Optional, Union
from completion.Utils import Utils
from completion.model.Enums import ColumnType, TextPreprocessingTaskType, ModelType

class InformationExtractionModel:

    def __init__(self, name: str, type: ModelType, template_path: Optional[str], entity: Optional[str] = None) -> None:
        self.name : str = name
        self.type : ModelType = type
        self.template_path : Optional[str] = template_path
        self.entity : Optional[str] = entity

    
    @staticmethod
    def from_json(json):
        template_path = None
        if Utils.attribute_exists(json, "template_path"):
            template_path = json["template_path"]
        entity = None
        if Utils.attribute_exists(json, "entity"):
            entity = json["entity"]
        return InformationExtractionModel(json["name"], ModelType[json["type"]], template_path=template_path, entity=entity)


class OutputColumn:

    def __init__(self, name: str, type: ColumnType, template: str) -> None:
        self.name : str = name
        self.type : ColumnType = type
        self.template : str = template
    
    @staticmethod
    def from_json(json):
        return OutputColumn(json["name"], ColumnType[json["type"]], json["template"])

class OutputSchema:

    def __init__(self, filename: str, extractable_from_entity: Optional[str], extractable_from_relation: Optional[str], columns: List[OutputColumn]) -> None:
        self.filename : str = filename
        self.extractable_from_entity : Optional[str] = extractable_from_entity
        self.extractable_from_relation : Optional[str] = extractable_from_relation
        self.columns : List[OutputColumn] = columns

    @staticmethod
    def from_json(json):
        columns = []
        for item in json["columns"]:
            columns.append(OutputColumn.from_json(item))
        extractable_from_entity = None
        if Utils.attribute_exists(json, "extractable_from_entity"):
            extractable_from_entity = json["extractable_from_entity"]
        extractable_from_relation = None
        if Utils.attribute_exists(json, "extractable_from_relation"):
            extractable_from_relation = json["extractable_from_relation"]
        return OutputSchema(json["filename"], extractable_from_entity, extractable_from_relation, columns)

class InformationExtractionDetails:

    def __init__(self,
                   text_preprocessing_tasks: List[TextPreprocessingTaskType], ner_model: Optional[InformationExtractionModel]
                 , relationship_model: Optional[InformationExtractionModel]
                 , entity_linking_models: Optional[List[InformationExtractionModel]]
                 , text_field: Optional[str], extraction_conditional_on_field: Optional[str]) -> None:
            self.text_preprocessing_tasks : List[TextPreprocessingTaskType] = text_preprocessing_tasks
            self.ner_model : Optional[InformationExtractionModel] = ner_model
            self.relationship_model : Optional[InformationExtractionModel] = relationship_model
            self.entity_linking_models : Optional[List[InformationExtractionModel]] = entity_linking_models
            self.text_field : Optional[str] = text_field
            self.extraction_conditional_on_field : Optional[str] = extraction_conditional_on_field

    @staticmethod
    def from_json(json):
        text_preprocessing_tasks = []
        if Utils.attribute_exists(json, "text_preprocessing_tasks"):
            for item in json["text_preprocessing_tasks"]:
                text_preprocessing_tasks.append(TextPreprocessingTaskType[item])
        ner_model = None
        if Utils.attribute_exists(json, "ner_model"):
            ner_model = InformationExtractionModel.from_json(json["ner_model"])
        relationship_model = None
        if Utils.attribute_exists(json, "relationship_model"):
            relationship_model = InformationExtractionModel.from_json(json["relationship_model"])
        text_field = None
        entity_linking_models = None
        if Utils.attribute_exists(json, "entity_linking_models"):
            entity_linking_models = []
            for item in json["entity_linking_models"]:
                entity_linking_models.append(InformationExtractionModel.from_json(item))
        if Utils.attribute_exists(json, "text_field"):
            text_field = json["text_field"]
        extraction_conditional_on_field = None
        if Utils.attribute_exists(json, "extraction_conditional_on_field"):
            extraction_conditional_on_field = json["extraction_conditional_on_field"]
        return InformationExtractionDetails(text_preprocessing_tasks, ner_model, relationship_model, entity_linking_models, text_field, extraction_conditional_on_field)


class CompletionConfig:

    def __init__(self, config_name: str, prefix: str, output_schemas: List[OutputSchema], information_extraction_details: List[InformationExtractionDetails]) -> None:
        self.config_name : str = config_name
        self.prefix : str = prefix
        self.information_extraction_details : List[InformationExtractionDetails] = information_extraction_details
        self.output_schema : List[OutputSchema] = output_schemas


    @staticmethod
    def from_json(json):
        information_extraction_details = None
        if Utils.attribute_exists(json, "information_extraction_details"):
            information_extraction_details = InformationExtractionDetails.from_json(json["information_extraction_details"])
        output_schemas = []
        if Utils.attribute_exists(json, "output_schema"):
            for item in json["output_schema"]:
                output_schemas.append(OutputSchema.from_json(item))
        return CompletionConfig(json["config_name"], json["prefix"], output_schemas, information_extraction_details)

class PromptMessage:

    def __init__(self, role: str, content: Union[List[str], str]) -> None:
        self.role : str = role
        if isinstance(content, list):
            self.content : str = '\n'.join(content)
        else:
            self.content : str = content

    
    @staticmethod
    def from_json(json):
        return PromptMessage(json["role"], json["content"])
    
    def get_json(json):
        return {
            "role": json.role,
            "content": json.content
        }

class PrompTemplate:

    def __init__(self, template: str, messages: List[PromptMessage]) -> None:
        self.template : str = template
        self.messages : List[PromptMessage] = messages
    
    @staticmethod
    def from_json(json):
        messages = []
        for item in json["messages"]:
            messages.append(PromptMessage.from_json(item))
        return PrompTemplate(json["template"], messages)