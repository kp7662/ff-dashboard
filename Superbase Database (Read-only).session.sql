-- SELECT * FROM auth.users
--     LIMIT 100;

-- SELECT * FROM public.argyle_driver_activities
--     LIMIT 100;

SELECT id, start_location_lng, start_location_lat, end_location_lng, end_location_lat,
       income_total_charge, income_other, income_fees, income_pay, income_tips,
       distance, duration, start_location_formatted_address, end_location_formatted_address,
       start_datetime, account, user as user_id
FROM public.argyle_driver_activities
-- WHERE user = 'ffreadonly'
ORDER BY start_datetime DESC
LIMIT 10;

SELECT DISTINCT user
FROM public.argyle_driver_activities;