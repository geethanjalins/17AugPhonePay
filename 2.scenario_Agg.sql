select * from aguser;
-- device usage vary significantly across regions
SELECT
    COALESCE(t."State", i."State", u."States") AS State,
    COALESCE(t."Year", i."Year", u."Yr") AS Year,
    COALESCE(t."Quater", i."Quater", u."Quater") AS Quater,
    COALESCE(t."Transacion_type", i."Transacion_type") AS Transaction_type,
    

    -- Total transactions from both general transactions & insurance
    SUM(COALESCE(t."Transacion_count", 0) + COALESCE(i."Transacion_count", 0)) AS total_transactions,
    SUM(COALESCE(t."Transacion_amount", 0) + COALESCE(i."Transacion_amount", 0)) AS total_amount,

    -- User engagement data
    SUM(COALESCE(u."Registered_users", 0)) AS total_users,
    SUM(COALESCE(u."App_opens", 0)) AS total_opens,

    -- Engagement ratio: app opens per user
    ROUND(SUM(COALESCE(u."App_opens", 0))::numeric / NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS opens_per_user,

    -- Value per user
    ROUND(SUM(COALESCE(t."Transacion_amount", 0) + COALESCE(i."Transacion_amount", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS value_per_user,

    -- Transactions per user
    ROUND(SUM(COALESCE(t."Transacion_count", 0) + COALESCE(i."Transacion_count", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS transactions_per_user

FROM agtn t
FULL JOIN agin i
    ON t."State" = i."State" AND t."Year" = i."Year" AND t."Quater" = i."Quater"
    AND t."Transacion_type" = i."Transacion_type"

FULL JOIN aguser u
    ON COALESCE(t."State", i."State") = u."States"
    AND COALESCE(t."Year", i."Year") = u."Yr"
    AND COALESCE(t."Quater", i."Quater") = u."Quater"

GROUP BY
    COALESCE(t."State", i."State", u."States"),
    COALESCE(t."Year", i."Year", u."Yr"),
    COALESCE(t."Quater", i."Quater", u."Quater"),
    COALESCE(t."Transacion_type", i."Transacion_type")

ORDER BY total_users DESC, opens_per_user DESC;
