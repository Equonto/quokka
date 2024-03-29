import subprocess
import os

class Lutra:

    def __init__(self):
        pass

    def run_lutra_process(self, ontology_filename):

        filenames = os.listdir("config/consistency/templates/bottr/")
        full_filenames = [f"templates/bottr/{filename}" for filename in filenames]
        filenames_string = ' '.join(full_filenames)

        outputType = "wottr"
        outputFolder = "output/"
        outputFilename = ontology_filename
        libraryType = "stottr"
        libraryFolder = "templates/stottr"
        inputType = "bottr"
        inputFolder = filenames_string

        command = "java -jar ../../libraries/lutra.jar -m expand -O " \
            + outputType + " -o " + outputFolder + outputFilename \
            + " -L " + libraryType + " -l " \
            + libraryFolder \
            + " -I " + inputType \
            + " " + inputFolder \
            + " --fetchMissing" \
        
        result = subprocess.run(command
            , stdout=subprocess.PIPE
            , stderr=subprocess.PIPE
            , shell=True
            , cwd="config/consistency")
            
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
        print(command)
        print(result.returncode)
        