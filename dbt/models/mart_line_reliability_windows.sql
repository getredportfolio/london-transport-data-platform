
with lines as (
    select * from {{ref('stg_tube_lines')}}
),
statuses as (
    select * from {{ref('stg_tube_status_snapshots')}}
) select lines.line_id, lines.line_name,

sum (
    case 
    when statuses.observed_at >= current_timestamp - interval '7 days'
    then 1
    else 0
    end
) as observations_7d,

sum (
    case
    when statuses.observed_at >= current_timestamp - interval '7 days'
    and statuses.status_severity = 10
    then 1
    else 0
    end
) as good_observations_7d,

round(
    100.0
    * sum(
        case
            when statuses.observed_at >= current_timestamp - interval '7 days'
                and statuses.status_severity = 10
            then 1
            else 0
        end
    )
    / nullif(
        sum(
            case
                when statuses.observed_at >= current_timestamp - interval '7 days'
                then 1
                else 0
            end
        ),
        0
    ),
    2
) as reliability_percentage_7d,

sum (
    case 
    when statuses.observed_at >= current_timestamp - interval '30 days'
    then 1
    else 0
    end
) as observations_30d,

sum (
    case
    when statuses.observed_at >= current_timestamp - interval '30 days'
    and statuses.status_severity = 10
    then 1
    else 0
    end
) as good_observations_30d,

round(
    100.0
    * sum(
        case
            when statuses.observed_at >= current_timestamp - interval '30 days'
                and statuses.status_severity = 10
            then 1
            else 0
        end
    )
    / nullif(
        sum(
            case
                when statuses.observed_at >= current_timestamp - interval '30 days'
                then 1
                else 0
            end
        ),
        0
    ),
    2
) as reliability_percentage_30d,

sum (
    case 
    when statuses.observed_at >= current_timestamp - interval '90 days'
    then 1
    else 0
    end
) as observations_90d,

sum (
    case
    when statuses.observed_at >= current_timestamp - interval '90 days'
    and statuses.status_severity = 10
    then 1
    else 0
    end
) as good_observations_90d,

round(
    100.0
    * sum(
        case
            when statuses.observed_at >= current_timestamp - interval '90 days'
                and statuses.status_severity = 10
            then 1
            else 0
        end
    )
    / nullif(
        sum(
            case
                when statuses.observed_at >= current_timestamp - interval '90 days'
                then 1
                else 0
            end
        ),
        0
    ),
    2
) as reliability_percentage_90d

from lines
left join statuses
on lines.line_id = statuses.line_id
group by lines.line_id, lines.line_name
