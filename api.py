'''
General API for transforming free-text diagnosis statements into relationship graphs.
'''


import itertools
from typing import List, Tuple

import networkx as nx
from focus.depparse import DepParse
import metamap.metamap as metamap
import server_client
from graph import Graph


ATTRIBUTE = '246061005'
UNAPPROVED_ATTRIBUTE = '408739003'

mm = metamap.MetaMap(additional_args='-y -L 2018AB -R SNOMEDCT_US --exclude_sts mnob,bmod', workers=1)


rel_name_to_sct = {
    'associatedSignAndSymptom': '47429007',
    'interpretation': '363713009',
    'anatomicalDirection': '116677004',
    'severity': '246112005',
    'bodySite': '363698007',
    'otherwiseRelated': '246061005',
    'dueTo': '42752001',
    'laterality': '272741003',
    'certainty': '246103008',
    'course': '263502005',
    'occurredFollowing': '255234002',
    'clinicalStatus': '263493007',
    'verificationStatus': '408729009',
    'stage': '258214002',
    'periodicity': '260864003',
    'findingMethod': '418775008'
}

unary_rels = {
    'historical': ('408731000', '410513005')
}

flatmap = lambda x: [j for i in x for j in i]

dp = DepParse(model='en_core_sci_md')

def process(raw_dx) -> Tuple[str, Graph]:
    return process_batch([raw_dx])[0]

def process_batch(raw_dxes, debug=True) -> List[Tuple[str, Graph]]:
    dxes = list(raw_dxes)

    def get_concept(token, metamap_concepts):
        for metamap_concept in metamap_concepts:
            if metamap_concept.trigger.lower() == token.lower_:
                return [metamap_concept]

        return_concepts = set()

        for metamap_concept in metamap_concepts:
            for offset in metamap_concept.offsets.split(","):
                if "/" in offset:
                    concept_start, concept_length = map(int, offset.split("/"))
                elif ":" in offset:
                    concept_start, concept_length = map(int, offset.split(":"))
                else:
                    raise Exception("Illegal character in offset split: " + offset)

                token_start = token.idx
                token_length = len(token.text)

                if len(set.intersection(
                        set(range(concept_start, concept_start + concept_length)),
                        set(range(token_start, token_start + token_length)))) > 0:
                    return_concepts.add(metamap_concept)

        return list(return_concepts)

    def get_attribute(tokens, metamap_concepts, allow_unapproved=False):
        cuis = flatmap([get_concept(t, metamap_concepts) for t in tokens])

        term = " ".join([t.lower_ for t in tokens])

        sct_ids = set()

        terms = server_client.term_to_code(term)

        if terms:
            sct_ids.update(terms)

        for cui in cuis:
            sct_ids.update(server_client.cui_to_sct(cui.cui, None))

        for sct_id in sct_ids:
            if server_client.is_super(ATTRIBUTE, sct_id) and (allow_unapproved or not server_client.is_super(UNAPPROVED_ATTRIBUTE, sct_id)):
                return sct_id

    results = []

    for sent, (graph, doc, triples, metamap_concepts) in zip(dxes, dp.dependency_parse_batch(dxes, debug=debug, as_graph=True)):
        concepts = []
        rels = []

        print(sent)

        root = list(filter(lambda x:x[1] == 'ROOT', triples))[0][0]

        for token in doc:
            print(token.lower_, token.pos_)

            attr = None

            if token.i > 0:
                attr = get_attribute([token], metamap_concepts, allow_unapproved=False)

            if attr is None:
                idx = token.i
                pos = token.pos_
                type = token.ent_type_

                if type != '1' and pos in ['NOUN', 'ADJ', 'VERB', 'NUM', 'ADV']:
                    cuis = get_concept(token, metamap_concepts)

                    if cuis:
                        concepts.append((idx, cuis))

        for (src_id, src_cuis), (tgt_id, tgt_cuis) in itertools.permutations(concepts, 2):
            if src_id != tgt_id:
                if nx.has_path(graph, src_id, tgt_id):
                    path = nx.shortest_path(graph, src_id, tgt_id)
                    if len(path) > 2:
                        predicate_tokens = path[1:-1]
                        if not len(set.intersection(set([c[0] for c in concepts]), set(predicate_tokens))) > 0:
                            rels.append([(src_id, src_cuis), predicate_tokens, (tgt_id, tgt_cuis)])
                    else:
                        rels.append([(src_id, src_cuis), None, (tgt_id, tgt_cuis)])

        print(rels)

        graph = Graph(root, sent)

        if len(rels) == 0:
            concepts = get_concept(doc[root], metamap_concepts)
            graph.add_node(root, concepts, flatmap([server_client.cui_to_sct(c.cui, None) for c in concepts]), doc[root].lower_)

        for (s, src_cuis), p, (o, tgt_cuis) in rels:
            src_sctids = flatmap([server_client.cui_to_sct(c.cui, None) for c in src_cuis])
            tgt_sctids = flatmap([server_client.cui_to_sct(c.cui, None) for c in tgt_cuis])

            attribute = None
            if p:
                attribute = get_attribute(list(map(lambda i: doc[i], p)), metamap_concepts)

            if not attribute:
                attributes = server_client.get_applicable_attributes(src_cuis[0].cui, tgt_cuis[0].cui)

                if len(attributes) == 1:
                    attribute = attributes[0]
                else:
                    shortest_path = " ".join([doc[i].lower_ for i in p]) if p else ""
                    attribute_hat = server_client.predict_full(
                        sent,
                        src_cuis[0].__dict__,
                        doc[s].lower_,
                        tgt_cuis[0].__dict__,
                        doc[o].lower_,
                        shortest_path
                    )

                    attribute_hat_name = attribute_hat['rel']

                    if attribute_hat_name in rel_name_to_sct:
                        attribute = rel_name_to_sct[attribute_hat_name]

                    if attribute_hat_name in unary_rels:
                        attribute = unary_rels[attribute_hat_name][0]
                        tgt_cuis = []
                        tgt_sctids = [unary_rels[attribute_hat_name][1]]


            graph.add_node(s, src_cuis, src_sctids, doc[s].lower_)
            graph.add_node(o, tgt_cuis, tgt_sctids, doc[o].lower_)

            graph.add_edge(s, o, attribute)

            try:
                print("---->", doc[s].lower_, attribute, doc[o].lower_)
                print("\t---->", src_sctids,
                      "|",
                      server_client.expand_sct_code(attribute),
                      "|",
                      tgt_sctids,
                      attribute)
            except Exception as e:
                print("Error debug print:", e)

        results.append((sent, graph))

    return results
