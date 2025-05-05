WITH regions_list AS (
    SELECT DISTINCT region 
    FROM {{ ref('fact_reviews') }}
    WHERE region IS NOT NULL
),
regional_topic_metrics AS (
    SELECT 
        fr.topic,
        fr.region,
        COUNT(CASE WHEN fr.sentiment = 'positive' THEN 1 END)::TEXT || '/' || 
        COUNT(CASE WHEN fr.topic IS NOT NULL THEN 1 END)::TEXT as region_score
    FROM {{ ref('fact_reviews') }} fr
    WHERE fr.topic IS NOT NULL
    GROUP BY fr.topic, fr.region
),
topic_metrics AS (
    SELECT 
        fr.topic,
        -- Bank scores per topic
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANK OF AFRICA' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANK OF AFRICA' THEN 1 END)::TEXT
        ) as BOA_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'Al Barid Bank' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'Al Barid Bank' THEN 1 END)::TEXT
        ) as ABB_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'ATTIJARIWAFA BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'ATTIJARIWAFA BANK' THEN 1 END)::TEXT
        ) as ATTIJARI_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'SOCIETE GENERALE' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'SOCIETE GENERALE' THEN 1 END)::TEXT
        ) as SG_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'ARAB BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'ARAB BANK' THEN 1 END)::TEXT
        ) as AB_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'UMNIA BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'UMNIA BANK' THEN 1 END)::TEXT
        ) as UMNIA_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BMCI' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BMCI' THEN 1 END)::TEXT
        ) as BMCI_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'credit agricole' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'credit agricole' THEN 1 END)::TEXT
        ) as CA_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'CFG BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'CFG BANK' THEN 1 END)::TEXT
        ) as CFG_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'CIH BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'CIH BANK' THEN 1 END)::TEXT
        ) as CIH_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'AL AKHDAR BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'AL AKHDAR BANK' THEN 1 END)::TEXT
        ) as AAB_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'CREDIT DU MAROC' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'CREDIT DU MAROC' THEN 1 END)::TEXT
        ) as CDM_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANK AL YOUSR' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANK AL YOUSR' THEN 1 END)::TEXT
        ) as BAY_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANQUE POPULAIRE' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANQUE POPULAIRE' THEN 1 END)::TEXT
        ) as BP_score,
        -- Dynamic regional performance calculation
        (SELECT JSON_OBJECT_AGG(
            r.region,
            COALESCE(rtm.region_score, '0/0')
         )
         FROM regions_list r
         LEFT JOIN regional_topic_metrics rtm 
         ON rtm.region = r.region 
         AND rtm.topic = fr.topic
        ) as region_performance
    FROM {{ ref('fact_reviews') }} fr
    WHERE fr.topic IS NOT NULL
    GROUP BY fr.topic
),
-- Extract best and worst regions based on performance
region_rankings AS (
    SELECT 
        topic,
        (SELECT key 
         FROM JSON_EACH_TEXT(region_performance) 
         WHERE value IS NOT NULL AND value <> 'null' AND value ~ '^[0-9]+/[0-9]+$'
         ORDER BY (
             CAST(SPLIT_PART(value, '/', 1) AS FLOAT) / 
             GREATEST(CAST(SPLIT_PART(value, '/', 2) AS FLOAT), 1)
         ) DESC 
         LIMIT 1) as best_region,
        (SELECT key 
         FROM JSON_EACH_TEXT(region_performance) 
         WHERE value IS NOT NULL AND value <> 'null' AND value ~ '^[0-9]+/[0-9]+$'
         ORDER BY (
             CAST(SPLIT_PART(value, '/', 1) AS FLOAT) / 
             GREATEST(CAST(SPLIT_PART(value, '/', 2) AS FLOAT), 1)
         ) ASC 
         LIMIT 1) as worst_region
    FROM topic_metrics
)

SELECT 
    tm.topic as topic_id,
    tm.BOA_score,
    tm.ABB_score,
    tm.ATTIJARI_score,
    tm.SG_score,
    tm.AB_score,
    tm.UMNIA_score,
    tm.BMCI_score,
    tm.CA_score,
    tm.CFG_score,
    tm.CIH_score,
    tm.AAB_score,
    tm.CDM_score,
    tm.BAY_score,
    tm.BP_score,
    tm.region_performance,
    rr.best_region,
    rr.worst_region
FROM topic_metrics tm
JOIN region_rankings rr ON tm.topic = rr.topic