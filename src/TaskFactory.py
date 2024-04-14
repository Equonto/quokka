from FileIo import FileIo
from completion.CompletionTask import CompletionTask
from correction.CorrectionTask import CorrectionTask
from consistency.ConsistencyTask import ConsistencyTask
from TaskType import TaskType

class TaskFactory:

    def __init__(self, settings):
        self.settings = settings

    def create_task(self, task_type):
        if task_type == TaskType.COMPLETION:
            return CompletionTask("data/input/", "data/output/datafiles", "config/completion/", "staging")
        elif task_type == TaskType.CORRECTION:
            return CorrectionTask()
        elif task_type == TaskType.POPULATION:
            return ConsistencyTask(self.settings.get_ontology_name())
        else:
            raise ValueError("Invalid task type: " + task_type)
