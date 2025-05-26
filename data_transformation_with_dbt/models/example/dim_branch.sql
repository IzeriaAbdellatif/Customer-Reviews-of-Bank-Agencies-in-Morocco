WITH branch_metrics AS (
    SELECT DISTINCT
        branch_id,
        branch_name,
        primary_type,
        bank_name,
        region,
        address,
        branch_rating,
        user_rating_count
    FROM {{ ref('bank_reviews') }}
)

SELECT * FROM branch_metrics