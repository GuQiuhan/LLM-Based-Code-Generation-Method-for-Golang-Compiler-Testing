import json

import jsonlines


def data_to_jsonl_append(path, data):
    with jsonlines.open(path, "a") as f:
        f.write(data)


def data_from_jsonl(path):
    with jsonlines.open(path, "r") as f:
        for line in f:
            yield line


def data_to_json_append(path, data):
    with open(path, "a") as f:
        f.write(json.dumps(data))


def data_from_json(path):
    with open(path, "r") as f:
        for line in json.load(f):
            yield line
