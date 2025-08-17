--SQL Query – Engagement & Value Analysis by State/District
SELECT
    COALESCE(t."State", i."State", u."States") AS States,
    COALESCE(t."Year", i."Year", u."Yr") AS Years,
    COALESCE(t."Quater", i."Quater", u."Quater") AS Quater,
    COALESCE(t."Transacion_type", i."Transacion_type") AS Transaction_type,

    -- Total transactions (insurance + non-insurance)
    SUM(COALESCE(t."Transacion_count", 0) + COALESCE(i."Transacion_count", 0)) AS total_transactions,
    SUM(COALESCE(t."Transacion_amount", 0) + COALESCE(i."Transacion_amount", 0)) AS total_amount,

    -- User metrics
    SUM(COALESCE(u."Registered_users", 0)) AS total_users,
    SUM(COALESCE(u."App_opens", 0)) AS total_opens,

    -- Engagement: app opens per user
    ROUND(SUM(COALESCE(u."App_opens", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS opens_per_user,

    -- Value per user
    ROUND(SUM(COALESCE(t."Transacion_amount", 0) + COALESCE(i."Transacion_amount", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS value_per_user,

    -- Transactions per user
    ROUND(SUM(COALESCE(t."Transacion_count", 0) + COALESCE(i."Transacion_count", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS transactions_per_user

FROM agtn t  -- transaction table
FULL JOIN agin i  -- insurance table
    ON t."State" = i."State"
    AND t."Year" = i."Year"
    AND t."Quater" = i."Quater"
    AND t."Transacion_type" = i."Transacion_type"
FULL JOIN aguser u  -- user table
    ON COALESCE(t."State", i."State") = u."States"
    AND COALESCE(t."Year", i."Year") = u."Yr"
    AND COALESCE(t."Quater", i."Quater") = u."Quater"

GROUP BY
    COALESCE(t."State", i."State", u."States"),
    COALESCE(t."Year", i."Year", u."Yr"),
    COALESCE(t."Quater", i."Quater", u."Quater"),
    COALESCE(t."Transacion_type", i."Transacion_type")

ORDER BY
    opens_per_user DESC,
    value_per_user DESC;
