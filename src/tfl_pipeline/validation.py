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

class TubeStatusSnapshot(BaseModel):
    line_id: str
    status_severity: int
    status_description: str

def validate_tube_statuses(data):
    results = []
    for line in data:
        for status in line["lineStatuses"]:
            result = TubeStatusSnapshot(
                line_id=line["id"],
                status_severity=status["statusSeverity"],
                status_description=status["statusSeverityDescription"]
            )
            results.append(result)

    return results
        







