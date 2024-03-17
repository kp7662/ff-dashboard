from sqlalchemy import text
from app import app, db
import pandas as pd

def get_rideshare_df():
    # Database query to retrieve rideshare data
    # TODO: order this query so the result is consistent
    query = """
    SELECT id, account, type, income_fees, income_pay, income_total, duration
    FROM public.argyle_driver_activities, user
    WHERE type = 'rideshare'
    LIMIT 2000;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Preprocess the data
    df['income_total_charge'] = df['income_fees'] + df['income_total']
    
    return df

def get_delivery_df():
    # Database query to retrieve delivery data
    query = """
    SELECT id, account, type, income_fees, income_pay, income_total
    FROM public.argyle_driver_activities, user
    WHERE type = 'delivery'
    LIMIT 2000;
    """
    with db.engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
    # Preprocess the data
    df['income_total_charge'] = df['income_fees'] + df['income_total']
    
    return df
