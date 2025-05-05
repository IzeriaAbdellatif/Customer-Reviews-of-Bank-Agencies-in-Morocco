WITH month_metrics AS (
    SELECT 
        review_month as month_id,
        CASE review_month
            WHEN 1 THEN 'January'
            WHEN 2 THEN 'February'
            WHEN 3 THEN 'March'
            WHEN 4 THEN 'April'
            WHEN 5 THEN 'May'
            WHEN 6 THEN 'June'
            WHEN 7 THEN 'July'
            WHEN 8 THEN 'August'
            WHEN 9 THEN 'September'
            WHEN 10 THEN 'October'
            WHEN 11 THEN 'November'
            WHEN 12 THEN 'December'
        END as month_name,
        -- Overall satisfaction per month
        CONCAT(
            COUNT(CASE WHEN sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(*)::TEXT
        ) as overall_satisfaction,
        -- Beginning of month (days 1-10)
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) <= 10 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) <= 10 THEN 1 END)::TEXT
        ) as early_month_satisfaction,
        -- Middle of month (days 11-20)
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) BETWEEN 11 AND 20 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) BETWEEN 11 AND 20 THEN 1 END)::TEXT
        ) as mid_month_satisfaction,
        -- End of month (days 21-31)
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) > 20 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(DAY FROM review_time) > 20 THEN 1 END)::TEXT
        ) as late_month_satisfaction
    FROM {{ ref('fact_reviews') }}
    GROUP BY review_month
)

SELECT * FROM month_metrics
ORDER BY month_id