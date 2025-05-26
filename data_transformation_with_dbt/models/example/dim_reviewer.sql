WITH reviewer_metrics AS (
    SELECT DISTINCT
        person_id,
        COUNT(review_id) as total_reviews,
        AVG(review_rating) as avg_rating,
        MIN(review_time) as first_review_date,
        MAX(review_time) as last_review_date
    FROM {{ ref('bank_reviews') }}
    GROUP BY person_id
)

SELECT * FROM reviewer_metrics
