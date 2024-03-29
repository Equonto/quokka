
from FileIo import FileIo
from correction.Validator import Validator
class CorrectionTask:

    def execute(self):
        config = FileIo.read_json("config/correction/config.json")
        staging_data = "config/correction/staging/data/"
        staging_shacl = "config/correction/staging/shacl/"
        output_folder = "data/output/suggestions/"
        FileIo.clear_directory(output_folder)
        FileIo.move_files("data/output/ontology", staging_data)
        FileIo.move_files("config/correction/imports", staging_data)
        FileIo.move_files("config/correction/shacl", staging_shacl)
        Validator().validate(staging_data, staging_shacl + config["shacl_filename"], output_folder + "results.ttl")
        FileIo.clear_directory(staging_data)
        FileIo.clear_directory(staging_shacl)
        print("process complete")
                

    


