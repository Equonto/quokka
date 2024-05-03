# Consistency Test 4

Test for Invalid Resource Assignment

Test Data:

This dataset contains two procedures and two tasks. The project is misconfigured so that a Tool entity is of type lis:Activity. This is inconsistent because any entity of type ompd:Resource must be a lis:Object.

Expected Result:

```The Ontology is Inconsistent```