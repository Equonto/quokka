# Quokka

This repository contains code, and example data for the Quokka Workflow. The Quokka Workflow is a semi-automated workflow for improving the completeness, correctness and consistency of industrial maintenance procedures.

This repository contains six procedures from the [MyFixit Dataset](https://github.com/rub-ksv/MyFixit-Dataset), available under a [Creative Commons License](https://github.com/rub-ksv/MyFixit-Dataset?tab=License-1-ov-file#readme).

## Contents of this repository

- 0_testdata: contains test configurations and input data for different cases described in the paper.
- anonotated_dataset: contains six myFixit procedures, pre-annotated by two independant human annotators.
- config: contains the configuration used to generate the results described in the paper.
- data: contains the input data and output data generated when running the quokka workflow.
- libraries: contains two java libraries (lutra and a library for executing SHACL shapes)
- src: quokka code

## Starting the Quokka Workflow

To run the quokka workflow using the configuration provided:

1. Create a python virtual environment, and pip install the packages given in requirements.txt
2. Run the src/ConsoleApp.py file.

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

