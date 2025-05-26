WITH date_metrics AS (
    SELECT DISTINCT
        review_time::date as date_id,
        EXTRACT(YEAR FROM review_time) as year,
        EXTRACT(MONTH FROM review_time) as month,
        EXTRACT(DOW FROM review_time) as day_of_week,
        CASE 
            WHEN EXTRACT(DOW FROM review_time) = 0 THEN 'Sunday'
            WHEN EXTRACT(DOW FROM review_time) = 1 THEN 'Monday'
            WHEN EXTRACT(DOW FROM review_time) = 2 THEN 'Tuesday'
            WHEN EXTRACT(DOW FROM review_time) = 3 THEN 'Wednesday'
            WHEN EXTRACT(DOW FROM review_time) = 4 THEN 'Thursday'
            WHEN EXTRACT(DOW FROM review_time) = 5 THEN 'Friday'
            ELSE 'Saturday'
        END as day_name
    FROM {{ ref('bank_reviews') }}
)

SELECT * FROM date_metrics