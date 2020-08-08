import metamap.metamap as metamap

import os

import csv
import server_client as client
import metamap
from sklearn.model_selection import train_test_split

use_server = "USE_SERVER" in os.environ

if use_server:
    server_client = client
else:
    import umls.umls as umls
    import snomed.sct as sct

    class LocalClient:
        def sct_to_cui(self, c):
            return umls.sct_to_cui(c)

        def get_name_with_type(self, c):
            return sct.get_name_with_type(c)

    server_client = LocalClient()

if 'SNOMEDCT_HOME' in os.environ:
    base_path = os.environ['SNOMEDCT_HOME']
else:
    raise Exception("Please set the `SNOMEDCT_HOME` variable to the base of your SNOMDEDCT installation.")


sct_id_to_rel_name = {
    '47429007': 'associatedSignAndSymptom',
    '363713009': 'interpretation',
    '116677004': 'anatomicalDirection',
    '246112005': 'severity',
    '363698007': 'bodySite',
    '246061005': 'otherwiseRelated',
    '42752001': 'dueTo',
    '272741003': 'laterality',
    '246103008': 'certainty',
    '263502005': 'course',
    '255234002': 'occurredFollowing',
    '263493007': 'clinicalStatus',
    '408729009': 'verificationStatus',
    '258214002': 'stage',
    '260864003': 'periodicity',
    '418775008': 'findingMethod'
}


class DataHandler:

    def __init__(self):
        with open(base_path + '/Full/Terminology/sct2_StatedRelationship_Full_US1000124_20180901.txt', encoding="utf8") as f:
            reader = csv.DictReader(f, delimiter='\t')

            X_sent = []
            X_shortest_path = []
            X_src = []
            X_tgt = []
            X_src_txt = []
            X_tgt_txt = []
            y = []

            for row in [row for row in reader if row['typeId'] in sct_id_to_rel_name]:
                source = row['sourceId']
                target = row['destinationId']
                rel = row['typeId']

                if rel in sct_id_to_rel_name:
                    rel_name = sct_id_to_rel_name[rel]

                    sent = ""

                    src_text = server_client.get_name_with_type(source).split(" (")[0].lower()
                    tgt_text = server_client.get_name_with_type(target).split(" (")[0].lower()

                    src_concept = self._to_concept(server_client.sct_to_cui(source), src_text)
                    tgt_concept = self._to_concept(server_client.sct_to_cui(target), tgt_text)

                    X_sent.append(sent)
                    X_shortest_path.append("")
                    X_src.append(src_concept)
                    X_tgt.append(tgt_concept)
                    X_src_txt.append(src_text)
                    X_tgt_txt.append(tgt_text)
                    y.append(rel_name)

        test, train_and_validation = train_test_split(list(zip(X_sent, X_shortest_path, X_src, X_tgt, X_src_txt, X_tgt_txt, y)), train_size=0.5)

        self.test_data = list(zip(*test))

        train, validation = train_test_split(train_and_validation, train_size=0.5)

        self.train_data = list(zip(*train))[:-1] # strip off the label
        self.validation_data = list(zip(*validation))

    def get_test_data(self):
        return self.test_data

    def get_validation_data(self):
        return self.validation_data

    def get_training_data(self):
        return self.train_data

    def _to_concept(self, cuis, desc):
        return [metamap.metamap.Concept(cui=cui, semtypes=[], trigger=desc, description=desc, offsets="", score="", negated=False, pos="") for cui in cuis]
