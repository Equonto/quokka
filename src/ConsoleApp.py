
from typing import Union
from TaskFactory import TaskFactory
from TaskType import TaskType
import inquirer
from FileIo import FileIo
from Settings import Settings

'''
This class is an entry point for the application. 
Asks the user which module that they would like to run.'''
class ConsoleApplication:

    def __init__(self):
        pass

    def run(self) -> None:
        while True:
            selection = self.ask_for_task_type()
            task_factory = TaskFactory(Settings(FileIo()))
            task_factory.create_task(selection).execute()

    
    def ask_for_task_type(self) -> Union[TaskType, None]:
        choices = {
                   'Completion': TaskType.COMPLETION,
                   'Consistency': TaskType.POPULATION,
                   'Correction': TaskType.CORRECTION
        }
        questions = [
            inquirer.List('task_type',
                          message="Select a task type",
                          choices=[key for key in choices.keys()],
                          ),
        ]
        answers = inquirer.prompt(questions)
        
        if (answers != None):
            return choices[
                answers['task_type']]
        else:
            return None


if __name__ == "__main__":
    app = ConsoleApplication()
    app.run()
    