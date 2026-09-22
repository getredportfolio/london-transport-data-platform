import requests


def fetch_tube_lines():
    tfl_tube_lines_url = "https://api.tfl.gov.uk/Line/Mode/tube"
    tfl_tube_lines_data_call = requests.get(tfl_tube_lines_url, timeout=30)
    tfl_tube_lines_data_call.raise_for_status()
    tfl_tube_lines_data = tfl_tube_lines_data_call.json()

    return tfl_tube_lines_data