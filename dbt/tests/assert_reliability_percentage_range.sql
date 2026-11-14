select * from {{ref ('mart_line_reliability')}}
where reliability_percentage < 0 or reliability_percentage > 100
