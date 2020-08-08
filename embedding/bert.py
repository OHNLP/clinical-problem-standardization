'''
A wrapper for interacting with bert-as-service (https://github.com/hanxiao/bert-as-service)
'''


import os.path
import pickle

import numpy as np
from bert_serving.client import BertClient

FILE = './embeddings.db'

if os.path.isfile(FILE):
    embeddings_on_disk = pickle.load(open(FILE, 'rb'))
else:
    embeddings_on_disk = {}

bert_client = BertClient()

def bert_sent_embeddings(sents, batch_size=250, persist=True):
    size_before = len(embeddings_on_disk)

    chunks = max(1, int(len(sents) / batch_size))
    splits = np.array_split(sents, chunks)

    return_list = []
    for split in splits:
        return_list += _bert_sent_embeddings(split.tolist())

        # only print if we're doing batch
        if len(sents) > 1:
            print("Processed:", len(return_list), "of", len(sents))

    size_after = len(embeddings_on_disk)

    if persist and size_after > size_before:
        save()

    return return_list


def _bert_sent_embeddings(sents):
    todo_sents = [s for s in sents if s not in embeddings_on_disk]

    if len(todo_sents) > 0:
        retrieved_embeddings = bert_client.encode(todo_sents, is_tokenized=False)

        assert(len(retrieved_embeddings) == len(todo_sents))


        for sent, vec in zip(todo_sents, retrieved_embeddings):
            embeddings_on_disk[sent] = vec

    return [embeddings_on_disk[s] for s in sents]

def save():
    pickle.dump(embeddings_on_disk, open('./embeddings.db', 'wb+'))


