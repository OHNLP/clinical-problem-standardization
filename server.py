'''
A server wrapper over some commonly used functions
'''

from flask import Flask, jsonify, request

import predict
from snomed.attribute_constraints import get_applicable_attributes
from snomed.attribute_constraints import get_applicable_attributes_cuis
from snomed.attribute_constraints import get_applicable_attributes_for_tgt_cuis
from snomed.sct import sct_code_to_terms, expand_sct_code, is_super, get_children, get_children_terms, term_to_code, get_name_with_type
from umls.umls import cui_to_sct, get_parents, sct_to_cui

app = Flask(__name__)

f_map = {
    'cui_to_sct': cui_to_sct,
    'sct_to_cui': sct_to_cui,
    'expand_sct_code': expand_sct_code,
    'is_super': is_super,
    'get_children': get_children,
    'get_children_terms': get_children_terms,
    'sct_code_to_terms': sct_code_to_terms,
    'get_applicable_attributes': get_applicable_attributes,
    'get_applicable_attributes_cuis': get_applicable_attributes_cuis,
    'get_applicable_attributes_for_tgt_cuis': get_applicable_attributes_for_tgt_cuis,
    'get_parents': get_parents,
    'predict_full': predict.predict_full_json,
    'term_to_code': term_to_code,
    'get_name_with_type': get_name_with_type
}

@app.route('/<f>', methods=['GET', 'POST'])
def __f(f):
    params = request.get_json()

    return jsonify(f_map[f](**params))

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=False)