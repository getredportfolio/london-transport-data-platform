from pydantic import BaseModel


class TubeLine(BaseModel):
    id : str
    name : str


def validate_tube_lines(data):
    results = []
    for line in data:
        result = TubeLine(**line) #converting each item in the dictionary to an object
        results.append(result)

    return results
        







