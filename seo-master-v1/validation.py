import json
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
ROOT=Path(__file__).resolve().parent

def validate(kind,data):
    if kind not in ('project','evidence'):raise ValueError('Unknown schema')
    schema=json.loads((ROOT/'schemas'/f'{kind}.schema.json').read_text())
    validator=Draft202012Validator(schema,format_checker=FormatChecker())
    errors=list(validator.iter_errors(data))
    if errors:raise ValueError(f'{kind} schema violation: {errors[0].json_path}')
    return True
