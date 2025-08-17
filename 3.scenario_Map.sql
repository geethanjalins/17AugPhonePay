select * from mapinall;
-- top performing areas
SELECT
    mi."States",
    mi."Yr",
    mi."Quater",
    mi."Type",
    
    
    -- Aggregated Insurance metrics
    SUM(mi."Count") AS total_insurance_count,
    SUM(mi."Amount") AS total_insurance_amount,

    -- Aggregated Transaction metrics
    SUM(mt."Count") AS total_transaction_count,
    SUM(mt."Amount") AS total_transaction_amount,

    -- Aggregated User metrics
    SUM(mu."Registered_users") AS total_registered_users,
    SUM(mu."App_opens") AS total_app_opens,

    -- Adoption rate metric
    ROUND(
        (SUM(mi."Count")::NUMERIC / NULLIF(SUM(mu."Registered_users"), 0)) * 100,
        2
    ) AS insurance_uptake_percentage

FROM mapinall mi
LEFT JOIN maptn mt
    ON mi."States" = mt."States"
    AND mi."Yr"::text = mt."Yr"::text
    AND mi."Quater" = mt."Quater"
   

LEFT JOIN mapuser mu
    ON mi."States" = mu."States"
    AND mi."Yr" = mu."Yr"
    AND mi."Quater" = mu."Quarter"
    AND mt."District" = mu."District"

GROUP BY
    mi."States",
    mi."Yr",
    mi."Quater",
    mi."Type",
	mt."District"
    

ORDER BY
    total_transaction_count DESC,
    total_transaction_amount DESC
LIMIT 20;
