from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from tfl_pipeline.api import fetch_tube_lines, fetch_tube_status


def test_fetch_tube_lines_returns_api_data():
    fake_data = [{"id": "central", "name": "Central"}, {"id": "elizabeth", "name": "Lizzie"}] 
    with patch("tfl_pipeline.api.requests.get") as mock_get: #mock api call to mock the actual requests
        mock_get.return_value.json.return_value = fake_data #rwhen the fake HTTP response's JSON method is called, return the fake data
        data = fetch_tube_lines()
        mock_get.assert_called_once_with("https://api.tfl.gov.uk/Line/Mode/tube", timeout=30)
        mock_get.return_value.raise_for_status.assert_called_once()

    assert len(data) > 0
    assert isinstance(data, list)
    assert data == fake_data

def test_fetch_tube_status_returns_api_data():
    fake_data = [{"line_id" : "1", "line_name" : "Central", "status" : "active"},{"line_id" : "2", "line_name" : "Lizzie", "status" : "Never really works does it"} ]
    with patch ("tfl_pipeline.api.requests.get") as mock_get:
        mock_get.return_value.json.return_value = fake_data
        data = fetch_tube_status()
        mock_get.assert_called_once_with("https://api.tfl.gov.uk/Line/Mode/tube/Status", timeout=30)
        mock_get.return_value.raise_for_status.assert_called_once()

    assert len(data) > 0
    assert isinstance(data, list)
    assert data == fake_data

def test_fetch_tube_status_raises_on_http_error():
    with patch ("tfl_pipeline.api.requests.get") as mock_get:
        mock_get.return_value.raise_for_status.side_effect = HTTPError("500 Server Error")
        with pytest.raises(HTTPError):
            fetch_tube_status()

