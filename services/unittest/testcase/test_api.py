import json
import sys
from unittest.mock import Mock

sys.path.append("/by/source/")
print(sys.path)
from handlers.engine_inspection import EngineInspection
from schema.EnginePydantic import EngineInspectionSchema

get_results = []


class SessionMocker:
    def __init__(self, *args, **kwargs):
        pass

    def query(self, *args, **kwargs):
        return self

    def get(self, *args, **kwargs):
        return get_results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_get_engine_inspection():
    global get_results
    get_results = []
    results = EngineInspection(SessionMocker).get_engine_inspection("123")
    assert results == {"record": []}

    with open(r"/by/unittest/testdata/valid_data.json") as fd:
        data = json.load(fd)
    get_results = data
    test = EngineInspection(SessionMocker).get_engine_inspection("123")
    assert test == {"record": data}


def test_post_engine_inspection():
    # When schema is valid
    with open(r"/by/unittest/testdata/valid_post_data.json") as fd:
        full_data = json.load(fd)
    obj = EngineInspection(SessionMocker)
    obj.get_all_records_with_filter = Mock(return_value=[])
    results = obj.post_engine_inspection(full_data["valid_scenario"]["input"])
    assert results == full_data["valid_scenario"]["output"]
