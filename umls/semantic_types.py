'''
Utilities for processing semantic types
'''

import pkg_resources

lines = list(map(lambda x: x.split('|'), open(pkg_resources.resource_filename(__name__, 'SemanticTypes_2018AB.txt')).readlines()))

abbreviation_to_id = {x[0]: x[1] for x in lines}
id_to_abbreviation = {x[1]: x[0] for x in lines}

groups = {line[2]:line[0] for line in
    list(map(lambda x: x.split('|'), open(pkg_resources.resource_filename(__name__, 'SemGroups_2018.txt')).readlines()))
}

group_names = ["NONE"] + list(sorted(list(set(groups.values()))))
names = ["NONE"] + list(sorted(list(set(abbreviation_to_id.keys()))))

def get_sem_type(concepts):
    types = []
    for c in concepts:
        types += c.semtypes
    return types


def get_semantic_group_from_concept(concepts):
    types = []
    for concept in concepts:
        for semtype in concept.semtypes:
            if semtype in abbreviation_to_id:
                types.append(groups[abbreviation_to_id[semtype]])

    return types
