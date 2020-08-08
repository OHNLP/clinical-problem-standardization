# clinical-problem-standardization

**clinical-problem-standardization** is a framework for standardizing free-text clinical problems into  [SNOMED CT Expressions](https://confluence.ihtsdotools.org/display/DOCSTART/7.+SNOMED+CT+Expressions) and [HL7 FHIR resources](https://www.hl7.org/fhir/).

A *clinical problem* is a short description of a patient issue, diagnosis, or concern, such as *"Severe with probable recurrent migraine."* These are found in multiple places in healthcare data, especially in problem lists.

This framework uses natural language processing techniques to parse these problem descriptions into standardized models.

**NOTICE:** This repository is research code and is subject to extensive change. Assume all code to be pre-alpha and experimental.

## Prerequisites

The following dependencies are required to run the code:

* Python 3.6+
* Pandas 0.24.2+
* NLTK 3.4.5+
* Tensorflow 1.14.0+
* spaCy 2.2.4+
* Snorkel 0.9.3+
* bert-serving-server/bert-serving-client 1.9.1+
* Flask 1.0.2+
* numpy 1.14.5+

The following will also need to be downloaded/installed:

* [UMLS](https://www.nlm.nih.gov/research/umls/quickstart.html)
* [SNOMED CT](https://www.nlm.nih.gov/healthit/snomedct/us_edition.html)
* [MetaMap](https://metamap.nlm.nih.gov/Installation.shtml)
* [bert-as-service](https://bert-as-service.readthedocs.io/en/latest/)
* [cui2vec concept vectors](http://cui2vec.dbmi.hms.harvard.edu/)

## Environment Variables to Set
``SNOMEDCT_HOME``: the path to SNOMED CT distribution files

``UMLS_HOME``: the path to ``META`` to the UMLS installation

``CUI2VEC_HOME``: the path to the cui2vec word embedding file

## Start bert-as-service
See the [bert-as-service documentation] for options regarding the BERT embedding server. It is recommended to use either a fine-tuned model or a model pre-trained for the biomedical domain. We recommend [clinicalBERT](https://github.com/EmilyAlsentzer/clinicalBERT).

## Training
Our framework uses [Snorkel](https://www.snorkel.org/) to create training data without having to manually annotate a training set. Users *are*, however, required to supply a labeled test and validation set.

There are two aspects of training. First, training the relation classifier. The follow ``data_handler.py`` shows an example of how to create a data adapter into the Snorkel training process. The existing ``data_handler.py`` uses SNOMED CT stated relationships as training data. While this does not produce a good model, it is used here for demonstration purposes. Users should supply their own ``DataHandler`` class as appropriate for their data set.

Users should also add their own labeling functions to the ``label_functions.py`` file. These labeling functions are critical to producing a quality training data set. See the [Snorkel tutorial](https://www.snorkel.org/use-cases/01-spam-tutorial) for more information on labeling functions.

Next, the dependency parser can be fine-tuned. See ``focus/train_parser.py`` for more details.

## Starting the UMLS/SNOMED CT Server
A server is included to wrap several functions pertaining to the UMLS and SNOMED CT (such as parent/child lookups, SNOMED -> UMLS conversions, etc.).

run ``server.py``

## Starting the Standardization Server
A trained model can be exposed via an HTTP server via the following Python file:

run ``rest_api.py``

## Standardization Server Endpoints
There is currently one endpoint exposed in the API, with inputs of the problem string and the desired output format:

``/process?dx=[clinical problem string]&?format=[owl|fhir|snomed|raw]``

where ``format`` can be one of the following:

| format | description |
| --- | --- |
| owl | [OWL](https://www.w3.org/OWL/) class expression |
| fhir | [FHIR Condition Resource](https://www.hl7.org/fhir/condition.html)  |
| snomed | [SNOMED CT Expression](https://confluence.ihtsdotools.org/display/DOCSTART/7.+SNOMED+CT+Expressions) |
| raw | A basic directed graph-based representations of concepts + relationships |
