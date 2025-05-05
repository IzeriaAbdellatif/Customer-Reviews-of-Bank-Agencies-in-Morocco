WITH region_metrics AS (
    SELECT 
        fr.region,
        -- Bank scores
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANK OF AFRICA' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANK OF AFRICA' THEN 1 END)::TEXT
        ) as BANK_OF_AFRICA_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'Al Barid Bank' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'Al Barid Bank' THEN 1 END)::TEXT
        ) as BARID_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'ATTIJARIWAFA BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'ATTIJARIWAFA BANK' THEN 1 END)::TEXT
        ) as ATTIJARI_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'SOCIETE GENERALE' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'SOCIETE GENERALE' THEN 1 END)::TEXT
        ) as SOCIETE_GENERAL_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'ARAB BANK' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'ARAB BANK' THEN 1 END)::TEXT
        ) as ARAB_BANK_score,
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
        ) as CREDIT_AGRICOLE_score,
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
        ) as AL_AKHDAR_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'CREDIT DU MAROC' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'CREDIT DU MAROC' THEN 1 END)::TEXT
        ) as CREDIT_DU_MAROC_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANK AL YOUSR' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANK AL YOUSR' THEN 1 END)::TEXT
        ) as AL_YOUSR_score,
        CONCAT(
            COUNT(CASE WHEN fr.sentiment = 'positive' AND fr.bank_name = 'BANQUE POPULAIRE' THEN 1 END)::TEXT, '/',
            COUNT(CASE WHEN fr.bank_name = 'BANQUE POPULAIRE' THEN 1 END)::TEXT
        ) as BANK_POPULAIRE_score,
        -- Modified topic performance calculation with string format x/y
        JSON_BUILD_OBJECT(
            'billing', CONCAT(
                COUNT(CASE WHEN fr.topic = 'billing' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'billing' THEN 1 END)::TEXT),
            'customer_service', CONCAT(
                COUNT(CASE WHEN fr.topic = 'customer service' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'customer service' THEN 1 END)::TEXT),
            'security', CONCAT(
                COUNT(CASE WHEN fr.topic = 'security' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'security' THEN 1 END)::TEXT),
            'atm', CONCAT(
                COUNT(CASE WHEN fr.topic = 'ATM issues' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'ATM issues' THEN 1 END)::TEXT),
            'wait_time', CONCAT(
                COUNT(CASE WHEN fr.topic = 'wait times' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'wait times' THEN 1 END)::TEXT),
            'staff', CONCAT(
                COUNT(CASE WHEN fr.topic = 'staff behavior' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'staff behavior' THEN 1 END)::TEXT),
            'mobile_banking', CONCAT(
                COUNT(CASE WHEN fr.topic = 'mobile banking' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'mobile banking' THEN 1 END)::TEXT),
            'account_management', CONCAT(
                COUNT(CASE WHEN fr.topic = 'account management' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'account management' THEN 1 END)::TEXT),
            'loans', CONCAT(
                COUNT(CASE WHEN fr.topic = 'loans' AND fr.sentiment = 'positive' THEN 1 END)::TEXT, '/',
                COUNT(CASE WHEN fr.topic = 'loans' THEN 1 END)::TEXT)
        ) as topic_performance
    FROM {{ ref('fact_reviews') }} fr
    GROUP BY fr.region
),
-- Extracting best and worst topics based on performance
topic_rankings AS (
    SELECT 
        region,
        (SELECT key 
         FROM JSON_EACH_TEXT(topic_performance) 
         WHERE value IS NOT NULL AND value <> 'null' AND value ~ '^[0-9]+/[0-9]+$'
         ORDER BY (
             CAST(SPLIT_PART(value, '/', 1) AS FLOAT) / 
             GREATEST(CAST(SPLIT_PART(value, '/', 2) AS FLOAT), 1)
         ) DESC 
         LIMIT 1) as best_topic,
        (SELECT key 
         FROM JSON_EACH_TEXT(topic_performance) 
         WHERE value IS NOT NULL AND value <> 'null' AND value ~ '^[0-9]+/[0-9]+$'
         ORDER BY (
             CAST(SPLIT_PART(value, '/', 1) AS FLOAT) / 
             GREATEST(CAST(SPLIT_PART(value, '/', 2) AS FLOAT), 1)
         ) ASC 
         LIMIT 1) as worst_topic
    FROM region_metrics
)

SELECT 
    lm.region as region_id,
    lm.BANK_OF_AFRICA_score,
    lm.BARID_score,
    lm.ATTIJARI_score,
    lm.SOCIETE_GENERAL_score,
    lm.ARAB_BANK_score,
    lm.UMNIA_score,
    lm.BMCI_score,
    lm.CREDIT_AGRICOLE_score,
    lm.CFG_score,
    lm.CIH_score,
    lm.AL_AKHDAR_score,
    lm.CREDIT_DU_MAROC_score,
    lm.AL_YOUSR_score,
    lm.BANK_POPULAIRE_score,
    lm.topic_performance,
    tr.best_topic,
    tr.worst_topic
    
FROM region_metrics lm
JOIN topic_rankings tr ON lm.region = tr.region