import jsonschema.validators


def instantiate(data, blueprint):
    """
    Instantiate the given data using the blueprinter.

    :argument blueprint: a blueprint (JSON Schema with Seep properties)

    """

    Validator = jsonschema.validators.validator_for(blueprint)
    blueprinter = _make_blueprinter(Validator)(blueprint)
    return blueprint_using(blueprinter, data)


def _make_blueprinter(Validator):
    return jsonschema.validators.extend(
        Validator, {
            "rename" : _rename,
        }
    )


def blueprint_using(blueprinter, data):
    blueprinter._seep = {}
    blueprinter.validate(data)
    return blueprinter._seep.get("names")


def _rename(validator, annotation, instance, schema):
    annotations = validator._seep.setdefault("names", {})
    annotations[annotation] = instance
