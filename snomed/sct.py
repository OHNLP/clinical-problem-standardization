'''
Various functions for working with SNOMED CT
'''

import csv
import os

if 'SNOMEDCT_HOME' in os.environ:
    base_path = os.environ['SNOMEDCT_HOME']
else:
    raise Exception("Please set the `SNOMEDCT_HOME` variable to the base of your SNOMDEDCT installation.")

terms = {}
dict_lookup = {}

print("Loading SNOMED Decriptions")

with open(base_path + '/Full/Terminology/sct2_Description_Full-en_US1000124_20180901.txt', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter='\t')

    for row in reader:
        term = row['term']
        code = row['conceptId']
        active = row['active'] == '1'

        if active:
            if code not in terms:
                terms[code] = set()

            terms[code].add(term)

            t = term.lower().split(" (")
            if len(t) > 1:
                key = t[1]
            else:
                key = t[0]

            if key not in dict_lookup:
                dict_lookup[key] = set()

            dict_lookup[key].add(code)

print("Done loading SNOMED Decriptions")


print("Loading SNOMEDCT Transitive Closure")

supertypes = {}
with open(base_path + '/Resources/TransitiveClosure/res2_TransitiveClosure_US1000124_20180901.txt', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    for line in reader:
        super = line['superTypeId']
        sub = line['subTypeId']
        if super not in supertypes:
            supertypes[super] = set()
        supertypes[super].add(sub)

print("Done loading SNOMEDCT Transitive Closure")

def sct_code_to_terms(code):
    return terms[code]

def expand_sct_code(code):
    return code + " | " + get_name_with_type(code) + " | "


def get_name_with_type(code):
    return [x for x in list(terms[code]) if x.endswith(")")][0]


def term_to_code(term):
    term = term.lower()

    if term in dict_lookup:
        return list(dict_lookup[term])

def is_super(super, child, strict=False):
    if not strict and super == child:
        return True
    if super not in supertypes:
        return False
    else:
        return child in supertypes[super]

def get_children(code):
    return list(supertypes[code])

def get_children_terms(code):
    return_terms = list(terms[code])

    if code in supertypes:
        return_terms += [term for c in supertypes[code] for term in terms[c]]

    return return_terms
