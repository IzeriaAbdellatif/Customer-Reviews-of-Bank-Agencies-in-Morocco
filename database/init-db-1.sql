create table banks
(
    id                text primary key,
    name              text,
    branch            text,
    location          text,
    rating            text,
    user_rating_count text
);

create table reviews
(
    id                        text primary key,
    bank_id                   text,
    author                    text,
    rating                    text,
    review_date               text,
    original_review_content   text,
    review_content_language   text,
    translated_review_content text
)