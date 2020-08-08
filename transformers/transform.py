'''
Classes to transform relationship graphs into standardized representations
'''

from abc import abstractmethod

from typing import List
import json

from fhir.resources.coding import Coding
from fhir.resources.extension import Extension
from fhir.resources.narrative import Narrative

from graph import Graph, Node, Edge

import server_client

import uuid

from fhir.resources.condition import Condition, ConditionStage
from fhir.resources.fhirreference import FHIRReference
from fhir.resources.codeableconcept import CodeableConcept

from rdflib.graph import Graph as RdfGraph
from rdflib import Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD, SKOS

from rdflib.extras.infixowl import BooleanClass, Restriction

import string

class BaseTransformer:

    @abstractmethod
    def transform(self, graph: Graph) -> any:
        pass

    @abstractmethod
    def serialize(self, payload: any) -> str:
        pass

class DefaultTransformer(BaseTransformer):

    def transform(self, graph: Graph) -> any:
        return graph

    def serialize(self, payload: Graph) -> str:
        return json.dumps(payload.to_json(), indent='\t')


class SnomedExpressionTransformer(BaseTransformer):

    def transform(self, graph: Graph) -> any:
        return f'''{self._get_sct_expr(graph.root, graph)}'''

    def _get_sct_expr(self, id: int, graph: Graph, depth=0, indent="\t"):
        children = list(filter(lambda x: x.src_id == id, graph.edges))

        focus = self._get_sct_display_graph(id, graph)

        if len(children) > 0:
            attributes_list = []
            for child in children:
                attributes_list.append(f'{indent * (depth+1)}{self._get_sct_display_sctid(child.relation)} = {self._get_sct_expr(child.tgt_id, graph, depth=depth+1, indent=indent)}')

            attributes = "\n".join(attributes_list)

            if depth > 0:
                return f'({focus}: \n{attributes})'
            else:
                return f'{focus}: \n{attributes}'
        else:
            return focus

    def _get_sct_display_graph(self, id: int, graph: Graph):
        if len(graph.nodes[id].sct_ids) == 0:
            umls = graph.nodes[id].cuis[0]
            return f"**{umls.cui}|{umls.description}**"
        else:
            return self._get_sct_display_sctid(graph.nodes[id].sct_ids[0])

    def _get_sct_display_sctid(self, sct_id: str):
        return server_client.expand_sct_code(sct_id)

    def serialize(self, payload: Graph) -> str:
        return payload



class FhirConditionTransformer(BaseTransformer):

    CLINICAL_FINDING = '404684003'

    def __init__(self):
        self.expression_transformer = SnomedExpressionTransformer()

    def transform(self, graph: Graph) -> Condition:
        controlled_rels = set([
            '363698007', '246112005', '408729009', '263493007', '258214002', '42752001', '255234002', '47429007'
        ])

        condition = Condition()
        condition.subject = FHIRReference()
        condition.code = self._to_codeable_concept(graph.root, graph)

        narrative = Narrative()
        narrative.status = 'additional'
        narrative.div = graph.text

        condition.text = narrative

        body_sites = self._get_object_nodes(graph.root, '363698007', graph)

        if len(body_sites) > 0:
            condition.bodySite = [self._to_codeable_concept(body_site, graph) for body_site in body_sites]

        for code, set_fn in [
            ('246112005', 'severity'),
            ('408729009', 'verificationStatus'),
            ('263493007', 'clinicalStatus')
        ]:
            nodes = self._get_object_nodes(graph.root, code, graph)
            if len(nodes) > 0:
                if len(nodes) > 1:
                    print("WARNING: More than one " + set_fn)

                setattr(condition, set_fn, self._to_codeable_concept(nodes[0], graph))

        stages = self._get_object_nodes(graph.root, '258214002', graph)

        if len(stages) > 0:

            def to_stage(stage):
                cs = ConditionStage()
                cs.summary = self._to_codeable_concept(stage, graph)
                return cs

            condition.stage = list(map(to_stage, stages))

        extensions = []

        for sct_id, url in [
            ("42752001", "http://hl7.org/fhir/StructureDefinition/condition-dueTo"),
            ("47429007", "http://hl7.org/fhir/StructureDefinition/condition-related"),
            ("255234002", "http://hl7.org/fhir/StructureDefinition/condition-occurredFollowing")]:
            extensions += self._as_extensions(graph.root, sct_id, url, graph)

        unused_edges = list(filter(lambda n: n.src_id == graph.root and n.relation not in controlled_rels, graph.edges))


        def is_clinical_finding(id):
            return any([server_client.is_super(self.CLINICAL_FINDING, sct_id) for sct_id in graph.nodes[id].sct_ids])

        for unused_edge in unused_edges:
            if unused_edge.relation == '246061005' and is_clinical_finding(unused_edge.tgt_id):
                extensions.append(self._as_extension(unused_edge.tgt_id, "http://hl7.org/fhir/StructureDefinition/condition-related", graph))
            else:
                extensions.append(self._as_extension(unused_edge.tgt_id, f"http://hl7.org/fhir/StructureDefinition/condition-{unused_edge.relation}", graph))

        if len(extensions) > 0:
            condition.extension = extensions

        return condition

    def _as_extensions(self, root: int, relation: str, url: str, graph: Graph) -> List[Extension]:
        node_ids = self._get_object_nodes(root, relation, graph)

        return list(map(lambda n: self._as_extension(n, url, graph), node_ids))

    def _as_extension(self, node: int, url: str, graph: Graph) -> List[Extension]:
        extension = Extension()
        extension.url = url
        extension.valueCodeableConcept = self._to_codeable_concept(node, graph)

        return extension

    def _get_object_nodes(self, root: int, relation: str, graph: Graph) -> List[Node]:
        return list(map(lambda x: x.tgt_id, filter(lambda x: x.src_id == root and x.relation == relation, graph.edges)))

    def _to_codeable_concept(self, node: int, graph: Graph):
        cc = CodeableConcept({'coding': [
            {'code': sct_id,
             'system': 'http://snomed.info/sct',
             'display': server_client.get_name_with_type(sct_id)} for sct_id in graph.nodes[node].sct_ids
        ]})

        nested = len(list(filter(lambda x: x.src_id == node, graph.edges))) > 0

        if nested:
            coding = Coding()
            coding.system = 'http://snomed.info/sct'
            coding.code = self.expression_transformer._get_sct_expr(node, graph)

            cc.coding.append(coding)

        return cc

    def serialize(self, payload: Condition) -> str:
        return json.dumps(payload.as_json(), indent='\t')


class OwlTransformer(BaseTransformer):

    pl_ns = Namespace("http://local/pl#") # change to some meaningful URI
    sct_ns = Namespace("http://snomed.info/id/")
    umls_ns = Namespace("http://www.nlm.nih.gov/research/umls/")

    def transform(self, graph: Graph, instances=True, expression=True) -> any:
        g = RdfGraph()

        g.bind("pl", self.pl_ns)
        g.bind("sct", self.sct_ns)
        g.bind("umls", self.umls_ns)
        g.bind("owl", OWL)
        g.bind("skos", SKOS)

        text = graph.text

        main_class = self.pl_ns[self._convert(text)]

        class_expression, main_individual = self._node_to_class(graph.root, graph, g, instances, expression)

        if expression:
            g.add((main_class, RDF.type, OWL.Class))

            g.add((main_class, OWL.equivalentClass, class_expression))

            g.add((main_class,
                           RDFS.label,
                           Literal(graph.text)))

        if instances:
            g.add((main_individual,
                   RDFS.label,
                   Literal(graph.text)))

        return g

    def _node_to_class(self, id: int, graph: Graph, rdf_graph: RdfGraph, instances: bool, expression: bool):
        node = graph.nodes[id]

        instance = self.pl_ns[str(uuid.uuid4())]

        blank_nodes = []

        for cui in node.cuis:
            cui_class = self.umls_ns[cui.cui]
            rdf_graph.add((cui_class, RDF.type, OWL.Class))

            rdf_graph.add((cui_class,
                   RDFS.label,
                   Literal(cui.description)))

            rdf_graph.add((cui_class,
                           SKOS.notation,
                           Literal(cui.cui)))

            if expression:
                blank_nodes.append(cui_class)

            if instances:
                rdf_graph.add((instance, RDF.type, cui_class))

        for sct_id in node.sct_ids:
            sct_class = self.sct_ns[sct_id]
            rdf_graph.add((sct_class, RDF.type, OWL.Class))

            rdf_graph.add((sct_class,
                           RDFS.label,
                           Literal(server_client.get_name_with_type(sct_id))))

            rdf_graph.add((sct_class,
                           SKOS.notation,
                           Literal(sct_id)))

            if expression:
                blank_nodes.append(sct_class)

            if instances:
                rdf_graph.add((instance, RDF.type, sct_class))

        if expression:
            classes_class = BooleanClass(
                operator=OWL.unionOf, members=blank_nodes, graph=rdf_graph).identifier

            blank_nodes = [classes_class]

        for edge in self._get_edges_for_src(id, graph):
            predicate = self.sct_ns[edge.relation]

            rdf_graph.add((predicate, RDF.type, OWL.ObjectProperty))
            rdf_graph.add((predicate,
                   RDFS.label,
                   Literal(server_client.get_name_with_type(edge.relation))))

            inner_class, inner_instance = self._node_to_class(edge.tgt_id, graph, rdf_graph, instances, expression)

            if expression:
                blank_nodes.append(
                    Restriction(graph=rdf_graph, onProperty=predicate, someValuesFrom=inner_class).identifier
                )

            if instances:
                rdf_graph.add((instance, predicate, inner_instance))

        return \
            BooleanClass(members=blank_nodes, graph=rdf_graph).identifier if expression else None, \
            instance if instances else None

    def _get_edges_for_src(self, src: int, graph: Graph) -> List[Edge]:
        return list(filter(lambda x: x.src_id == src, graph.edges))

    def _convert(self, s):
        s = s.translate(str.maketrans('', '', string.punctuation))
        s = ''.join(x for x in s.title() if not x.isspace())

        return s

    def serialize(self, payload: RdfGraph, format='turtle', file_name=None) -> str:
        if file_name:
            payload.serialize(destination=file_name, format=format)

        return payload.serialize(format=format).decode("utf-8")