import json

SUPPORTED_RESPONSE_FORMATS = set(["text", "json"])

def valid_response_format(f):
    return f in SUPPORTED_RESPONSE_FORMATS

def format_response(key, value, f):
    if f == "json":
        return json.dumps({
            key : value
        })
    else: #default to "text"
        return value    

