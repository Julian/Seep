import jsonschema.validators


def _set_defaults(validator, properties, instance, schema):
    for property, subschema in properties.items():
        if "default" in subschema and property not in instance:
            instance[property] = subschema["default"]


DefaultSetter = jsonschema.validators.create(
    meta_schema={}, validators={"properties": _set_defaults},
)


def extend(validator_cls):
    """
    Extend the given :class:`jsonschema.IValidator` with the Seep layer.

    """

    Validator = jsonschema.validators.extend(
        validator_cls, {
            "properties" : _properties_with_defaults(validator_cls),
        }
    )

    class Blueprinter(Validator):
        def instantiate(self, data):
            self.validate(data)
            return data

    return Blueprinter


def instantiate(data, blueprint):
    """
    Instantiate the given data using the blueprinter.

    :argument blueprint: a blueprint (JSON Schema with Seep properties)

    """

    Validator = jsonschema.validators.validator_for(blueprint)
    blueprinter = extend(Validator)(blueprint)
    return blueprinter.instantiate(data)


def _properties_with_defaults(validator_cls):
    def properties_with_defaults(validator, properties, instance, schema):
        for error in validator_cls.VALIDATORS["properties"](
            validator, properties, instance, schema
        ):
            yield error

        subschemas = [(instance, schema)]
        while subschemas:
            subinstance, subschema = subschemas.pop()
            DefaultSetter(subschema).validate(subinstance)
            subschemas.extend(
                (subinstance.setdefault(property, {}), subsubschema)
                for property, subsubschema in
                subschema.get("properties", {}).items()
            )

    return properties_with_defaults
