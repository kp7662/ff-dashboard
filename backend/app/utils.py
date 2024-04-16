# backend/app/utils.py

# Standard library imports
from datetime import datetime, timedelta
from io import StringIO, BytesIO
from sqlalchemy import create_engine, text
from plotnine import (element_text, ggtitle, aes, ggplot, scale_x_discrete, geom_violin,
                      geom_point, geom_boxplot, scale_fill_manual, scale_y_continuous, theme, theme_classic,
                      position_jitter, labs, ylim, ggsave)
from mizani.formatters import percent_format
from redis.exceptions import RedisError
import logging
import time
import pickle

# Third-party imports
import numpy as np
import pandas as pd
from sqlalchemy import text

# Local application imports
from app import app, db, cache, logger
# --------------------------------------------------------------------------------

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------
def get_rideshare_data(date_filter='3m', start_date=None, end_date=None, affiliation=None):
    """
    Fetches and returns rideshare data as a DataFrame, based on either a predefined period
    or specific start and end dates provided by the user.

    Parameters:
    - date_filter (str): A predefined period for data retrieval ('7d', '1m', '3m', '6m', '1y').
    - start_date (str or None): The start date for data filtering in 'YYYY-MM-DD' format.
    - end_date (str or None): The end date for data filtering in 'YYYY-MM-DD' format.
    - affiliation (str or None): The affiliation to filter the data.

    Returns:
    - DataFrame: Processed rideshare data for the requested period or date range.
    """

    if start_date and end_date:
        cache_key = f'rideshare_data_custom_{start_date}_{end_date}_{affiliation}'
    else:
        cache_key = f'rideshare_data_{date_filter}_{affiliation}'

    # Start measuring time
    # start_time = time.time()
    
    try:
        # Try to fetch from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            # cache_duration = time.time() - start_time
            # logger.info(f"Cache hit for {cache_key}. Loaded data from cache in {cache_duration:.2f} seconds.")
            return pd.read_json(StringIO(cached_data), orient='split')
    except RedisError as e:
        logger.error(f"Cache miss for {cache_key}: {e}")

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        end_date = datetime.now()
        if date_filter == '7d':
            start_date = end_date - timedelta(days=7)
        elif date_filter == '1m':
            start_date = end_date - timedelta(days=30)
        elif date_filter == '3m':
            start_date = end_date - timedelta(days=91)
        elif date_filter == '6m':
            start_date = end_date - timedelta(days=182)
        elif date_filter == '1y':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=7)  # Default case

    # Reset start time for measuring database query duration
    # db_start_time = time.time()
    
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
    # db_duration = time.time() - db_start_time
    # logger.info(f"Loaded data from database in {db_duration:.2f} seconds.")

    # Preprocess the data

    # Replace 0 or None in 'distance' with NaN (if needed)
    df['distance'] = df['distance'].replace(0, np.nan).fillna(np.nan)

    df['income_total_charge'] = df['income_fees'] + df['income_total']
    df['current_pay'] = df['income_pay'] + df['income_bonus']  # Exclude tips from current pay
    df['pay_per_mile'] = np.where(df['distance'] != 0, df['current_pay'] / df['distance'], np.nan)

    # Fetch and clean affiliations
    df_affiliations = fetch_and_clean_affiliations()

    # Merge the affiliations with the rideshare data
    df = df.merge(df_affiliations, how='left', left_on='account', right_on='argyle_account').drop('argyle_account', axis=1)
    
    # Apply affiliation filter if provided
    if affiliation is not None:
        if affiliation == 'CIDU':
            df = df[df['affiliation'] == 'colorado_independent_drivers_united']
        elif affiliation == 'RDU':
            df = df[df['affiliation'] == 'rideshare_drivers_united']
        elif affiliation == 'DU':
            df = df[df['affiliation'] == 'drivers_union']
        elif affiliation == 'CDU':
            df = df[df['affiliation'] == 'connecticut_drivers_united']
        elif affiliation == 'DDA':
            df = df[df['affiliation'] == 'dmv_drivers_alliance']
        elif affiliation == 'Unaffiliated':
            df = df[df['affiliation'] == 'unaffiliated']
        elif affiliation == 'All':
            pass  # Do not filter the DataFrame
        else:
            raise ValueError("Invalid affiliation parameter. Options: 'CIDU', 'RDU', 'DU', 'CDU', 'DDA', 'Unaffiliated', 'All'")

    # Cache the processed DataFrame
    try:
        # Cache the processed DataFrame
        cache.set(cache_key, df.to_json(orient='split'), timeout=30 * 24 * 3600) # TTL = One month
    except RedisError as e:
        logger.error(f"Failed to cache data: {e}")

    return df

# --------------------------------------------------------------------------------

def get_delivery_data(date_filter='3m', start_date=None, end_date=None, affiliation=None):
    """
    Fetches and returns delivery data as a DataFrame, based on either a predefined period
    or specific start and end dates provided by the user.

    Parameters:
    - date_filter (str): A predefined period for data retrieval ('7d', '1m', '3m', '6m', '1y').
    - start_date (str or None): The start date for data filtering in 'YYYY-MM-DD' format.
    - end_date (str or None): The end date for data filtering in 'YYYY-MM-DD' format.
    - affiliation (str or None): The affiliation to filter the data.

    Returns:
    - DataFrame: Processed delivery data for the requested period or date range.
    """

    if start_date and end_date:
        cache_key = f'delivery_data_custom_{start_date}_{end_date}_{affiliation}'
    else:
        cache_key = f'delivery_data_{date_filter}_{affiliation}'

    # Start measuring time
    # start_time = time.time()
    
    try:
        # Try to fetch from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            # cache_duration = time.time() - start_time
            # logger.info(f"Cache hit for {cache_key}. Loaded data from cache in {cache_duration:.2f} seconds.")
            return pd.read_json(StringIO(cached_data), orient='split')
    except RedisError as e:
        logger.error(f"Cache miss for {cache_key}: {e}")

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    else:
        end_date = datetime.now()
        if date_filter == '7d':
            start_date = end_date - timedelta(days=7)
        elif date_filter == '1m':
            start_date = end_date - timedelta(days=30)
        elif date_filter == '3m':
            start_date = end_date - timedelta(days=91)
        elif date_filter == '6m':
            start_date = end_date - timedelta(days=182)
        elif date_filter == '1y':
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=7)  # Default case
    
    # Reset start time for measuring database query duration
    # db_start_time = time.time()
    
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
    WHERE type = 'delivery' AND
    start_datetime::timestamp >= :start_date AND
    start_datetime::timestamp <= :end_date
    ORDER BY id;
    """
    # Execute the query
    with db.engine.connect() as conn:
        result = conn.execute(text(query), {'start_date': start_date, 'end_date': end_date})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    # Calculate and log time taken for database operations
    # db_duration = time.time() - db_start_time
    # logger.info(f"Loaded data from database in {db_duration:.2f} seconds.")

    # Preprocess the data

    # Replace 0 or None in 'distance' with NaN (if needed)
    df['distance'] = df['distance'].replace(0, np.nan).fillna(np.nan)

    df['income_total_charge'] = df['income_fees'] + df['income_total']
    df['current_pay'] = df['income_pay'] + df['income_bonus']  # Exclude tips from current pay
    df['pay_per_mile'] = np.where(df['distance'] != 0, df['current_pay'] / df['distance'], np.nan)

    # Fetch and clean affiliations
    df_affiliations = fetch_and_clean_affiliations()

    # Merge the affiliations with the rideshare data
    df = df.merge(df_affiliations, how='left', left_on='account', right_on='argyle_account').drop('argyle_account', axis=1)
    
    # Apply affiliation filter if provided
    if affiliation is not None:
        if affiliation == 'CIDU':
            df = df[df['affiliation'] == 'colorado_independent_drivers_united']
        elif affiliation == 'RDU':
            df = df[df['affiliation'] == 'rideshare_drivers_united']
        elif affiliation == 'DU':
            df = df[df['affiliation'] == 'drivers_union']
        elif affiliation == 'CDU':
            df = df[df['affiliation'] == 'connecticut_drivers_united']
        elif affiliation == 'DDA':
            df = df[df['affiliation'] == 'dmv_drivers_alliance']
        elif affiliation == 'Unaffiliated':
            df = df[df['affiliation'] == 'unaffiliated']
        elif affiliation == 'All':
            pass  # Do not filter the DataFrame
        else:
            raise ValueError("Invalid affiliation parameter. Options: 'CIDU', 'RDU', 'DU', 'CDU', 'DDA', 'Unaffiliated', 'All'")

    # Cache the processed DataFrame
    try:
        # Cache the processed DataFrame
        cache.set(cache_key, df.to_json(orient='split'), timeout=30 * 24 * 3600) # TTL = One month
    except RedisError as e:
        logger.error(f"Failed to cache data: {e}")

    return df

# --------------------------------------------------------------------------------

def get_aggregate_stats(start_date, end_date):
    """
    Fetches aggregate statistics for tips and pay per minute across all affiliations within a specified timeframe.

    Parameters:
    - start_date (str): The start date for data filtering in 'YYYY-MM-DD' format.
    - end_date (str): The end date for data filtering in 'YYYY-MM-DD' format.

    Returns:
    - dict: A dictionary containing aggregate statistics for tips and pay per minute.
    """
    cache_key = f"aggregate_stats_{start_date}_{end_date}"
    try:
        # Try to fetch from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return pickle.loads(cached_data)
    except RedisError as e:
        logger.error(f"Cache miss for {cache_key}: {e}")

    # If cache miss, compute the stats
    delivery_df = get_delivery_data(start_date=start_date, end_date=end_date, affiliation='All')
    rideshare_df = get_rideshare_data(start_date=start_date, end_date=end_date, affiliation='All')

    # Ensure income_total_charge is not zero to avoid division by zero errors for tip percentage calculation
    valid_delivery_df_for_tips = delivery_df[delivery_df['income_total_charge'] != 0]
    valid_rideshare_df_for_tips = rideshare_df[rideshare_df['income_total_charge'] != 0]

    # Calculate Aggregate Tip Value (Delivery)
    if not delivery_df.empty:
        aggregate_tip_value_delivery = delivery_df['income_tips'].sum() / len(delivery_df)
    else:
        aggregate_tip_value_delivery = 0

    # Calculate Aggregate Tip Percentage (Delivery)
    if not valid_delivery_df_for_tips.empty:
        valid_delivery_df_for_tips['tip_percentage'] = (valid_delivery_df_for_tips['income_tips'] / valid_delivery_df_for_tips['income_total_charge']) * 100
        aggregate_tip_percentage_delivery = valid_delivery_df_for_tips['tip_percentage'].mean()
    else:
        aggregate_tip_percentage_delivery = 0

    # Calculate Aggregate Tip Value (Rideshare)
    if not rideshare_df.empty:
        aggregate_tip_value_rideshare = rideshare_df['income_tips'].sum() / len(rideshare_df)
    else:
        aggregate_tip_value_rideshare = 0

    # Calculate Aggregate Tip Percentage (Rideshare)
    if not valid_rideshare_df_for_tips.empty:
        valid_rideshare_df_for_tips['tip_percentage'] = (valid_rideshare_df_for_tips['income_tips'] / valid_rideshare_df_for_tips['income_total_charge']) * 100
        aggregate_tip_percentage_rideshare = valid_rideshare_df_for_tips['tip_percentage'].mean()
    else:
        aggregate_tip_percentage_rideshare = 0

    # Ensure duration is not zero for pay per minute calculation
    valid_delivery_df_for_pay = delivery_df[delivery_df['duration'] > 0]
    valid_rideshare_df_for_pay = rideshare_df[rideshare_df['duration'] > 0]

    # Calculate Aggregate Pay per Minute
    if not valid_delivery_df_for_pay.empty:
        # Convert duration from seconds to minutes
        valid_delivery_df_for_pay['duration_min'] = valid_delivery_df_for_pay['duration'] / 60
        valid_delivery_df_for_pay['pay_per_min'] = valid_delivery_df_for_pay['income_total'] / valid_delivery_df_for_pay['duration_min']
        aggregate_pay_per_minute_delivery = round(valid_delivery_df_for_pay['pay_per_min'].mean(), 2)
    else:
        aggregate_pay_per_minute_delivery = 0

    if not valid_rideshare_df_for_pay.empty:
        # Convert duration from seconds to minutes
        valid_rideshare_df_for_pay['duration_min'] = valid_rideshare_df_for_pay['duration'] / 60
        valid_rideshare_df_for_pay['pay_per_min'] = valid_rideshare_df_for_pay['income_total'] / valid_rideshare_df_for_pay['duration_min']
        aggregate_pay_per_minute_rideshare = round(valid_rideshare_df_for_pay['pay_per_min'].mean(), 2)
    else:
        aggregate_pay_per_minute_rideshare = 0

    # Return the aggregate statistics as a JSON-serializable dictionary
    aggregate_stats = {
        "aggregate_tip_value_delivery": aggregate_tip_value_delivery,
        "aggregate_tip_percentage_delivery": aggregate_tip_percentage_delivery,
        "aggregate_tip_value_rideshare": aggregate_tip_value_rideshare,
        "aggregate_tip_percentage_rideshare": aggregate_tip_percentage_rideshare,
        "aggregate_pay_per_minute_delivery": aggregate_pay_per_minute_delivery,
        "aggregate_pay_per_minute_rideshare": aggregate_pay_per_minute_rideshare
    }

    try:
        # Cache the computed statistics
        cache.set(cache_key, pickle.dumps(aggregate_stats), timeout=3600)  # Cache for 1 hour
    except RedisError as e:
        logger.error(f"Failed to cache data: {e}")

    return aggregate_stats

# --------------------------------------------------------------------------------

def get_rideshare_pay_breakdown_df(date_filter='7d', start_date=None, end_date=None):
    """
    Fetches and returns a DataFrame containing a breakdown of rideshare payments,
    optionally filtered by a predefined period or specific start and end dates.

    Parameters:
    - date_filter (str): A predefined period for data retrieval ('7d', '1m', '3m', '6m', '1y').
                         Used only if start_date and end_date are not provided.
    - start_date (str or None): The start date for data filtering in 'YYYY-MM-DD' format.
    - end_date (str or None): The end date for data filtering in 'YYYY-MM-DD' format.

    Returns:
    - DataFrame: A pandas DataFrame containing the rideshare payment breakdown.
    """
    # Use the previously defined function to fetch rideshare data with caching
    df = get_rideshare_data(date_filter, start_date, end_date)

    # Filter the DataFrame to include only the relevant columns for payment breakdown
    df = df[['id', 'income_fees', 'income_pay', 'income_tips', 'income_bonus']]

    # Convert columns to float, ensuring any non-numeric entries are handled gracefully
    for column in ['income_fees', 'income_pay', 'income_tips', 'income_bonus']:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0.0).astype(float)

    return df

# --------------------------------------------------------------------------------

def get_delivery_pay_breakdown_df(date_filter='7d', start_date=None, end_date=None):
    """
    Fetches and returns a DataFrame containing a breakdown of delivery payments,
    optionally filtered by a predefined period or specific start and end dates.

    Parameters:
    - date_filter (str): A predefined period for data retrieval ('7d', '1m', '3m', '6m', '1y').
                         Used only if start_date and end_date are not provided.
    - start_date (str or None): The start date for data filtering in 'YYYY-MM-DD' format.
    - end_date (str or None): The end date for data filtering in 'YYYY-MM-DD' format.

    Returns:
    - DataFrame: A pandas DataFrame containing the rideshare payment breakdown.
    """
    # Use the previously defined function to fetch rideshare data with caching
    df = get_delivery_data(date_filter, start_date, end_date)

    # Filter the DataFrame to include only the relevant columns for payment breakdown
    df = df[['id', 'income_fees', 'income_pay', 'income_tips', 'income_bonus']]

    # Convert columns to float, ensuring any non-numeric entries are handled gracefully
    for column in ['income_fees', 'income_pay', 'income_tips', 'income_bonus']:
        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0.0).astype(float)

    return df

# --------------------------------------------------------------------------------
# The following functions are adapted from https://github.com/Princeton-HCI/ff-analysis/blob/7ee9c04106f35cb3a60eb87a3d22f72f9c4316d7/workflow/scripts/utils.py

def make_snake_case(s):
    import re
    return re.sub(r'\W+', '_', s.strip()).lower()

def load_json_safe(x):
    import json
    try:
        return json.loads(x)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError for: {x} - Error: {e}")  # Log error and problematic string
        return {}
    except TypeError as e:
        print(f"TypeError for: {x} - Error: {e}")  # Log error and problematic string
        return {}
    
# --------------------------------------------------------------------------------

# The following function is adapted from: https://github.com/Princeton-HCI/ff-analysis/blob/7ee9c04106f35cb3a60eb87a3d22f72f9c4316d7/workflow/scripts/02-load-db-dump.py

def clean_user_affiliations(affiliations):
    driver_org_translation_dict = {
        "RDU/Rideshare Drivers United": "Rideshare Drivers United",
        "Drivers Union / Teamsters 117": "Drivers Union",
    }
    affiliation_strings = [
        a["name"] if isinstance(a, dict) else a for a in affiliations
    ]
    cleaned_strings = [driver_org_translation_dict.get(a, a) for a in affiliation_strings]
    cleaned_strings = ["unaffiliated" if pd.isnull(s) else s for s in cleaned_strings]
    cleaned_strings = [make_snake_case(s) for s in cleaned_strings if s is not None]
    return cleaned_strings

def fetch_and_clean_affiliations():
    """
    Fetches user affiliations from the database, cleans them, and returns a DataFrame
    mapping argyle_account to affiliation.

    Returns:
    - DataFrame with columns ['argyle_account', 'affiliation'].
    """
    affiliation_query = text("""
    SELECT argyle_account, raw_user_meta_data
    FROM public.user_meta_data;
    """)

    with db.engine.connect() as conn:
        affiliation_result = conn.execute(affiliation_query)
        df_affiliations = pd.DataFrame(affiliation_result.fetchall(), columns=affiliation_result.keys())

    # Process affiliations
    df_affiliations['affiliations_list'] = df_affiliations['raw_user_meta_data'].apply(lambda x: x.get('affiliation', []) if isinstance(x, dict) else [])
    cleaned_affiliations = df_affiliations['affiliations_list'].apply(clean_user_affiliations)
    df_affiliations['affiliation'] = cleaned_affiliations.apply(lambda x: x[0] if x else 'unaffiliated')

    # Keep only necessary columns
    df_affiliations = df_affiliations[['argyle_account', 'affiliation']]
    
    return df_affiliations

# --------------------------------------------------------------------------------

# The following function is adapted from: https://github.com/Princeton-HCI/ff-analysis/blob/main/workflow/notebooks/reports/survey.py.ipynb

def load_data_from_sql():
    # Calculate the date 6 months ago from today
    six_months_ago = datetime.now() - timedelta(days=182)
    cache_key = f"data-{six_months_ago.strftime('%Y-%m-%d')}"

    try:
        # Check if data is in cache
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            # print("Using cached data")
            df = pickle.loads(cached_data)
            return df
    except RedisError as e:
        print(f"Failed to retrieve from cache: {e}")

    # print("Querying database")
    query = """
    SELECT id, user_id, estimate, fair, max_take, average_take
    FROM public.driver_survey_1
    WHERE created_at >= :six_months_ago
    ORDER BY id
    """

    with db.engine.connect() as conn:
        result = conn.execute(text(query), {'six_months_ago': six_months_ago})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    try:
        # Cache the DataFrame
        cache.set(cache_key, pickle.dumps(df), timeout=3600)  # cache for 1 hour
    except RedisError as e:
        print(f"Failed to save to cache: {e}")

    return df

def prepare_data(df):
    cols_to_numeric = ['average_take', 'max_take', 'estimate', 'fair']
    df[cols_to_numeric] = df[cols_to_numeric].apply(pd.to_numeric, errors='coerce')

    df["take_rate"] = df["average_take"]
    df["max_take"] = df["max_take"]
    df['estimate'] = df['estimate']
    df['fair'] = df['fair']

    df = df.dropna(subset=cols_to_numeric)

    df = df.rename(
        columns={
            "take_rate": "Actual average fee %",
            "estimate": "Driver estimates of\naverage fees",
            "fair": "What drivers said\nwould be a fair fee",
            "max_take": "Highest fee taken\nfrom a driver's fare",
        }
    )

    df = pd.melt(
        df,
        id_vars=["user_id"],
        value_vars=[
            "Driver estimates of\naverage fees",
            "What drivers said\nwould be a fair fee",
            "Actual average fee %",
            "Highest fee taken\nfrom a driver's fare",
        ]
    )

    df["value"] = df["value"].astype(float) / 100  # Scale down if values were too large
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=["value"], inplace=True)

    return df

def create_plot(df):
    # print(df['value'].describe())  # To see a quick statistical summary for debugging

    plot = (
        ggplot(df, aes(x='variable', y='value', fill='variable'))
        + geom_violin()
        + geom_boxplot(width=0.1)
        + geom_point(aes(y='value'), position=position_jitter(width=0.1))
        + scale_fill_manual(values=["#fbb4ae", "#b3cde3", "#ccebc5", "#decbe4"])
        + scale_x_discrete(
            limits=[
                "Driver estimates of\naverage fees",
                "What drivers said\nwould be a fair fee",
                "Actual average fee %",
                "Highest fee taken\nfrom a driver's fare",
            ]
        )
        + theme_classic()
        + theme(legend_position='none')
        + scale_y_continuous(
            limits=[0, 0.7],
            breaks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
            labels=percent_format(),
        )
        + labs(
            x="",
            y="% Fee",
            # title="Driver perception of Uber fees",
            # subtitle="Drivers' perceptions mirror the maximum fees taken from their fares,\nwhile the fair fee they want is less than what platforms take.\n",
            caption="Fee % includes taxes and insurance. \nAll trips used for this plot were taken in the past 6 months."
        )
        + theme(plot_caption=element_text(hjust=0, size=8))
    )

    image_stream = BytesIO()
    plot.save(image_stream, format='png', width=10, height=6, dpi=300)
    image_stream.seek(0)
    return image_stream

# --------------------------------------------------------------------------------

# Some unused functions (for now)

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
        ORDER BY id;
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