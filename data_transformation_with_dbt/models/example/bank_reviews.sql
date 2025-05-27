WITH unnested_reviews AS (
    -- First review
    SELECT 
        id as branch_id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,  -- Add this line
        rating as branch_rating,
        user_rating_count,
        person_id_1 as person_id,
        time_1 as review_time,
        review_1 as review_text,
        rating_1 as review_rating,
        review_1_topic as topic,
        review_1_sentiment as sentiment
    FROM {{ source('unique_source','new_bank_branches') }}
    WHERE person_id_1 IS NOT NULL

    UNION ALL

    -- Second review
    SELECT 
        id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,  -- Add this line
        rating,
        user_rating_count,
        person_id_2,
        time_2,
        review_2,
        rating_2,
        review_2_topic,
        review_2_sentiment
    FROM {{ source('unique_source','new_bank_branches') }}
    WHERE person_id_2 IS NOT NULL

    UNION ALL

    -- Third review
    SELECT 
        id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,  -- Add this line
        rating,
        user_rating_count,
        person_id_3,
        time_3,
        review_3,
        rating_3,
        review_3_topic,
        review_3_sentiment
    FROM {{ source('unique_source','new_bank_branches') }}
    WHERE person_id_3 IS NOT NULL

    UNION ALL

    -- Fourth review
    SELECT 
        id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,  -- Add this line
        rating,
        user_rating_count,
        person_id_4,
        time_4,
        review_4,
        rating_4,
        review_4_topic,
        review_4_sentiment
    FROM {{ source('unique_source','new_bank_branches') }}
    WHERE person_id_4 IS NOT NULL

    UNION ALL

    -- Fifth review
    SELECT 
        id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,  -- Add this line
        rating,
        user_rating_count,
        person_id_5,
        time_5,
        review_5,
        rating_5,
        review_5_topic,
        review_5_sentiment
    FROM {{ source('unique_source','new_bank_branches') }}
    WHERE person_id_5 IS NOT NULL
)

SELECT 
    {{ dbt_utils.generate_surrogate_key(['branch_id', 'person_id', 'review_time']) }} as review_id,
    *,
    EXTRACT(YEAR FROM review_time) as review_year,
    EXTRACT(MONTH FROM review_time) as review_month,
    EXTRACT(DOW FROM review_time) as review_day_of_week,
    CASE 
        WHEN review_rating >= 4 THEN 'High'
        WHEN review_rating = 3 THEN 'Medium'
        ELSE 'Low'
    END as satisfaction_level,
    ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY review_time) as review_sequence_per_user
FROM unnested_reviews
ORDER BY review_time DESC