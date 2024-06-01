from FileIo import FileIo
from consistency.Lutra import Lutra
from consistency.Reasoner import Reasoner

class ConsistencyTask:

    def __init__(self, ontology_name, imports_list):
        self.ontology_name = ontology_name
        self.imports_list = imports_list
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
        print("Running reasoner on generated ontology")

        result = Reasoner(self.ontology_name, self.imports_list).run_pellet_reasoner()
        if (result):
            print("\033[92m" + "Ontology is consistent" + "\033[0m") 
        else:
            print("\033[91m" + "Ontology is inconsistent, please check and try again" + "\033[0m")
        FileIo.move_files("config/consistency/output", "data/output/ontology")
        FileIo.clear_directory("config/consistency/staging")
        FileIo.clear_directory("config/consistency/output")
        print("Process complete. Please check the config/output folder.")


