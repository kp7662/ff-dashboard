# backend/app/utils.py

# Standard library imports
from datetime import datetime, timedelta
from io import StringIO
import logging
import time

# Third-party imports
import numpy as np
import pandas as pd
from flask_caching import Cache
from sqlalchemy import text

# Local application imports
from app import app, db, cache, logger

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------

def get_rideshare_data_by_period(period='7d'):
    """
    Fetches rideshare data for a specified period from cache or database, preprocesses, and returns it as a DataFrame.

    If the data is found in cache, it is loaded and deserialized. If not found, the data is queried from the database
    based on the given period ('7d', '1m', '3m', '6m', '1y'), where 'd' stands for days and 'm' for months. The query
    retrieves various details related to rideshare activities within the specified period. Before returning, this
    function preprocesses the data by replacing zeros or Nones in 'distance' with NaN, calculating the total charge,
    adjusting the current pay by excluding tips, and computing pay per mile. The preprocessed data is then cached for
    future requests.

    Parameters:
    - period (str): The period for which to retrieve rideshare data. Default is '7d'. Accepted values are '7d', '1m',
    '3m', '6m', '1y'.

    Returns:
    - DataFrame: A pandas DataFrame containing the processed rideshare data for the requested period.
    """
    cache_key = f'rideshare_data_{period}'
    
    # Start measuring time
    start_time = time.time()

    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        # Cache hit, calculate time taken to retrieve from cache
        cache_duration = time.time() - start_time
        logger.info(f"Cache hit for {cache_key}. Loaded data from cache in {cache_duration:.2f} seconds.")
        
        # Deserialize and return the DataFrame
        return pd.read_json(StringIO(cached_data), orient='split')
    
    # If cache miss, log it and proceed to query the database
    logger.info(f"Cache miss for {cache_key}. Querying database...")
    # Reset start time for measuring database query duration
    db_start_time = time.time()

    # Calculate the start date based on the period
    end_date = datetime.now()
    if period == '7d':
        start_date = end_date - timedelta(days=7)
    elif period == '1m':
        start_date = end_date - timedelta(days=30)
    elif period == '3m':
        start_date = end_date - timedelta(days=91)
    elif period == '6m':
        start_date = end_date - timedelta(days=182)
    elif period == '1y':
        start_date = end_date - timedelta(days=365)
    else:
        # Default to 7 days if period is not recognized
        start_date = end_date - timedelta(days=7)
    
    query = """
    SELECT id, account, employer, created_at, updated_at, status, type,
    all_datetimes_request_at, duration, timezone, earning_type, 
    start_location_lat, start_location_lng, start_location_formatted_address, 
    end_location_lat, end_location_lng, end_location_formatted_address, distance, 
    distance_unit, metadata, circumstances_is_pool, circumstances_is_surge, 
    circumstances_service_type, circumstances_position, income_currency, 
    income_total_charge, income_fees, income_total, income_pay, income_tips,
    income_bonus, metadata_origin_id, end_datetime, start_datetime, task_count, 
    income_other, user
    FROM public.argyle_driver_activities
    WHERE type = 'rideshare' AND
    start_datetime::timestamp >= :start_date AND
    start_datetime::timestamp <= :end_date
    ORDER BY id;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query), {'start_date': start_date, 'end_date': end_date})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Calculate and log time taken for database operations
    db_duration = time.time() - db_start_time
    logger.info(f"Loaded data from database in {db_duration:.2f} seconds.")

    # Preprocess the data

    # Replace 0 or None in 'distance' with NaN (if needed)
    df['distance'] = df['distance'].replace(0, np.nan).fillna(np.nan)

    df['income_total_charge'] = df['income_fees'] + df['income_total']
    df['current_pay'] = df['income_pay'] + df['income_bonus']  # Exclude tips from current pay
    df['pay_per_mile'] = np.where(df['distance'] != 0, df['current_pay'] / df['distance'], np.nan)

    # Cache the processed DataFrame
    cache.set(cache_key, df.to_json(orient='split'), timeout=3600) # Can adjust TTL later

    return df

# --------------------------------------------------------------------------------

def get_rideshare_avg_trip_duration():
    """
    Retrieves the average trip duration of rideshare activities from cache or, if not available, computes it from
    database records. This value is then cached for future requests.

    Initially, the function checks for the average trip duration in the cache. If found, it logs the retrieval time
    and returns the cached value. If the average trip duration is not in the cache (cache miss), the function queries
    the database for all rideshare trip durations, computes the average, logs the time taken for database operations
    and the overall operation time, including caching. The computed average trip duration is then cached with a set
    timeout and returned.

    Returns:
    - float: The average trip duration for rideshare activities.
    """
    cache_key = 'avg_trip_duration'
    start_time = time.time()

    cached_avg_duration = cache.get(cache_key)
    
    if cached_avg_duration is not None:
        duration = time.time() - start_time  # Calculate the duration of cache retrieval
        logger.info(f"Cache hit for {cache_key}. Retrieved in {duration:.4f} seconds.")
        return cached_avg_duration
    
    # If not found in cache, proceed with database query
    logger.info(f"Cache miss for {cache_key}. Querying database...")
    start_db_time = time.time()
    query = """
    SELECT duration 
    FROM public.argyle_driver_activities
    WHERE type = 'rideshare'
    ORDER BY id
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    average_trip_duration = df['duration'].mean()
    db_duration = time.time() - start_db_time  # Calculate the duration of database operation
    logger.info(f"Loaded data from database and computed average in {db_duration:.4f} seconds.")

    # Cache the computed average for future requests
    cache.set(cache_key, average_trip_duration, timeout=3600)  # Cache for 1 hour
    
    total_duration = time.time() - start_time  # Total operation time including caching
    logger.info(f"Total operation time including caching: {total_duration:.4f} seconds.")
    
    return average_trip_duration

# --------------------------------------------------------------------------------

def get_rideshare_monthly_pay():
    """
    Retrieves rideshare monthly pay data, either from cache or by querying the database, then returns it as a DataFrame.
    
    This function first attempts to retrieve the data from cache. If successful (cache hit), it logs the retrieval time,
    deserializes the JSON string to a DataFrame, and returns it. If the data is not in the cache (cache miss), it logs
    this event, executes a database query to fetch rideshare payment data (limited to the first 2000 records for
    performance reasons), and preprocesses the data by calculating total charges and current pay excluding tips.
    
    After preprocessing, the DataFrame is converted to a JSON string and cached for future requests with a set timeout.
    The function logs the duration it takes to load data from the database and cache it. Finally, it returns the
    DataFrame containing the preprocessed rideshare monthly pay data.
    
    Returns:
    - DataFrame: A pandas DataFrame containing rideshare monthly pay data, including total charges and current pay,
    preprocessed for further analysis.
    """
    cache_key = 'get_rideshare_monthly_pay'
    start_time = time.time()  # Start timing

    cached_data = cache.get(cache_key)
    
    if cached_data:
        # If there's a cache hit, log it and load the DataFrame from the cached JSON
        # Use StringIO to wrap the JSON string
        df = pd.read_json(StringIO(cached_data), orient='split')
        duration = time.time() - start_time  # Calculate the duration
        logger.info(f"Cache hit for {cache_key}. Loaded data from cache in {duration:.2f} seconds.")
    else:
        # If there's a cache miss, log it, query the database, and cache the result
        logger.info(f"Cache miss for {cache_key}. Querying database...")
        
        # Database query to retrieve rideshare data
        query = """
        SELECT id, start_datetime, income_fees, income_total, income_pay, income_bonus
        FROM public.argyle_driver_activities
        WHERE type = 'rideshare'
        ORDER BY id
        LIMIT 2000;
        """
        with db.engine.connect() as conn:
            result = conn.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        # Preprocess the data
        df['income_total_charge'] = df['income_fees'] + df['income_total']
        df['current_pay'] = df['income_pay'] + df['income_bonus']  # Exclude tips from current pay
        
        # Convert DataFrame to JSON and cache it
        processed_data = df.to_json(orient='split')
        cache.set(cache_key, processed_data, timeout=3600)  # Cache for 1 hour
        
        duration = time.time() - start_time  # Calculate the duration
        logger.info(f"Loaded rideshare monthly pay data from database and cached it in {duration:.2f} seconds.")
    
    return df  # Return the DataFrame, not the JSON string

# --------------------------------------------------------------------------------

def get_rideshare_pay_breakdown_df():
    # Database query to retrieve rideshare data
    query = """
    SELECT id, income_fees, income_pay, income_tips, income_bonus
    FROM public.argyle_driver_activities
    WHERE type = 'rideshare'
    ORDER BY id
    LIMIT 10000;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
        # Convert columns to float
    for column in ['income_fees', 'income_pay', 'income_tips', 'income_bonus']:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)

    return df

def get_delivery_pay_breakdown_df():
    # Database query to retrieve delivery data
    query = """
    SELECT id, income_fees, income_pay, income_tips, income_bonus
    FROM public.argyle_driver_activities
    WHERE type = 'delivery'
    ORDER BY id
    LIMIT 10000;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Convert columns to float
    for column in ['income_fees', 'income_pay', 'income_tips', 'income_bonus']:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype(float)

    return df