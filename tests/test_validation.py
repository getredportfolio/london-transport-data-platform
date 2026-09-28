import pytest
from pydantic import ValidationError

from tfl_pipeline.validation import TubeLine, validate_tube_lines


def test_tube_line_positive_validation():
    data = { "id" : "central", "name" : "Central"} #creating fake data
    line = TubeLine(**data) #calling the fake data in the object we created earlier

    assert line.id == "central" #checking whether fake data matches object
    assert line.name == "Central" #checking whether fake data matches object


def test_tube_line_negative_validation():
    data = { "id" : "central"} #creating fake incomplete data

    with pytest.raises(ValidationError):
        TubeLine(**data) #checking whether fake incomplete data raises an error


def test_validate_tube_lines():
    data = [
    {"id": "central", "name": "Central"},
    {"id": "victoria", "name": "Victoria"}
    ]
    validated = validate_tube_lines(data)
    assert len(validated) == 2
    assert isinstance(validated, list)
    assert isinstance(validated[0], TubeLine)
    assert validated[0].id == "central"

def test_validate_tube_line_missing_name():
    data = [
    {"id": "central", "name": "Central"},
    {"id": "victoria"}
    ]
    with pytest.raises(ValidationError):
        validate_tube_lines(data) #checking whether the missing name triggers a validation error message

    