from tfl_pipeline.api import fetch_tube_lines, fetch_tube_status
from tfl_pipeline.database import insert_tube_status_snapshots, upsert_tube_lines
from tfl_pipeline.validation import validate_tube_lines, validate_tube_statuses


def run_ingestion():
    tube_lines_data = fetch_tube_lines()
    validated_lines = validate_tube_lines(tube_lines_data)
    upsert_tube_lines(validated_lines)

    tube_line_status = fetch_tube_status()
    validated_status = validate_tube_statuses(tube_line_status)
    insert_tube_status_snapshots(validated_status)
