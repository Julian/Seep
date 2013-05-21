from unittest import TestCase

import jsonschema
import seep


class TestExtract(TestCase):
    def test_validation_error(self):
        with self.assertRaises(jsonschema.ValidationError):
            seep.instantiate("foo", {"type" : "integer"})

    def test_annotate(self):
        instance = {"foo" : 12}
        schema = {"properties" : {"foo" : {"annotate" : "bar"}}}
        self.assertEqual(seep.instantiate(instance, schema), {"bar" : 12})
