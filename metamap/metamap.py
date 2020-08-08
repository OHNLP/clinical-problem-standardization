"""
A high-throughput utility to run Metamap on a set of files.
"""

import csv
import itertools
import multiprocessing
import subprocess
from multiprocessing.pool import ThreadPool

import numpy as np
import pickledb
import requests


class Concept:
    def __init__(self, trigger, cui, description, semtypes, offsets, score, negated, pos):
        self.trigger = trigger
        self.cui = cui
        self.description = description
        self.semtypes = semtypes
        self.offsets = offsets
        self.score = score
        self.negated = negated
        self.pos = pos

    @staticmethod
    def get_concepts_from_mm(fields, text, lite=False):
        concepts = []

        offset_field = fields[7 if lite else 8]
        for offset in offset_field.split(';'):
            offsets = list(map(lambda x: x.strip('[]'), offset.split('],[')))
            for offset_ in offsets:
                concept = Concept(
                    Concept.__get_trigger(fields, text),
                    fields[4],
                    fields[3],
                    Concept.__get_semtypes(fields),
                    offset_,
                    Concept.__get_score(fields),
                    Concept.__get_negated(fields),
                    Concept.__get_pos(fields)
                )

                concepts.append(concept)

        return concepts

    @staticmethod
    def __get_score(fields):
        if fields[1] == 'AA':
            return 0.0
        else:
            return float(fields[2])

    @staticmethod
    def __get_trigger(fields, line):
        if fields[1] == 'AA':
            trigger = fields[8].split(':')
            start = int(trigger[0])
            end = start + int(trigger[1])
            return line[start:end]
        else:
            return next(csv.reader([fields[6].strip('[]')], delimiter='-'))[3]

    @staticmethod
    def __get_pos(fields):
        if fields[1] == 'AA':
            return 'noun'
        else:
            return next(csv.reader([fields[6].strip('[]')], delimiter='-'))[4]

    @staticmethod
    def __get_negated(fields):
        return False#int(next(csv.reader([fields[6].strip('[]')], delimiter='-'))[5]) == 1

    @staticmethod
    def __get_semtypes(fields):
        return fields[5].strip('[]').split(",")

    def __str__(self) -> str:
        return self.cui + " : " + self.description + " : " + str(self.semtypes) + str(self.offsets)



class MetaMap:

    def __init__(self, metamap_exe="metamap", metamaplite_url="http://localhost:8080/", workers=max(multiprocessing.cpu_count() - 1, 1), additional_args='-z -y'):
        self.metamap_exe = metamap_exe
        self.workers = workers
        self.pool = ThreadPool(workers)
        self.metamaplite_url = metamaplite_url
        self.additional_args = additional_args
        self.db = pickledb.load('metamap.db', False, False)

    def _call_metamaplite(self, batch):
        response = requests.post(self.metamaplite_url, data="\n".join(batch))

        if response.status_code == 200:
            return response.text
        else:
            print(response.text)
            return ""

    def call_metamap_batch(self, texts, lite=False, batch_size=20):
        batches = max(len(texts)/ batch_size, 1)

        if lite:
            def process(batch):
                groups = [None]*len(batch)
                for i, text in enumerate(batch):
                    groups[i] = []

                output = self._call_metamaplite(batch)

                for line in output.splitlines(keepends=False):
                    group = int(line.split('|', maxsplit=2).pop(0))
                    groups[group].append(line)

                concepts = []
                for i, text in enumerate(batch):
                    concepts.append(self.metamap_output_to_concept(text, groups[i], True))

                return concepts

            return self.flatmap(self.pool.map(process, [x for x in np.array_split(np.array(texts), batches) if len(x) > 0]))
        else:
            txt_batches = np.array_split(texts, batches)
            return [b for batch in self.pool.map(self.call_metamap, txt_batches) for b in batch]


    def call_metamap_raw(self, text):
        """cal metamap via a subprocess"""
        text = [str(i) + "|" + txt.strip() + "\n" for i, txt in enumerate(text)]
        if not text:
            return []

        p = subprocess.Popen([self.metamap_exe, "--sldiID", "-Z", "2018AB", "-L", "2018AB", "-N", "--silent", self.additional_args], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.write("\n".join(text).encode("utf-8"))
        output, err = p.communicate()

        if err is not None:
            raise BaseException(err)

        output_dict = {}

        for line in output.decode("utf-8").splitlines()[1:]:
            id = int(line.split('|')[0])
            if id not in output_dict:
                output_dict[id] = []
            output_dict[id].append(line)

        results = [[] for _ in range(len(text))]

        for i in range(0, len(results) + 1):
            if i in output_dict:
                results[i] += output_dict[i]

        return results

    def call_metamap(self, text):
        key = "".join(text)
        if self.db.exists(key):
            output = self.db.get(key)
        else:
            output = self.call_metamap_raw(text)
            self.db.set(key, output)

        return [self.metamap_output_to_concept(t, o) for t, o in zip(text, output)]

    def metamap_output_to_concept(self, text, output, lite=False):
        result = []

        for line in output:
            fields = line.split("|")

            for c in Concept.get_concepts_from_mm(fields, text, lite):
                result.append(c)

        return result

    def flatmap(self, l):
        """list of lists --> one big list"""
        return list(itertools.chain(*l))

    def format(self, result):
        """turn the CUI/text tuple into a string"""
        return "%s,%s\n" % result

