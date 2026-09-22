from unittest.mock import patch

from tfl_pipeline.api import fetch_tube_lines


def test_fetch_tube_lines_returns_api_data():
    fake_data = [{"id": "1", "name": "Central"}, {"id": "2", "name": "Lizzie"}] 
    with patch("tfl_pipeline.api.requests.get") as mock_get: #mock api call to mock the actual requests
        mock_get.return_value.json.return_value = fake_data #rwhen the fake HTTP response's JSON method is called, return the fake data
        data = fetch_tube_lines()
        mock_get.assert_called_once_with("https://api.tfl.gov.uk/Line/Mode/tube", timeout=30)
        mock_get.return_value.raise_for_status.assert_called_once()

    assert len(data) > 0
    assert isinstance(data, list)
    assert data == fake_data
    