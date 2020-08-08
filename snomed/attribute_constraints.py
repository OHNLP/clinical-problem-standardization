# -*- coding: utf-8 -*-
import csv
import itertools
import os

import snomed.sct as sct
import snomed.sctecl as sctecl
import umls.umls as umls

if 'SNOMEDCT_HOME' in os.environ:
    base_path = os.environ['SNOMEDCT_HOME']
else:
    raise Exception("Please set the `SNOMEDCT_HOME` variable to the base of your SNOMDEDCT installation.")

print("Loading SNOMED Relationships")

with open(base_path + '/Full/Refset/Metadata/der2_cissccRefset_MRCMAttributeDomainFull_US1000124_20180901.txt', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter='\t')
    domains = {}
    for row in reader:
        if row['active'] == "1":
            mandatory = row['ruleStrengthId'] == '723597001'
            domains[row['referencedComponentId']] = (sctecl.do_parse(row['domainId']), mandatory)

with open(base_path + '/Full/Refset/Metadata/der2_ssccRefset_MRCMAttributeRangeFull_US1000124_20180901.txt', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter='\t')
    ranges = {}
    for row in reader:
        if row['active'] == "1":
            mandatory = row['ruleStrengthId'] == '723597001'
            ranges[row['referencedComponentId']] = (sctecl.do_parse(row['rangeConstraint']), mandatory)

print("Done loading SNOMED Relationships")

def meets_domain_constraint(attribute, concept):
    return _meets_constraint(attribute, concept, domains)

def meets_range_constraint(attribute, concept):
    return _meets_constraint(attribute, concept, ranges)

def get_applicable_attributes_for_tgt_cuis(target):
    applicable = set()

    target_sctids = umls.cui_to_sct(target)

    for target_sctid in target_sctids:
        for attribute in set(ranges.keys()):
            if meets_range_constraint(attribute, target_sctid):
                applicable.add(attribute)

    return list(applicable)

def get_applicable_attributes(source, target, bidirectional=True):
    applicable = set()

    def f(source_, target_):
        for attribute in set.intersection(set(domains.keys()), set(ranges.keys())):
            if meets_domain_constraint(attribute, source_) and meets_range_constraint(attribute, target_):
                applicable.add(attribute)

    f(source, target)

    if bidirectional:
        f(target, source)

    return list(applicable)

def get_applicable_attributes_cuis(source, target, bidirectional=True):
    applicable = set()

    source_sctids = umls.cui_to_sct(source)
    target_sctids = umls.cui_to_sct(target)

    pairs = itertools.product(source_sctids, target_sctids)

    for pair in pairs:
        applicable.update(set(get_applicable_attributes(*pair, bidirectional=bidirectional)))

    return list(applicable)

def _meets_constraint(attribute, concept, domain_or_range_):
    if attribute not in domain_or_range_:
        return False

    x = domain_or_range_[attribute]

    constraints = x[0]
    mandatory = x[1]

    #if not mandatory:
    #    return True

    for constraint in constraints:
        res = sct.is_super(constraint[0], concept)
        if res:
            return True

    return False


def get_attributes():
    return [(k, sct.sct_code_to_terms(k)) for k in ranges.keys()]