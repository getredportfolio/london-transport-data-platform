from unittest.mock import patch

from tfl_pipeline.pipeline import run_ingestion


@patch("tfl_pipeline.pipeline.insert_tube_status_snapshots")
@patch("tfl_pipeline.pipeline.validate_tube_statuses")
@patch("tfl_pipeline.pipeline.fetch_tube_status")
@patch("tfl_pipeline.pipeline.upsert_tube_lines")
@patch("tfl_pipeline.pipeline.validate_tube_lines")
@patch("tfl_pipeline.pipeline.fetch_tube_lines")
def test_run_ingestion(mock_fetch_tube_lines,
                       mock_validate_tube_lines,
                        mock_upsert_tube_lines,
                        mock_fetch_tube_status,
                        mock_validate_tube_statuses,
                        mock_insert_tube_status_snapshot,
                        ):
    raw_lines = ["raw-line-data"]
    validated_lines = ["validated-line-data"]

    mock_fetch_tube_lines.return_value = raw_lines
    mock_validate_tube_lines.return_value = validated_lines

    raw_status = ["raw-status-data"]
    validated_status = ["validated-status-data"]

    mock_fetch_tube_status.return_value = raw_status
    mock_validate_tube_statuses.return_value = validated_status

    run_ingestion()

    #checking whether both the fetches worked
    mock_fetch_tube_status.assert_called_once_with()
    mock_fetch_tube_lines.assert_called_once_with()

    #checking whether both the validations worked
    mock_validate_tube_statuses.assert_called_once_with(raw_status)
    mock_validate_tube_lines.assert_called_once_with(raw_lines)

    #checking whether both the inserts worked
    mock_insert_tube_status_snapshot.assert_called_once_with(validated_status)
    mock_upsert_tube_lines.assert_called_once_with(validated_lines)
    
