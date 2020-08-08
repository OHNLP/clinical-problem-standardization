from metamap.metamap import Concept

class Graph:

    def __init__(self, root: int, text: str):
        self.root = root
        self.nodes: Node = {}
        self.edges: Edge = []
        self.text = text

    def add_node(self, id: int, cuis: Concept, sct_ids: list, text: str) -> None:
        self.nodes[id] = Node(cuis, sct_ids, text)

    def add_edge(self, src_id: int, tgt_id: int, relation: str) -> None:
        self.edges.append(Edge(src_id, tgt_id, relation))

    def to_json(self):
        d = dict(self.__dict__)
        d['nodes'] = {k: v.to_json() for k, v in self.nodes.items()}
        d['edges'] = [e.to_json() for e in self.edges]

        return d


class Node:
    def __init__(self, cuis: Concept, sct_ids: list, text: str):
        self.cuis = cuis
        self.sct_ids = sct_ids
        self.text = text

    def to_json(self):
        d = dict(self.__dict__)
        d['cuis'] = [c.__dict__ for c in self.cuis]
        d['sct_ids'] = self.sct_ids

        return d

class Edge:
    def __init__(self, src_id: int, tgt_id: int, relation: str):
        self.src_id = src_id
        self.tgt_id = tgt_id
        self.relation = relation

    def to_json(self):
        return dict(self.__dict__)