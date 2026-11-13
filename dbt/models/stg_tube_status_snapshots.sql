select snapshot_id, line_id, observed_at, status_severity, status_description
from {{source('tfl', 'tube_status_snapshots')}}