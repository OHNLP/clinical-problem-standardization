'''
Utility class over cui2vec vectors (see: http://cui2vec.dbmi.hms.harvard.edu/)
'''


import numpy as np
import os
import server_client

use_server = "USE_SERVER" in os.environ

if use_server:
    client = os.environ['CUI2VEC_HOME']
else:
    import umls.umls as umls

    class LocalClient:
        def get_parents(self, c):
            return umls.get_parents(c)

    client = LocalClient()


class Cui2Vec():

    def __init__(self):
        if 'CUI2VEC_HOME' in os.environ:
            cui2vec_path = os.environ['CUI2VEC_HOME']
        else:
            raise Exception("Please set the `CUI2VEC_HOME` variable to the base of your cui2vec file.")

        cui2vec_ = {}
        with open(cui2vec_path) as f:
            next(f)
            for line in f.readlines():
                tokens = line.split(",")
                cui = tokens.pop(0).strip('\"')
                cui2vec_[cui] = np.array([float(x) for x in tokens])

        self.dims = 500

        print("Loaded UMLS Concept vectors:", len(cui2vec_))

        self.embeddings = cui2vec_

        self.hits = 0
        self.misses = 0

    def cui2vec(self, concepts):
        for concept in concepts:
            if concept.cui in self.embeddings:
                self.hits += 1
                return self.embeddings[concept.cui]

        for concept in concepts:
            for parent in server_client.get_parents(concept.cui):
                if parent in self.embeddings:
                    self.hits += 1
                    return self.embeddings[parent]

        self.misses += 1
        return np.zeros(self.dims)
