

from owlready2 import *
import rdflib

class Reasoner:

    def __init__(self, ontology_filename, imports_list):
        self.imports_list = imports_list
        self.ontology = self.load_ontology("config/consistency/imports/", "config/consistency/output/", ontology_filename=ontology_filename)

    def reserialize_ontology(self, staging_directory, ontology_filename):
        g = rdflib.Graph()
        format = ontology_filename.split(".")[1]
        if (format == "ttl" and ontology_filename != "catalog-v001.xml"):
            g.parse(staging_directory+ontology_filename, format=format)
            ontology_filename = ontology_filename.replace(format, "xml")
            g.serialize(destination=staging_directory+ontology_filename, format="xml")

    
    # Loads ontology with instances into world
    def load_ontology(self, imports_directory, staging_directory, ontology_filename):
        
        # load all ontologies in the imports folder
        imports = []
        for filename in self.imports_list:
            if filename.endswith(".ttl"):
                self.reserialize_ontology(imports_directory, filename)
                filename = filename.replace(".ttl", ".xml")
                ontology = get_ontology("file://"+imports_directory+filename)
                imports.append(ontology)
            elif filename.endswith(".owl") or filename.endswith(".rdf") or filename.endswith(".xml"):
                ontology = get_ontology("file://"+imports_directory+filename)
                imports.append(ontology)

        if ontology_filename.endswith(".ttl"):
            self.reserialize_ontology(staging_directory, ontology_filename)
            ontology_filename = ontology_filename.replace(".ttl", ".xml")
        
        
        # add imported ontologies to core ontology
        ontology = get_ontology("file://"+staging_directory+ontology_filename)

        for imported_ontology in imports:
            imported_ontology.load()
            ontology.imported_ontologies.append(imported_ontology)

        ontology.load()
        return ontology
    
    def run_pellet_reasoner(self):
        try:
            with default_world:
                sync_reasoner_pellet(infer_property_values = True, infer_data_property_values = True)
            return True
        except OwlReadyInconsistentOntologyError as e:
            return False