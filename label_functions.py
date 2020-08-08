'''
Example data programming labeling functions.

This example only uses SNOMED CT as distant supervision.

Users should expect to replace these with functions that relate to their data set,
including your one specific rules tailored toward your use-case.
'''


from snorkel.labeling import labeling_function
import relation.rels as rel_names
import umls.semantic_types as semantic_types
import server_client as server_client
import os

use_server = "USE_SERVER" in os.environ

if use_server:
    client = server_client
else:
    import snomed.sct as sct

    class LocalClient:
        def get_children_terms(self, c):
            return sct.get_children_terms(c)

    client = LocalClient()

terms_cache = {}


def is_tgt_term_a_child_of_code(x, code):
    if code not in terms_cache:
        terms_cache[code] = set([x.lower() for x in client.get_children_terms(code)])

    found_terms = terms_cache[code]

    terms = set([c.trigger.lower() for c in x['tgt']])

    return len(set.intersection(found_terms, terms)) > 0


ABSTAIN = -1


@labeling_function()
def lf_laterality(x):
    if is_tgt_term_a_child_of_code(x, "182353008"):
        return rel_names.rels_txt_to_int['laterality']

    return ABSTAIN

@labeling_function()
def lf_periodicity(x):
    if is_tgt_term_a_child_of_code(x, "7389001"):
        return rel_names.rels_txt_to_int['periodicity']

    return ABSTAIN

@labeling_function()
def lf_severity(x):
    if is_tgt_term_a_child_of_code(x, "272141005"):
        return rel_names.rels_txt_to_int['severity']

    return ABSTAIN

@labeling_function()
def lf_interpretation(x):
    if is_tgt_term_a_child_of_code(x, "276800000"):
        return rel_names.rels_txt_to_int['interpretation']

    return ABSTAIN

@labeling_function()
def lf_anatomical_direction(x):
    if is_tgt_term_a_child_of_code(x, "106233006") and not is_tgt_term_a_child_of_code(x, "182353008"):
        return rel_names.rels_txt_to_int['anatomicalDirection']

    return ABSTAIN

@labeling_function()
def lf_anatomical_direction2(x):
    if is_tgt_term_a_child_of_code(x, "272425003") and not is_tgt_term_a_child_of_code(x, "182353008"):
        return rel_names.rels_txt_to_int['anatomicalDirection']

    return ABSTAIN

@labeling_function()
def lf_certainty(x):
    if is_tgt_term_a_child_of_code(x, "106230009"):
        return rel_names.rels_txt_to_int['certainty']

    return ABSTAIN

@labeling_function()
def lf_course(x):
    if is_tgt_term_a_child_of_code(x, "288524001"):
        return rel_names.rels_txt_to_int['course']

    return ABSTAIN

@labeling_function()
def lf_clinical_status(x):
    if is_tgt_term_a_child_of_code(x, "303105007"):
        return rel_names.rels_txt_to_int['clinicalStatus']

    return ABSTAIN

@labeling_function()
def lf_clinical_status(x):
    if is_tgt_term_a_child_of_code(x, "288533004"):
        return rel_names.rels_txt_to_int['clinicalStatus']

    return ABSTAIN


@labeling_function()
def lf_verification_status(x):

    # from: https://www.hl7.org/fhir/valueset-condition-ver-status.html
    statuses = ['refuted', 'unconfirmed', 'confirmed', 'ruled-out']
    for status in statuses:
        if any([status in c.trigger.lower() for c in x['tgt']]):
            return rel_names.rels_txt_to_int['verificationStatus']

    return ABSTAIN

@labeling_function()
def lf_stage(x):
    if is_tgt_term_a_child_of_code(x, "261612004"):
        return rel_names.rels_txt_to_int['stage']

    return ABSTAIN

@labeling_function()
def lf_due_to_shortest_path(x,):
    shortest_path = x['shortest_path']

    terms = ['due to']

    if any([True if x in shortest_path else False for x in terms]):
        return rel_names.rels_txt_to_int['dueTo']

    return ABSTAIN

@labeling_function()
def lf_occurred_following_shortest_path(x,):
    shortest_path = x['shortest_path']

    terms = ['after', 'following']

    if any([True if x in shortest_path else False for x in terms]):
        return rel_names.rels_txt_to_int['occurredFollowing']

    return ABSTAIN

@labeling_function()
def lf_negated(x,):
    negated = any([c.negated for c in x['tgt']])

    if negated:
        return rel_names.rels_txt_to_int['negated']

    return ABSTAIN

@labeling_function()
def lf_body_site(x,):
    if is_tgt_term_a_child_of_code(x, "38866009"):
        return rel_names.rels_txt_to_int['bodySite']

    return ABSTAIN

@labeling_function()
def lf_body_site_sem_type(x,):
    tgt_sem_type_group = set(semantic_types.get_semantic_group_from_concept(x['tgt']))

    types = set(['ANAT'])
    if tgt_sem_type_group == types:
        return rel_names.rels_txt_to_int['bodySite']

    return ABSTAIN

@labeling_function()
def lf_historical(x,):
    if is_tgt_term_a_child_of_code(x, "392521001"):
        return rel_names.rels_txt_to_int['historical']

    return ABSTAIN

@labeling_function()
def lf_finding_method(x,):
    if is_tgt_term_a_child_of_code(x, "386053000"):
        return rel_names.rels_txt_to_int['findingMethod']

    return ABSTAIN

@labeling_function()
def lf_associated_sign_and_symptom(x,):
    if is_tgt_term_a_child_of_code(x, "404684003"):
        shortest_path = x['shortest_path']

        terms = ['with']
        if any([True if x == shortest_path else False for x in terms]):
            return rel_names.rels_txt_to_int['associatedSignAndSymptom']

    return ABSTAIN

lfs = [lf_laterality,
       lf_periodicity,
       lf_severity,
       lf_due_to_shortest_path,
       lf_certainty,
       lf_stage,
       lf_occurred_following_shortest_path,
       lf_interpretation,
       lf_negated,
       lf_clinical_status,
       lf_body_site, lf_body_site_sem_type,
       lf_anatomical_direction, lf_anatomical_direction2,
       lf_verification_status,
       lf_historical,
       lf_finding_method,
       lf_associated_sign_and_symptom,
       lf_course
       ]
