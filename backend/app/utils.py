from sqlalchemy import text
from app import app, db
import pandas as pd

def get_rideshare_df():
    # Database query to retrieve rideshare data
    query = """
    SELECT * FROM public.argyle_driver_activities
    WHERE type = 'rideshare'
    ORDER BY id
    LIMIT 2000;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Preprocess the data
    df['income_total_charge'] = df['income_fees'] + df['income_total']
    df['current_pay'] = df['income_pay'] + df['income_bonus'] # exclude tips from current pay
    df['pay_per_mile'] = df['current_pay'] / df['distance']
    
    return df

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