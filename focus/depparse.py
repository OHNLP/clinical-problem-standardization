'''
A utility for running dependency parsing on clinical problem descriptions
'''

import metamap.metamap as metamap
import networkx as nx
import spacy
from spacy.tokens import Span
from nltk import Tree

mm = metamap.MetaMap(additional_args='-y -L 2018AB -R SNOMEDCT_US --exclude_sts mnob,bmod', workers=1)


class DepParse():

    # Train a custom dependency parse model using focus/train_parser.py
    def __init__(self, model='custom'):
        if model == 'custom':
            self.nlp = spacy.load('./data/dep_parse', disable=["entity_linker", "textcat", "entity_ruler", "sentencizer", "merge_noun_chunks", "merge_entities", "merge_subtokens"])
        elif model == 'en_core_sci_md':
            self.nlp = spacy.load("en_core_sci_md")
        elif model == 'en':
            self.nlp = spacy.load("en")
        else:
            raise Exception("Model: " + model + " not found.")

    def dependency_parse_batch(self, txts, debug=False, as_graph=False, with_doc=False):
        concepts = mm.call_metamap_batch(txts)

        return [
            (doc, self.do_dependency_parse(doc, concepts[i], debug, as_graph)) if with_doc else self.do_dependency_parse(doc, concepts[i], debug, as_graph)
            for i, doc in enumerate(self.nlp.pipe(txts, disable=["entity_linker", "textcat", "entity_ruler", "sentencizer", "merge_noun_chunks", "merge_entities", "merge_subtokens"]))
        ]

    def do_dependency_parse(self, doc, concepts, debug=False, as_graph=False):
        triples = []

        if debug:
            print('''
              {
                "txt": "%s",
                "heads": %s,
                "deps": %s
              }
            ''' % (doc.text,
                   "["+", ".join(map(str, [t.head.i for t in doc]))+"]",
                   "["+", ".join(["\""+t.dep_+"\"" for t in doc])+"]"))

        with doc.retokenize() as retokenizer:
            merged_spans = []
            for concept in concepts:
                try:
                    start, length = concept.offsets.split("/")
                    span = doc.char_span(int(start), int(start)+int(length))
                    if span is not None and len(span) > 1:
                        merged_spans.append(span)
                except ValueError:
                    pass

            merge_compounds = False

            if merge_compounds:
                start = None
                for token in doc:
                    if token.dep_ == 'compound':
                        if start is None:
                            start = token.i
                    else:
                        if start is not None:
                            span = Span(doc, start, token.i+1)
                            filtered_spans = spacy.util.filter_spans(merged_spans + [span])
                            if span in filtered_spans:
                                merged_spans.append(span)
                            start = None

            for span in spacy.util.filter_spans(merged_spans):
                retokenizer.merge(span)


        for token in doc:
            triples.append((token.i, token.dep_, token.head.i))

        edges = []
        for token in doc:
            if token.dep_ == 'ROOT':
                edges.append(('ROOT', token.i))

            # FYI https://spacy.io/docs/api/token
            for child in token.children:
                if child.dep_ != 'conj' or token.dep_ == 'ROOT':
                    edges.append((token.i, child.i))

                    for conjunct in child.conjuncts:
                        if token.i != conjunct.i:
                            edges.append((token.i, conjunct.i))

        graph = nx.DiGraph(edges)

        def to_nltk_tree(node):
            if node.n_lefts + node.n_rights > 0:
                return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
            else:
                return node.orth_

        if debug:
            tree = to_nltk_tree(list(doc.sents)[0].root)
            try:
                tree.pretty_print()
            except Exception as e:
                print("Could not print tree:", e)

        if debug:
            for token in doc:
                print("ENT:", token.text, token.ent_type_, token.ent_iob_, token.pos_)
                print(token.text, token.dep_, token.head.text, token.head.pos_,
                      [child for child in token.children])

        if as_graph:
            return graph, doc, triples, concepts
        else:
            return triples