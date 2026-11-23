select * from {{ref ('mart_line_reliability_windows')}}
where
reliability_percentage_7d < 0
or reliability_percentage_7d > 100
or reliability_percentage_30d < 0
or reliability_percentage_30d > 100
or reliability_percentage_90d < 0
or reliability_percentage_90d > 100