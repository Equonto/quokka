# Quokka

This repository contains code, and example data for the Quokka Workflow. The Quokka Workflow is a semi-automated workflow for improving the completeness, correctness and consistency of industrial maintenance procedures.

This repository contains six procedures from the [MyFixit Dataset](https://github.com/rub-ksv/MyFixit-Dataset), available under a [Creative Commons License](https://github.com/rub-ksv/MyFixit-Dataset?tab=License-1-ov-file#readme).

## Contents of this repository

- 0_testdata: contains test configurations and input data for different cases described in the paper.
- anonotated_dataset: contains six myFixit procedures, pre-annotated by two independant human annotators.
- config: contains the configuration used to generate the results described in the paper.
- data: contains the input data and output data generated when running the quokka workflow using the configuration described in the paper.
- libraries: contains two java libraries (lutra and a library for executing SHACL shapes)
- src: quokka code

## Starting the Quokka Workflow

#### Prerequisites:

1. Ensure that you have an Open AI Account (https://openai.com/index/openai-api/) and create a new API key. Note, running the Quokka workflow over high-volume datasets will incur high costs in OpenAI.
2. Ensure you have Python installed
3. Clone this repository onto your device.

#### To run the quokka workflow using the configuration provided:

1. Create a .env file in the root directory with the following value: ```OPENAI_API_KEY=<your OpenAI API key>```
2. Create a python virtual environment, and pip install the packages given in requirements.txt
3. Run the src/ConsoleApp.py file.
4. You will be presented with three options. Select ```completion``` to run the completion module, select ```consistency``` to run the consistency module, and select ```correctness``` to run the correctness module. The best way to work with the Quokka workflow is to run all three in order.

#### To view the outputs of the workflow

- The output of the completion module can be found at ```data/output/datafiles``` 
- The output of the consistencty module can be found at ```data/output/ontology```
- The output of the correctness module can be found at ```data/output/suggestions```

### To run the Quokka workflow with one of the example sets given in the 0_testdata folder:

1. Replace the ```config``` directory with the contents of the ```config``` folder in the test data
2. Replace the ```data/input``` directory with the csv files given the in test data
3. Run the Quokka workflow

## How to Cite this Work

To cite Quokka, please use the following:

```@article{woods2024quokka,
  title={Semantic Quality Assurance for Industrial Maintenance Procedures},
  author={Woods, Caitlin and French, Tim and Hodkiewicz, Melinda},
  year={2024},
  note={[in review]}
}
```

Additional documentation containing details for how to re-configure the Quokka workflow for different use cases is under construction.

Acknowledgement: This code was written with the help of GitHub Co-Pilot
