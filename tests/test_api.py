from tfl_pipeline.api import fetch_tube_lines

def test_api():
    data = fetch_tube_lines()
    assert len(data) > 0
    assert isinstance(data, list)