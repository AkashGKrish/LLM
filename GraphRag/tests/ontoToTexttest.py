import unittest
from rdflib import Graph, Literal, URIRef
from ontoToText import get_ontology_data

class TestGetOntologyData(unittest.TestCase):

    def test_empty_graph(self):
        graph = Graph()
        result = get_ontology_data(graph)
        self.assertEqual(result, [])

    def test_single_subject_no_predicates(self):
        graph = Graph()
        subject = URIRef("http://example.com/subject1")  # Use URIRef for subject
        predicate = URIRef("http://example.com/predicate")  # Use URIRef for predicate
        object_literal = Literal("object value")  # Use Literal for object (if it's a string)
        graph.add((subject, predicate, object_literal))
        result = get_ontology_data(graph)
        self.assertEqual(len(result), 1)
        self.assertIn("Subject: {}".format(subject), result[0])
        self.assertIn("Objects and Predicates:", result[0])

    def test_single_subject_multiple_predicates(self):
        graph = Graph()
        subject = URIRef("http://example.com/subject1")
        predicate1 = URIRef("http://example.com/predicate1")
        object1 = Literal("object value 1")
        predicate2 = URIRef("http://example.com/predicate2")
        object2 = Literal("object value 2")
        graph.add((subject, predicate1, object1))
        graph.add((subject, predicate2, object2))
        result = get_ontology_data(graph)
        self.assertEqual(len(result), 1)
        self.assertIn("Subject: {}".format(subject), result[0])
        self.assertIn("Predicate: {}, Object: {}".format(predicate1, object1), result[0])
        self.assertIn("Predicate: {}, Object: {}".format(predicate2, object2), result[0])

    def test_multiple_subjects_multiple_predicates(self):
        graph = Graph()
        subject1 = URIRef("http://example.com/subject1")
        predicate1 = URIRef("http://example.com/predicate1")
        object1 = Literal("object value 1")
        predicate2 = URIRef("http://example.com/predicate2")
        object2 = Literal("object value 2")
        subject2 = URIRef("http://example.com/subject2")
        predicate3 = URIRef("http://example.com/predicate3")
        object3 = Literal("object value 3")
        predicate4 = URIRef("http://example.com/predicate4")
        object4 = Literal("object value 4")
        graph.add((subject1, predicate1, object1))
        graph.add((subject1, predicate2, object2))
        graph.add((subject2, predicate3, object3))
        graph.add((subject2, predicate4, object4))
        result = get_ontology_data(graph)
        self.assertEqual(len(result), 2)
        self.assertIn("Subject: {}".format(subject1), result[0])
        self.assertIn("Predicate: {}, Object: {}".format(predicate1, object1), result[0])
        self.assertIn("Predicate: {}, Object: {}".format(predicate2, object2), result[0])
        self.assertIn("Subject: {}".format(subject2), result[1])
        self.assertIn("Predicate: {}, Object: {}".format(predicate3, object3), result[1])
        self.assertIn("Predicate: {}, Object: {}".format(predicate4, object4), result[1])

    def test_non_rdflib_graph(self):
        with self.assertRaises(AttributeError):
            get_ontology_data("not a graph")

if __name__ == "__main__":
    unittest.main()