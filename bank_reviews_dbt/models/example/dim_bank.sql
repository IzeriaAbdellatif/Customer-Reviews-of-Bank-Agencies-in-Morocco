WITH bank_metrics AS (
    SELECT 
        fr.bank_name,
        COUNT(DISTINCT fr.branch_id) as branch_count,
        AVG(fr.branch_rating) as avg_rating,
        SUM(fr.user_rating_count) as total_reviews,
        
        -- Overall satisfaction
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as overall_satisfaction,

        -- Security satisfaction
        CONCAT(
            COUNT(CASE WHEN fr.topic = 'security' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.topic = 'security' AND fr.sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as security_satisfaction,

        -- Customer Service satisfaction
        CONCAT(
            COUNT(CASE WHEN fr.topic = 'customer service' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.topic = 'customer service' AND fr.sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as service_satisfaction,

        -- Digital Banking satisfaction
        CONCAT(
            COUNT(CASE WHEN fr.topic = 'mobile banking' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.topic = 'mobile banking' AND fr.sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as digital_satisfaction,

        -- Wait Times satisfaction
        CONCAT(
            COUNT(CASE WHEN fr.topic = 'wait times' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.topic = 'wait times' AND fr.sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as wait_time_satisfaction

    FROM {{ ref('fact_reviews') }} fr
    GROUP BY fr.bank_name
),

regional_satisfaction AS (
    SELECT 
        bank_name,
        region,
        CONCAT(
            COUNT(CASE WHEN sentiment = 'positive' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN sentiment IS NOT NULL THEN 1 END)::TEXT
        ) as region_satisfaction,
        COUNT(DISTINCT branch_id) as region_branches,
        COUNT(*) as region_reviews
    FROM {{ ref('fact_reviews') }}
    GROUP BY bank_name, region
),

regional_stats AS (
    SELECT 
        bank_name,
        JSON_AGG(
            JSON_BUILD_OBJECT(
                'region', region,
                'satisfaction_ratio', region_satisfaction,
                'branches', region_branches,
                'reviews', region_reviews
            )
        ) as regional_performance
    FROM regional_satisfaction
    GROUP BY bank_name
)

SELECT 
    bm.*,
    rs.regional_performance,
    -- Best performing region
    (SELECT region 
     FROM regional_satisfaction rs2 
     WHERE rs2.bank_name = bm.bank_name 
     ORDER BY rs2.region_satisfaction DESC 
     LIMIT 1) as best_performing_region,
    -- Worst performing region
    (SELECT region 
     FROM regional_satisfaction rs2 
     WHERE rs2.bank_name = bm.bank_name 
     ORDER BY rs2.region_satisfaction ASC 
     LIMIT 1) as worst_performing_region
FROM bank_metrics bm
LEFT JOIN regional_stats rs ON rs.bank_name = bm.bank_name
ORDER BY overall_satisfaction DESC