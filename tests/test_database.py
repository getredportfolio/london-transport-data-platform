from unittest.mock import ANY, patch

from tfl_pipeline.database import insert_tube_status_snapshots, upsert_tube_lines
from tfl_pipeline.validation import TubeLine, TubeStatusSnapshot


@patch("tfl_pipeline.database.get_connection")
def test_upsert_tube_lines(mock_get_connection):
    central = TubeLine(id="central", name="Central")
    victoria = TubeLine(id="victoria", name="Victoria")

    lines = [victoria, central]

    mock_connection = mock_get_connection.return_value
    mock_cursor = mock_connection.cursor.return_value

    upsert_tube_lines(lines)

    assert mock_cursor.execute.call_count == 2
    mock_connection.commit.assert_called_once()

    mock_cursor.execute.assert_any_call(
        ANY,
        ("victoria", "Victoria"),

    )
    mock_cursor.execute.assert_any_call(
        ANY,
        ("central", "Central"),
    )

    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()


@patch("tfl_pipeline.database.get_connection")
def test_insert_tube_status_snapshots(mock_get_connection):
    central = TubeStatusSnapshot(line_id="central", status_severity=8, status_description="Minor Delays")
    victoria = TubeStatusSnapshot(line_id="victoria", status_severity=10, status_description="Good Service")
    snapshots = [central, victoria]

    mock_connection = mock_get_connection.return_value
    mock_cursor = mock_connection.cursor.return_value

    insert_tube_status_snapshots(snapshots)

    assert mock_cursor.execute.call_count == 2
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()

    mock_cursor.execute.assert_any_call(
        ANY,
        ("central", 8, "Minor Delays"),
    )

    mock_cursor.execute.assert_any_call(
        ANY,
        ("victoria", 10, "Good Service")
    )
