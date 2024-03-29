
import subprocess

class Validator:

    def validate(self, inputFolder, shaclPath, outputPath) :
        command = f"java -jar libraries/shacl-validator-1.0-jar-with-dependencies.jar {inputFolder} {shaclPath} {outputPath}"
        print("start validation")
        result = subprocess.run(command
            , stdout=subprocess.PIPE
            , stderr=subprocess.PIPE
            , shell=True)
        print("finish validation")
        print(result.stdout.decode("utf-8"))
        print(result.stderr.decode("utf-8"))
        return result
    