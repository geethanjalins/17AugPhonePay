select * from mapinall;
select * from maptn;
select * from mapuser;
-- significant number of registered user and app to understand user behavior
SELECT 
    COALESCE(i."States", t."States", u."States") AS States,
    COALESCE(i."Yr"::text, t."Yr"::text, u."Yr"::text) AS Years,
    COALESCE(i."Quater", t."Quater", u."Quarter") AS Quater,
    COALESCE( t."District",u."District") AS District,
    COALESCE(i."Metric",t."Metric_Type") AS Metric_type,

    -- Transaction metrics
    SUM(COALESCE(i."Count", 0) + COALESCE(t."Count", 0)) AS total_transactions,
    SUM(COALESCE(i."Amount", 0) + COALESCE(t."Amount", 0)) AS total_amount,

    -- User metrics
    SUM(COALESCE(u."Registered_users", 0)) AS total_registered_users,
    SUM(COALESCE(u."App_opens", 0)) AS total_app_opens,

    -- Engagement ratios
    ROUND(
        SUM(COALESCE(u."App_opens", 0))::NUMERIC /
        NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2
    ) AS opens_per_user,

    ROUND(
        SUM(COALESCE(i."Amount", 0) + COALESCE(t."Amount", 0))::NUMERIC /
        NULLIF(SUM(COALESCE(u."Registered_users", 0)), 0), 2
    ) AS value_per_user

FROM mapinall i
FULL JOIN maptn t
    ON i."States" = t."States"
    AND i."Yr"::text = t."Yr"::text
    AND i."Quater" = t."Quater"

FULL JOIN mapuser u
    ON COALESCE(i."States", t."States") = u."States"
AND COALESCE(t."District") = u."District"
AND COALESCE(i."Yr"::text, t."Yr"::text) = u."Yr"::text
AND COALESCE(i."Quater"::text, t."Quater"::text) = u."Quarter"::text

GROUP BY 
    COALESCE(i."States", t."States", u."States"),
    COALESCE(i."Yr"::text, t."Yr"::text, u."Yr"::text),
    COALESCE(i."Quater", t."Quater", u."Quarter"),
    COALESCE(t."District", u."District"),
    COALESCE(i."Metric", t."Metric_Type")

ORDER BY total_transactions DESC, total_amount DESC
LIMIT 50;
