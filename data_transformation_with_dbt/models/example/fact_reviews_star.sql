SELECT
    review_id,
    branch_id,
    person_id,
    review_time::date as date_id,
    review_text,
    review_rating,
    topic,
    sentiment,
    satisfaction_level,
    review_sequence_per_user
FROM {{ ref('bank_reviews') }}