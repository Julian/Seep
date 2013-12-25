from unittest import TestCase

import jsonschema
import seep


class TestInstantiate(TestCase):
    def test_it_sets_defaults(self):
        data = {}
        schema = {"properties" : {"foo" : {"default" : 12}}}
        seep.instantiate(data, schema)
        self.assertEqual(data, {"foo" : 12})

    def test_identity_instantiate(self):
        data = {"foo" : 12}
        schema = {"properties" : {"foo" : {}}}
        seep.instantiate(data, schema)
        self.assertEqual(data, {"foo" : 12})

    def test_validation_errors_are_still_errors(self):
        with self.assertRaises(jsonschema.ValidationError):
            seep.instantiate("foo", {"type" : "integer"})
