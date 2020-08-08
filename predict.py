'''
API over the relationship prediction model.
'''

import tensorflow as tf

import metamap.metamap as metamap
import rel_models.rel_classifier_clinicalbert as rel_classifier_clinicalbert
import umls.semantic_types as semantic_types
from cui2vec import Cui2Vec
from os import path

# CUI2Vec pretrained vectors are avialable: http://cui2vec.dbmi.hms.harvard.edu/
cui2vec = Cui2Vec().cui2vec

mm = metamap.MetaMap(additional_args='-y -L 2018AB -R SNOMEDCT_US --exclude_sts mnob', workers=1)
lite = False

model_path = './models/BiLSTMClinicalBert__shortest_path--source--source_sem_type--source_sem_type_group--source_vec--target--target_sem_type--target_sem_type_group--target_vec.model'

if path.exists(model_path):
    nb = rel_classifier_clinicalbert.ClinicalBertClassifier(model=model_path)
else:
    nb = None

def get_sem_type(concepts):
    for c in concepts:
        return c.semtypes[0]
    return "NONE"


def predict_full_json(txt, src, src_txt_span, tgt, tgt_txt_span, shortest_path):
    session = nb.session

    with session.graph.as_default():
        tf.compat.v1.keras.backend.set_session(session)

        src = metamap.Concept(**src)
        tgt = metamap.Concept(**tgt)

        result = predict_full(src, src_txt_span, tgt, tgt_txt_span, shortest_path, txt)

    return {'rel': result[0], 'score': result[1].astype(float)}


def predict_full(source, src_txt_span, target, tgt_txt_span, shortest_path, text):
    print(locals())

    y = nb.predict(text,
                   shortest_path,
                   src_txt_span,
                   tgt_txt_span,
                   cui2vec([source]),
                   cui2vec([target]),
                   get_sem_type([source]),
                   get_sem_type([target]),
                   semantic_types.get_semantic_group_from_concept([source]),
                   semantic_types.get_semantic_group_from_concept([target])
                   )
    print(y)

    return y
