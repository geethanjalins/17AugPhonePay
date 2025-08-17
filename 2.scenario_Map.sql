select * from mapinall;
select * from maptn;
select * from mapuser;
--analyze insurance uptake across states and districts along with user engagement metrics
SELECT
    mi."States",
    mi."Yr",
    mi."Quater",
    mi."Type" ,
    mt."District",

    -- Insurance metrics
   SUM(mi."Count") AS total_insurance_count,
   SUM(mi."Amount") AS total_insurance_amount,

    -- Transaction metrics
    SUM(mt."Count") AS total_transaction_count,
    SUM(mt."Amount") AS total_transaction_amount,

    -- User metrics
    SUM(mu."Registered_users") AS total_registered_users,
    SUM(mu."App_opens") AS total_app_opens

FROM mapinall mi
LEFT JOIN maptn mt
    ON mi."States" = mt."States"
    AND mi."Yr"::text = mt."Yr"::text
    AND mi."Quater" = mt."Quater"
   

LEFT JOIN mapuser mu
    ON mt."States" = mu."States"
    AND mt."Yr"::text = mu."Yr"::text
    AND mt."Quater" = mu."Quarter"
    AND mt."District" = mu."District"

GROUP BY
    mi."States",
    mi."Yr",
    mi."Quater",
    mi."Type",
    mt."District"

ORDER BY
    total_insurance_count DESC,
    total_insurance_amount DESC;
