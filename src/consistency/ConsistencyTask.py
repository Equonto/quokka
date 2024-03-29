from FileIo import FileIo
from consistency.Lutra import Lutra

class ConsistencyTask:

    def __init__(self, ontology_name):
        self.ontology_name = ontology_name
        pass

    def execute(self):
        lutra = Lutra()
        FileIo.clear_directory("data/output/ontology")
        FileIo.clear_directory("config/consistency/staging")
        FileIo.move_files("config/consistency/imports", "data/output/ontology")
        FileIo.move_files("data/output/datafiles", "config/consistency/staging")
        FileIo.move_files("config/consistency/metadata", "config/consistency/staging")
        print("Running lurta")
        lutra.run_lutra_process(self.ontology_name)
        print("Process complete. Please check the config/output folder.")
        FileIo.move_files("config/consistency/output", "data/output/ontology")
        FileIo.clear_directory("config/consistency/staging")
        FileIo.clear_directory("config/consistency/output")
        print("process complete")


