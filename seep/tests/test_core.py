from unittest import TestCase

import jsonschema
import seep.core


class TestInstantiate(TestCase):
    def test_it_sets_defaults(self):
        data = {}
        schema = {"properties" : {"foo" : {"default" : 12}}}
        seep.core.instantiate(data, schema)
        self.assertEqual(data, {"foo" : 12})

    def test_it_sets_nested_defaults(self):
        data = {}
        schema = {
            "properties" : {
                "foo" : {
                    "default" : {},
                    "properties" : {"bar" : {"default" : []}},
                }
            }
        }
        seep.core.instantiate(data, schema)
        self.assertEqual(data, {"foo" : {"bar" : []}})

    def test_it_sets_multiple_nested_defaults(self):
        data = {}
        schema = {
            "properties" : {
                "bar" : {"default" : 123},
                "foo" : {
                    "default" : {},
                    "properties" : {
                        "bar" : {
                            "properties": {"baz" : {"default" : []}},
                        },
                    },
                },
            }
        }
        seep.core.instantiate(data, schema)
        self.assertEqual(data, {"bar": 123, "foo" : {"bar" : {"baz" : []}}})

    def test_identity_instantiate(self):
        data = {"foo" : 12}
        schema = {"properties" : {"foo" : {}}}
        seep.core.instantiate(data, schema)
        self.assertEqual(data, {"foo" : 12})

    def test_validation_errors_are_still_errors(self):
        with self.assertRaises(jsonschema.ValidationError):
            seep.core.instantiate("foo", {"type" : "integer"})
