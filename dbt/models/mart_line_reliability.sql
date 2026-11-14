with lines as (
    select * from {{ ref ('stg_tube_lines')}}
),
statuses as (
    select * from {{ref ('stg_tube_status_snapshots')}}
)
select lines.line_id,
lines.line_name,
count(statuses.snapshot_id) as total_observations,

sum(
    case when
    statuses.status_severity = 10 then 1
    else 0
    end
) as good_service_observations,

sum(
    case when
    statuses.status_severity <> 10 then 1
    else 0
    end
) as disrupted_observations,

round(
    100.0
    * sum(
        case when
        statuses.status_severity = 10 then 1
        else 0
        end
    )
    / nullif(count(statuses.snapshot_id),0),
    2
) as reliability_percentage

from lines left join statuses on lines.line_id = statuses.line_id
group by lines.line_id, lines.line_name