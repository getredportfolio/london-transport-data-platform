create table if not exists tube_status_snapshots(
    snapshot_id BIGSERIAL PRIMARY KEY,
    line_id TEXT NOT NULL REFERENCES tube_lines(line_id),
    observed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_severity INTEGER NOT NULL,
    status_description TEXT NOT NULL

)