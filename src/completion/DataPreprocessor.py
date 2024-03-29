
from nltk.tokenize import sent_tokenize
import uuid
import pandas as pd

class DataPreprocessor:

    # todo: clean
    def __init__(self, data, data_preprocessing_tasks):
        self.data = data
        self.data_preprocessing_tasks = data_preprocessing_tasks

    def run(self):
        for task in self.data_preprocessing_tasks:
            if task.type == "SPLIT_SENTENCES":
                self.data = self.separate_sentences(self.data, task.required_columns)
            if task.type == "CONVERT_SEQUENCE_TO_BEFORE_RELATION":
                  self.data = self.interperet_sequence(self.data, task.required_columns)
            if task.type == "CHECK_ATOMICITY":
                  self.data = self.interperet_children(self.data, task.required_columns)
            if task.type == "SET_PARENT_FOR_TOP_LEVEL_TASK":
                  self.data = self.interperet_parents(self.data, task.required_columns)

        return self.data
                    
    def get_column_name(self, required_columns, key):
        for rq_key, rq_value in required_columns.items():
            if rq_key == key:
                return rq_value

    def separate_sentences(self, data, required_columns):

        text_column = self.get_column_name(required_columns, "text_column")
        id_column = self.get_column_name(required_columns, "id_column")
        sequence_column = self.get_column_name(required_columns, "sequence_column")
        parent_column = self.get_column_name(required_columns, "parent_id_column")

        output_data = data.copy()
        for index, record in data.iterrows():
            sentences = sent_tokenize(record[text_column])
            if len(sentences) > 1:
                for index, sentence in enumerate(sentences):
                    new_record = record.copy()
                    new_record[text_column] = sentence
                    new_record[sequence_column] = index + 1 # index starts at 0, sequence starts at 1
                    new_record[parent_column] = record[id_column]
                    new_record[id_column] = uuid.uuid4()
                    output_data = pd.concat([output_data, pd.DataFrame([new_record])], ignore_index=True)

        return output_data
    
    def interperet_sequence(self, data, required_columns):

        id_column = self.get_column_name(required_columns, "id_column")
        sequence_column = self.get_column_name(required_columns, "sequence_column")
        parent_id_column = self.get_column_name(required_columns, "parent_id_column")
        procedure_id_column = self.get_column_name(required_columns, "group_id_column")
        new_column = self.get_column_name(required_columns, "output_column")

        for index, record in data.iterrows():
            
                for procedure_id in data[procedure_id_column].unique():


                    if (procedure_id == record[procedure_id_column]):
    
                        beforeId = self.get_before_id(data,
                                                                record[sequence_column],
                                                                sequence_column,
                                                                id_column,
                                                                record[parent_id_column],
                                                                parent_id_column,
                                                                procedure_id_column,
                                                                procedure_id)
                        
                    
                        if (beforeId) != None:
                            data.at[index, new_column] = beforeId


        return data

    def get_before_id(self, df, sequence, sequence_column, id_column, parent_id, parent_id_column, procedure_id_column, procedure_id):
        procedure_steps = df.loc[df[procedure_id_column] == procedure_id]

        # TODO: check this
        if str(parent_id) == "nan":
            steps_with_same_parent = procedure_steps.loc[procedure_steps[parent_id_column].isnull()]
        else:
            steps_with_same_parent = procedure_steps.loc[procedure_steps[parent_id_column] == parent_id]
        before_step_sequence_number = sequence + 1
        if (before_step_sequence_number == len(procedure_steps) + 1):
            return None
        else:
            before_step = steps_with_same_parent.loc[steps_with_same_parent[sequence_column] == before_step_sequence_number]
            if len(before_step) > 0:
                return before_step[id_column].iloc[0]
            else:
                return None


    def interperet_children(self, data, required_columns):

        id_column = self.get_column_name(required_columns, "id_column")
        parent_id_column = self.get_column_name(required_columns, "parent_id_column")
        new_column = self.get_column_name(required_columns, "output_column")

        data[new_column] = data[id_column].apply(lambda x: self.get_children(data, x, parent_id_column))
        return data
    

    def get_children(self, df, id_column, parent_id_column):
        child_steps = df.loc[df[parent_id_column] == id_column]
        return  not len(child_steps) > 0
    
    def interperet_parents(self, data, reqired_columns):
        # if the parent is null, then it is a top level task, and parentID should be procedureId
        parent_id_column = self.get_column_name(reqired_columns, "parent_id_column")
        procedure_id_column = self.get_column_name(reqired_columns, "group_id_column")
        
        for index, record in data.iterrows():
            if (record[parent_id_column] == "nan" or record[parent_id_column] == None 
                or type(record[parent_id_column]) != str or record[parent_id_column].strip() == ""):
                data.at[index, parent_id_column] = record[procedure_id_column]
        return data