-- SELECT * FROM auth.users
--     LIMIT 100;

SELECT * FROM public.argyle_driver_activities
    LIMIT 5000;

SELECT *
FROM user_meta_data;

SELECT raw_user_meta_data ->> 'affiliation' AS affiliation
FROM user_meta_data;

-- SELECT id, account, employer, created_at, updated_at, status, type,
--     all_datetimes_request_at, duration, timezone, earning_type, 
--     start_location_lat, start_location_lng, start_location_formatted_address, 
--     end_location_lat, end_location_lng, end_location_formatted_address, distance, 
--     distance_unit, metadata, circumstances_is_pool, circumstances_is_surge, 
--     circumstances_service_type, circumstances_position, income_currency, 
--     income_total_charge, income_fees, income_total, income_pay, income_tips,
--     income_bonus, metadata_origin_id, end_datetime, start_datetime, task_count, 
--     income_other, user
--     FROM public.argyle_driver_activities
--     WHERE type = 'rideshare'
--     ORDER BY id
--     LIMIT 1000;

-- SELECT DISTINCT user
-- FROM public.argyle_driver_activities;