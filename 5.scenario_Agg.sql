-- Replace :year_param and :quarter_param with the desired year and quarter values
SELECT
    i."State",
    i."Year",
    i."Quater",
    i."Transacion_type",

    -- Insurance transactions
    SUM(i."Transacion_count") AS total_transactions,
    SUM(i."Transacion_amount") AS total_amount,

    -- User metrics from user table
    SUM(COALESCE(u."Registered_users", 0)) AS total_users,
    SUM(COALESCE(u."App_opens", 0)) AS total_opens,

    -- Engagement: app opens per user
    ROUND(SUM(COALESCE(u."App_opens", 0))::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS opens_per_user,

    -- Value per user (insurance-focused)
    ROUND(SUM(i."Transacion_amount")::numeric /
          NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2) AS value_per_user

FROM agin i  -- insurance table
LEFT JOIN aguser u
    ON i."State" = u."States"
    AND i."Year" = u."Yr"
    AND i."Quater" = u."Quater"

WHERE i."Year" = '2018'
i."Quater" = 4

GROUP BY
    i."State",
    i."Year",
    i."Quater",
    i."Transacion_type"

ORDER BY
    total_transactions DESC,
    total_amount DESC
LIMIT 100;
