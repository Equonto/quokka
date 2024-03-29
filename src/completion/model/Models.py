from typing import List, Dict, Any, Optional, Union
from completion.Utils import Utils
from completion.model.Enums import ColumnType, TextPreprocessingTaskType, ModelType


class InformationExtractionModel:

    def __init__(self, name: str, type: ModelType, template_path: Optional[str]) -> None:
        self.name : str = name
        self.type : ModelType = type
        self.template_path : Optional[str] = template_path

    
    @staticmethod
    def from_json(json):
        template_path = None
        if Utils.attribute_exists(json, "template_path"):
            template_path = json["template_path"]
        return InformationExtractionModel(json["name"], ModelType[json["type"]], template_path)

class DataPreprocessingTask:

    def __init__(self, type: str, required_columns: Dict[str, str]) -> None:
        self.type : str = type
        self.required_columns : Dict[str, str] = required_columns
    
    @staticmethod
    def from_json(json):
        required_columns = {}
        for item in json["required_columns"]:
            if not item["key"] or not item["value"]:
                raise ValueError("Invalid data preprocessing task: " + json)
            required_columns[item["key"]] = item["value"]
        return DataPreprocessingTask(json["type"], required_columns)


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

class DataTransformationItem:

    def __init__(self, input_data_filepath: str, data_preprocessing_tasks: Optional[List[DataPreprocessingTask]]
                 , text_preprocessing_tasks: List[TextPreprocessingTaskType], ner_model: Optional[InformationExtractionModel]
                 , relationship_model: Optional[InformationExtractionModel]
                 , text_field: Optional[str], output_schema: List[OutputSchema], extraction_conditional_on_field: Optional[str]) -> None:
        self.input_data_filepath : str = input_data_filepath
        self.data_preprocessing_tasks : Optional[List[DataPreprocessingTask]] = data_preprocessing_tasks
        self.text_preprocessing_tasks : List[TextPreprocessingTaskType] = text_preprocessing_tasks
        self.ner_model : Optional[InformationExtractionModel] = ner_model
        self.relationship_model : Optional[InformationExtractionModel] = relationship_model
        self.text_field : Optional[str] = text_field
        self.output_schema : List[OutputSchema] = output_schema
        self.extraction_conditional_on_field : Optional[str] = extraction_conditional_on_field
    
    @staticmethod
    def from_json(json):
        data_preprocessing_tasks = []
        if Utils.attribute_exists(json, "data_preprocessing_tasks"):
            for item in json["data_preprocessing_tasks"]:
                data_preprocessing_tasks.append(DataPreprocessingTask.from_json(item))
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
        output_schema = []
        text_field = None
        if Utils.attribute_exists(json, "text_field"):
            text_field = json["text_field"]
        extraction_conditional_on_field = None
        if Utils.attribute_exists(json, "extraction_conditional_on_field"):
            extraction_conditional_on_field = json["extraction_conditional_on_field"]
        for item in json["output_schema"]:
            output_schema.append(OutputSchema.from_json(item))
        return DataTransformationItem(json["input_data_filepath"], data_preprocessing_tasks, text_preprocessing_tasks, ner_model, relationship_model, text_field, output_schema, extraction_conditional_on_field)

class CompletionConfig:

    def __init__(self, output_data_folder: str, prefix: str, data_transformation_items: List[DataTransformationItem]) -> None:
        self.output_data_folder : str = output_data_folder
        self.prefix : str = prefix
        self.data_transformation_items : List[DataTransformationItem] = data_transformation_items

    @staticmethod
    def from_json(json):
        data_transformation_items = []
        for item in json["data_transformation_items"]:
            data_transformation_items.append(DataTransformationItem.from_json(item))
        return CompletionConfig(json["output_data_folder"], json["prefix"], data_transformation_items)

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