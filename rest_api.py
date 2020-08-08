'''
REST API for processing free-text diagnosis statements into either:
    (1) OWL class expressions
    (2) FHIR Condition Resources
    (3) SNOMED CT Expressions
    (4) Raw concept relationship graphs
'''

from flask import Flask, request

import api
from transformers.transform import FhirConditionTransformer, SnomedExpressionTransformer, OwlTransformer, DefaultTransformer

app = Flask(__name__)

transformers = {
    'owl': OwlTransformer(),
    'fhir': FhirConditionTransformer(),
    'snomed': SnomedExpressionTransformer(),
    'raw': DefaultTransformer()
}

get_args = {
    'owl': lambda x: {
        'expression': x.get('expression', 'true') == 'true',
        'instances': x.get('instances', 'true') == 'true'
    },
    'fhir': lambda x: {},
    'snomed': lambda x: {},
    'raw': lambda x: {}
}

@app.route('/process', methods=['GET'])
def predict():
    dx = request.args.get('dx')

    format = request.args.get('format', default='snomed')

    graph = api.process(dx)[1]

    t = transformers[format]

    return t.serialize(t.transform(graph, **get_args[format](request.args)))

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=False, port=5150)