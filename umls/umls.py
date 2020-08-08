'''
Wrappers exposing various UMLS functionality
'''

import csv
import os.path

import snomed.sct as sct

if 'UMLS_HOME' in os.environ:
    umls_base_path = os.environ['UMLS_HOME']
else:
    raise Exception("Please set the `UMLS_HOME` variable to the base of your UMLS installation.")

mrconso_file = umls_base_path + "MRCONSO.RRF"
mrrel_file = umls_base_path + "MRREL.RRF"

if 'SNOMEDCT_HOME' in os.environ:
    sct_base_path = os.environ['SNOMEDCT_HOME']
else:
    raise Exception("Please set the `SNOMEDCT_HOME` variable to the base of your SNOMDEDCT installation.")


cui_to_sct_ = {}

sct_to_cuis_ = {}


with open(mrconso_file, encoding="utf8") as f:
    reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)

    for line in reader:
        cui = line[0]
        sab = line[11]
        code = line[13]
        suppress = line[16] != 'N'

        if not suppress and sab == 'SNOMEDCT_US':
            if cui not in cui_to_sct_:
                cui_to_sct_[cui] = set()
            cui_to_sct_[cui].add(code)

            if code not in sct_to_cuis_:
                sct_to_cuis_[code] = set()
            sct_to_cuis_[code].add(cui)

print("Done loading MRCONSO")

umls_tree = {}

with open(mrrel_file, encoding="utf8") as f:
    reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)

    for line in reader:
        sab = line[10]
        src = line[0]
        tgt = line[4]
        rel = line[3]

        if rel == 'PAR':
            if src not in umls_tree:
                umls_tree[src] = []

            umls_tree[src].append(tgt)

print("Done loading MRREL")

sem_type_to_sct_root = {
    'dsyn': '64572001',
    'bpoc': '123037004'
}

def get_parents(cui):
    if cui in umls_tree:
        return umls_tree[cui]
    else:
        return []

def cui_to_sct(cui, sem_types=None):
    if cui not in cui_to_sct_:
        return []

    sctids = cui_to_sct_[cui]
    if len(sctids) > 1:
        print("More than 1 sctid for: " + cui)

        if sem_types is None:
            sctids_ = set(sctids)
        else:
            sctids_ = set()
            for sctid in sctids:
                for sem_type in sem_types:
                    if sem_type in sem_type_to_sct_root:
                        if sct.is_super(sem_type_to_sct_root[sem_type], sctid):
                            sctids_.add(sctid)
                    else:
                        sctids_.add(sctid)

        final = sctids_.copy()
        for outer in sctids_:
            for inner in sctids_:
                if (outer != inner) and sct.is_super(outer, inner):
                    if outer in final:
                        final.remove(outer)

        sctids = final

    return list(sctids)

def sct_to_cui(sct):
    if sct in sct_to_cuis_:
        cuis = sct_to_cuis_[sct]
        return list(cuis)
    else:
        return []
