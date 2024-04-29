class Settings:

    def __init__(self, io):
        self.settings = io.read_json("config/settings.json")
        pass

    def get_ontology_name(self, extension = "ttl"):
        version_number = self.settings['ontology_version'].replace(".", "_")
        filename = self.settings['ontology_filename']
        return f"{filename}_v{version_number}.{extension}"
    
    def get_imports_list(self):
        return self.settings['imported_ontologies']