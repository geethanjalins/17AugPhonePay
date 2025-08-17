select * from agin;
select * from agtn;
select * from aguser;
--deeper understanding of patterns across states, quarters, and payment categories, 
--design an analysis that combines transaction trends with user engagement metrics.
--A. Quarterly Transaction Trends by State & Type

SELECT
    "State",
    "Year",
    "Quater",
    "Transacion_type",
    SUM("Transacion_count") AS total_transactions,
    SUM("Transacion_amount") AS total_amount
FROM agin
GROUP BY "State", "Year", "Quater", "Transacion_type"
ORDER BY "State", "Year", "Quater", total_transactions DESC;

--B. Growth Rate Analysis (Quarter-over-Quarter)

WITH ranked_data AS (
    SELECT
        "State",
        "Transacion_type",
        "Year",
        "Quater",
        SUM("Transacion_count") AS total_transactions,
        SUM("Transacion_amount") AS total_amount,
        LAG(SUM("Transacion_count")) OVER (
            PARTITION BY "State", "Transacion_type"
            ORDER BY "Year", "Quater"
        ) AS prev_transactions
    FROM agin
    GROUP BY "State", "Transacion_type","Year", "Quater"
)
SELECT
    "State",
    "Transacion_type",
    "Year",
    "Quater",
    total_transactions,
    prev_transactions,
    (((total_transactions - prev_transactions) / NULLIF(prev_transactions, 0)) * 100, 2) AS growth_rate_pct
FROM ranked_data
ORDER BY growth_rate_pct DESC;


--C. User Engagement Efficiency

SELECT
    "States",
    "Yr",
    "Quater",
    SUM("Registered_users") AS total_users,
    SUM("App_opens") AS total_opens,
    (SUM("App_opens") * 1.0 / NULLIF(SUM("Registered_users"), 0), 2) AS opens_per_user
FROM aguser
GROUP BY "States", "Yr", "Quater"
ORDER BY opens_per_user DESC;
