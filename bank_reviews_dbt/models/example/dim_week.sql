WITH day_metrics AS (
    SELECT 
        review_day_of_week as day_id,
        CASE review_day_of_week
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END as day_name,
        -- Overall satisfaction per day
        CONCAT(
            COUNT(CASE WHEN sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(*)::TEXT
        ) as overall_satisfaction,
        -- Satisfaction by time slots
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 5 
                AND EXTRACT(HOUR FROM review_time) < 8 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 5 
                AND EXTRACT(HOUR FROM review_time) < 8 THEN 1 END)::TEXT
        ) as early_morning_satisfaction,
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 8 
                AND EXTRACT(HOUR FROM review_time) < 12 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 8 
                AND EXTRACT(HOUR FROM review_time) < 12 THEN 1 END)::TEXT
        ) as morning_satisfaction,
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 12 
                AND EXTRACT(HOUR FROM review_time) < 17 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 12 
                AND EXTRACT(HOUR FROM review_time) < 17 THEN 1 END)::TEXT
        ) as afternoon_satisfaction,
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 17 
                AND EXTRACT(HOUR FROM review_time) < 21 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 17 
                AND EXTRACT(HOUR FROM review_time) < 21 THEN 1 END)::TEXT
        ) as evening_satisfaction,
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 21 
                AND EXTRACT(HOUR FROM review_time) < 24 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 21 
                AND EXTRACT(HOUR FROM review_time) < 24 THEN 1 END)::TEXT
        ) as night_satisfaction,
        CONCAT(
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 0 
                AND EXTRACT(HOUR FROM review_time) < 5 
                AND sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE 
                WHEN EXTRACT(HOUR FROM review_time) >= 0 
                AND EXTRACT(HOUR FROM review_time) < 5 THEN 1 END)::TEXT
        ) as late_night_satisfaction
    FROM {{ ref('fact_reviews') }}
    GROUP BY review_day_of_week
)

SELECT * FROM day_metrics
ORDER BY day_id