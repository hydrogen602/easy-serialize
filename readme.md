
# Easy-Serialize

Turn custom python objects into strings and vice-versa.

## Supports

- json
- nested objects
- no dependencies outside of python's library (only pytest for developing)

## Drawbacks

- objects like tuples are automatically turned into lists
- only supports json right now
- can't handle circular references
- if an object has references in many places, it will be present in the json repeatedly and after deserializing will be separate objects

