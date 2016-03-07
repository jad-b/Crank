# Serializing

__JSON Object__ A `dict` with JSON-compatible types.

Data is stored as JSON. Serialized objects are responsible for dictating how
they go to and from JSON objects. This allows composite objects to delegate
serialization to their attributes.

Anything the builtin Python `json` module can't handle needs to be converted to an
acceptable format before encoding and after decoding.

An object needs to specify two methods to provide this behavior:

```Python
def to_json(self):
    """Return a JSON object fit for serialization."""
    d = {}
    # Call to_json() on all attributes needing conversion
    return d

@classmethod
def from_json(cls, json_object):
    """Convert the JSON-serialized values into their correct type."""
    obj = cls(**json_object)
    # Call from_json() on all JSON-serialized attributes
    return obj
```

Only top-level objects used in `json.dump|load` calls need to implement a custom
JSON Encoder and Decoder. The `decode(s)` allows for a standard decoding,
followed by recursively applying `from_json` to the hierarchy. The JSONEndoer's `default(o)`
method performs the same role, but in reverse.

```
class TopJSONEncoder(json.JSONEncoder):

    def default(self, o):
        return o.to_json() # Calls to_json on all sub-objects

class TopJSONDecoder(json.JSONDecoder):

    def decode(self, s):
        json_obj = super().decode(s)
        return TopLevelObject.from_json(json_obj) ```
```

The JSONEncoder can be avoided by modifying the top-level classes `to_json` to accept
an obj to encoded: `to_json(self, instance)`. As `self` and `instance` are the same,
this is probably better written `to_json(self, *args)`.
