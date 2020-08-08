#!/usr/bin/env python
# coding: utf8
"""
Script for training a new dependency parse model.


NOTE: This code is adapted from code posted here: https://spacy.io/usage/training


This requires a training data in a file called 'training_data.json' which is a
JSON format in this form:

[
  {
    "txt": "severe pain",
    "heads": [1, 1],
    "deps": ["amod", "ROOT"]
  },
  {
  ...
  }
]

This training data is NOT included and must be supplied.
"""
from __future__ import unicode_literals, print_function

import numpy as np
import random
from pathlib import Path
import spacy
from nltk import Tree
from spacy.gold import GoldParse
from spacy.util import minibatch, compounding
from sklearn.model_selection import train_test_split
from copy import deepcopy
import json
from sklearn.model_selection import KFold
from spacy.util import decaying

en_core_sci_sm = spacy.load("en_core_sci_sm")
en_core_sci_md = spacy.load("en_core_sci_md")
en_core_sci_lg = spacy.load("en_core_sci_lg")

en = spacy.load("en")
en.tokenizer = en_core_sci_sm.tokenizer

# training data
ALL_DATA = json.load(open('training_data.json'))


def train(train_data, model="en_core_sci_lg", output_dir='./data/dep_parse', n_iter=15):
    """Load the model, set up the pipeline and train the parser."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # add the parser to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "parser" not in nlp.pipe_names:
        parser = nlp.create_pipe("parser")
        nlp.add_pipe(parser, first=True)
    # otherwise, get it, so we can add labels to it
    else:
        parser = nlp.get_pipe("parser")

    ner = nlp.get_pipe("ner")
    ner.add_label('0')
    ner.add_label('1')

    # add labels to the parser
    for entry in train_data:
        for dep in entry.get("deps", []):
            parser.add_label(dep)

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "parser" and pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts = [x['txt'] for x in batch]

                def get_pos(t):
                    ents = []
                    if 'mask' in t:
                        for mask in t['mask']:
                            idx = t['txt'].find(mask)
                            if idx > -1:
                                ents.append((idx, idx + len(mask), "1"))

                    return ents

                annotations = [{'heads': x['heads'], 'deps': x['deps'], 'entities': get_pos(x)} for x in batch]
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print("Losses", sorted([(k,v) for k,v in losses.items()], key=lambda x:x[0]))

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

    print("Train on", len(train_data))

    return nlp

def test(nlp, test_data):

    # test the trained model
    for test_text in test_data:
        doc = nlp(test_text['txt'])
        print("Dependencies")
        print([(t.i, t.text) for t in doc])
        print([t.head.i for t in doc])
        for t in doc:
            for c in t.children:
                print(t.text, c.dep_, c.text)

        def to_nltk_tree(node):
            if node.n_lefts + node.n_rights > 0:
                return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
            else:
                return node.orth_

        tree = to_nltk_tree(list(doc.sents)[0].root)
        tree.pretty_print()

    testing = []
    for entry in test_data:
        d = nlp(entry['txt'])
        gold = GoldParse(d, heads=entry['heads'], deps=entry['deps'], entities=[entry['entities']])
        testing.append((d, gold))

    scorer = nlp.evaluate(testing, verbose=False)
    print(scorer.scores)
    print("Test on", len(test_data))

    return scorer.scores


if __name__ == "__main__":
    def run_analysis():
        data = np.array(ALL_DATA)
        kf = KFold(n_splits=10)

        splits = kf.split(data)

        scores = []
        for train_, test_ in splits:
            model = train(data[train_])
            scores.append(test(model, data[test_]))

        custom_scores = {}
        for type in ['uas', 'las']:
            row_scores = [y[type] for y in scores]
            avg = np.mean(row_scores)
            sd = np.std(row_scores)
            custom_scores[type] = (avg, sd)

        eng_scores = test(en, ALL_DATA)
        sci_sm_scores = test(en_core_sci_sm, ALL_DATA)
        sci_md_scores = test(en_core_sci_md, ALL_DATA)

        print(eng_scores)
        print(sci_sm_scores)
        print(sci_md_scores)
        print(custom_scores)

    train(ALL_DATA)