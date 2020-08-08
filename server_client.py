'''
A client for server.py
'''

import requests

def cui_to_sct(cui, sem_types):
    return requests.post("http://127.0.0.1:5000/cui_to_sct", json=locals()).json()

def sct_to_cui(sct):
    return requests.post("http://127.0.0.1:5000/sct_to_cui", json=locals()).json()

def is_super(super, child, strict=False):
    return requests.post("http://127.0.0.1:5000/is_super", json=locals()).json()

def get_applicable_attributes(source, target):
    return requests.post("http://127.0.0.1:5000/get_applicable_attributes", json=locals()).json()

def expand_sct_code(code):
    return requests.post("http://127.0.0.1:5000/expand_sct_code", json=locals()).json()

def get_children(code):
    return requests.post("http://127.0.0.1:5000/get_children", json=locals()).json()

def get_children_terms(code):
    return requests.post("http://127.0.0.1:5000/get_children_terms", json=locals()).json()

def get_applicable_attributes_cuis(source, target, bidirectional=True):
    return requests.post("http://127.0.0.1:5000/get_applicable_attributes_cuis", json=locals()).json()

def get_applicable_attributes_for_tgt_cuis(target):
    return requests.post("http://127.0.0.1:5000/get_applicable_attributes_for_tgt_cuis", json=locals()).json()

def get_parents(cui):
    return requests.post("http://127.0.0.1:5000/get_parents", json=locals()).json()

def term_to_code(term):
    return requests.post("http://127.0.0.1:5000/term_to_code", json=locals()).json()

def get_name_with_type(code):
    return requests.post("http://127.0.0.1:5000/get_name_with_type", json=locals()).json()

def predict(txt, src, tgt):
    return requests.post("http://127.0.0.1:5000/predict", json=locals()).json()

def predict_full(txt, src, src_txt_span, tgt, tgt_txt_span, shortest_path):
    return requests.post("http://127.0.0.1:5000/predict_full", json=locals()).json()

