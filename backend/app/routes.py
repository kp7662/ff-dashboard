# backend/app/routes.py
# Standard library imports
import random
import json
import base64

# Third-party libraries
import folium
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from flask import jsonify, send_file, request, redirect
from sqlalchemy import text

# Local application imports
from app import app
from .utils import *

# --------------------------------------------------------------------------------

@app.route("/")
def home():
    return redirect("http://localhost:5173/")

# --------------------------------------------------------------------------------

@app.route('/rideshare-data')
def rideshare_data_route():
    # start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')
    affiliation = request.args.get('affiliation')

    rideshare_df = get_rideshare_data(date_filter='3m', start_date=None, end_date=None , affiliation=affiliation)
    # rideshare_df = get_rideshare_data(date_filter=None, start_date='2024-01-01', end_date='2024-03-01')
    # Convert DataFrame to JSON or other desired format for the response
    rideshare_data = rideshare_df.to_dict(orient='records')
    return jsonify({"rideshare_data": rideshare_data})

@app.route('/delivery-data')
def delivery_data_route():
    # start_date = request.args.get('start_date')
    # end_date = request.args.get('end_date')
    affiliation = request.args.get('affiliation')

    delivery_df = get_delivery_data(date_filter='3m', start_date=None, end_date=None , affiliation=affiliation)
    # delivery_df = get_delivery_data(date_filter=None, start_date='2024-01-01', end_date='2024-03-01')
    # Convert DataFrame to JSON or other desired format for the response
    delivery_data = delivery_df.to_dict(orient='records')
    return jsonify({"delivery_data": delivery_data})

# --------------------------------------------------------------------------------

@app.route('/rideshare-sign-ups')
def rideshare_sign_ups():
    # Generate the current timestamp as the last updated time
    last_updated = datetime.utcnow().strftime('%m/%d/%y')

    # Get the affiliation, start_date, and end_date parameters from the request URL
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    affiliation = request.args.get('affiliation')

    # Call get_rideshare_data() function with the affiliation, start_date, and end_date parameters
    rideshare_df = get_rideshare_data(date_filter='3m', start_date=start_date, end_date=end_date, affiliation=affiliation)
    rideshare_data = rideshare_df.to_dict(orient='records')

    unique_accounts = {data['account'] for data in rideshare_data}

    # Calculate the total number of unique accounts
    total_sign_ups = len(unique_accounts)

    return jsonify({'total_sign_ups': total_sign_ups, 'last_updated': last_updated})

# --------------------------------------------------------------------------------

@app.route('/delivery-sign-ups')
def delivery_sign_ups():
    # Generate the current timestamp as the last updated time
    last_updated = datetime.utcnow().strftime('%m/%d/%y')

    # Get the affiliation, start_date, and end_date parameters from the request URL
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    affiliation = request.args.get('affiliation')

    # Call get_delivery_data() function with the affiliation, start_date, and end_date parameters
    delivery_df = get_delivery_data(date_filter='3m', start_date=start_date, end_date=end_date, affiliation=affiliation)
    delivery_data = delivery_df.to_dict(orient='records')

    unique_accounts = {data['account'] for data in delivery_data}

    # Calculate the total number of unique accounts
    total_sign_ups = len(unique_accounts)

    return jsonify({'total_sign_ups': total_sign_ups, 'last_updated': last_updated})

# --------------------------------------------------------------------------------

@app.route('/average-tips-per-delivery')
def average_tips_per_delivery():
    # Extract query parameters for affiliation, start_date, and end_date
    affiliation = request.args.get('affiliation')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Fetch delivery data using the get_delivery_data function for the specific affiliation
    delivery_df = get_delivery_data(start_date=start_date, end_date=end_date, affiliation=affiliation)

    # Fetch rideshare data using the get_delivery_data function for the specific affiliation
    rideshare_df = get_rideshare_data(start_date=start_date, end_date=end_date, affiliation=affiliation)

    # Ensure income_total_charge is not zero to avoid division by zero errors for percentage calculation
    valid_delivery_df = delivery_df[delivery_df['income_total_charge'] != 0]
    valid_rideshare_df = rideshare_df[rideshare_df['income_total_charge'] != 0]

    # Calculation 1: Average Tip Value per Delivery Order
    if not delivery_df.empty:
        average_tip_value = round(delivery_df['income_tips'].sum() / len(delivery_df), 2)
    else:
        average_tip_value = 0

    # Calculation 2: Percentage of Average Tip per Delivery Order
    if not valid_delivery_df.empty:
        valid_delivery_df['tip_percentage'] = (valid_delivery_df['income_tips'] / valid_delivery_df['income_total_charge']) * 100
        tip_percentage_mean = valid_delivery_df['tip_percentage'].mean()
        average_tip_percentage = round(tip_percentage_mean) if not pd.isna(tip_percentage_mean) else 0
    else:
        average_tip_percentage = 0

        # Calculation 3: Average Tip Value per Rideshare Order
    if not rideshare_df.empty:
        average_tip_value_rideshare = round(rideshare_df['income_tips'].sum() / len(rideshare_df), 2)
    else:
        average_tip_value_rideshare = 0

    # Calculation 4: Percentage of Average Tip per Rideshare Order
    if not valid_rideshare_df.empty:
        valid_rideshare_df['tip_percentage'] = (valid_rideshare_df['income_tips'] / valid_rideshare_df['income_total_charge']) * 100
        tip_percentage_mean_rideshare = valid_rideshare_df['tip_percentage'].mean()
        average_tip_percentage_rideshare = round(tip_percentage_mean_rideshare) if not pd.isna(tip_percentage_mean_rideshare) else 0
    else:
        average_tip_percentage_rideshare = 0

    # Fetch aggregate statistics for the same timeframe
    aggregate_stats = get_aggregate_stats(start_date=start_date, end_date=end_date)
    aggregate_tip_value_delivery = round(aggregate_stats["aggregate_tip_value_delivery"], 2)
    aggregate_tip_value_rideshare = round(aggregate_stats["aggregate_tip_value_rideshare"], 2)
    # Ensure that aggregate_tip_percentage_delivery is not NaN before rounding
    aggregate_tip_percentage_delivery = round(aggregate_stats["aggregate_tip_percentage_delivery"]) if not np.isnan(aggregate_stats["aggregate_tip_percentage_delivery"]) else 0
    aggregate_tip_percentage_rideshare = round(aggregate_stats["aggregate_tip_percentage_rideshare"]) if not np.isnan(aggregate_stats["aggregate_tip_percentage_rideshare"]) else 0

    # Return the calculated values along with aggregate stats in JSON format
    return jsonify({
        "average_tip_value_per_delivery_order": average_tip_value,
        "average_tip_percentage_per_delivery_order": average_tip_percentage,
        "average_tip_value_per_rideshare_order": average_tip_value_rideshare,
        "average_tip_percentage_per_rideshare_order": average_tip_percentage_rideshare,

        "aggregate_tip_value_delivery": aggregate_tip_value_delivery,
        "aggregate_tip_percentage_delivery": aggregate_tip_percentage_delivery,
        "aggregate_tip_value_rideshare": aggregate_tip_value_rideshare,
        "aggregate_tip_percentage_rideshare": aggregate_tip_percentage_rideshare,
    })

# --------------------------------------------------------------------------------

@app.route('/average-pay-per-min')
def average_pay_per_min():
    # Extract query parameters for affiliation, start_date, and end_date
    affiliation = request.args.get('affiliation')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Fetch delivery data using the get_delivery_data function for the specific affiliation
    delivery_df = get_delivery_data(start_date=start_date, end_date=end_date, affiliation=affiliation)
    rideshare_df = get_rideshare_data(start_date=start_date, end_date=end_date, affiliation=affiliation)

    # Ensure duration is not zero to avoid division by zero errors
    valid_delivery_df = delivery_df[delivery_df['duration'] > 0]

    # Calculation: Average Pay per Minute for the specified affiliation
    if not valid_delivery_df.empty:
        # Convert duration from seconds to minutes
        valid_delivery_df['duration_min'] = valid_delivery_df['duration'] / 60
        # Calculate pay per minute
        valid_delivery_df['pay_per_min'] = valid_delivery_df['income_total'] / valid_delivery_df['duration_min']
        average_pay_per_minute_delivery = round(valid_delivery_df['pay_per_min'].mean(), 2)
    else:
        average_pay_per_minute_delivery = 0

    valid_rideshare_df = rideshare_df[rideshare_df['duration'] > 0]

    if not valid_rideshare_df.empty:
        # Convert duration from seconds to minutes
        valid_rideshare_df['duration_min'] = valid_rideshare_df['duration'] / 60
        # Calculate pay per minute
        valid_rideshare_df['pay_per_min'] = valid_rideshare_df['income_total'] / valid_rideshare_df['duration_min']
        average_pay_per_minute_rideshare = round(valid_rideshare_df['pay_per_min'].mean(), 2)
    else:
        average_pay_per_minute_rideshare = 0

    # Fetch aggregate statistics for the same timeframe across all affiliations
    aggregate_stats = get_aggregate_stats(start_date=start_date, end_date=end_date)

    # Extract the aggregate pay per minute from the aggregate statistics
    aggregate_pay_per_minute_delivery = aggregate_stats.get("aggregate_pay_per_minute_delivery", 2)
    aggregate_pay_per_minute_rideshare = aggregate_stats.get("aggregate_pay_per_minute_rideshare", 2)

    # Return the calculated value along with aggregate stats in JSON format
    return jsonify({
        "average_pay_per_minute_delivery": average_pay_per_minute_delivery,
        "average_pay_per_minute_rideshare": average_pay_per_minute_rideshare,
        "aggregate_pay_per_minute_delivery": aggregate_pay_per_minute_delivery,
        "aggregate_pay_per_minute_rideshare": aggregate_pay_per_minute_rideshare
    })
# --------------------------------------------------------------------------------

@app.route('/rideshare/average-trip-duration')
def average_trip_duration():
    average_trip_duration = get_rideshare_avg_trip_duration()
    average_trip_duration_rounded = round(average_trip_duration, 2)
    return jsonify({"average_trip_duration": average_trip_duration_rounded})

# --------------------------------------------------------------------------------

@app.route('/rideshare/monthly-pay')
def rideshare_monthly_pay():
    rideshare_df = get_rideshare_monthly_pay()

    # Formula to calculate monthly average pay:
    rideshare_df['datetime'] = pd.to_datetime(rideshare_df['start_datetime'])
    rideshare_df['current_pay'] = pd.to_numeric(rideshare_df['current_pay'], errors='coerce')

    # Create a new column 'year_month' to store the year and month of each ride
    rideshare_df['year_month'] = rideshare_df['datetime'].dt.to_period('M')

    # Calculate monthly average pay
    monthly_average_pay = rideshare_df.groupby('year_month')['current_pay'].mean().reset_index()

    # Convert year_month to string for better readability in the JSON response
    monthly_average_pay['year_month'] = monthly_average_pay['year_month'].astype(str)

    # Convert DataFrame to dictionary for JSON response
    result = monthly_average_pay.to_dict(orient='records')

    return jsonify({"monthly_average_pay": result})

# --------------------------------------------------------------------------------

@app.route('/pay-breakdown')
def pay_breakdown():
    rideshare_df = get_rideshare_pay_breakdown_df(date_filter='7d', start_date=None, end_date=None)
    delivery_df = get_delivery_pay_breakdown_df(date_filter='7d', start_date=None, end_date=None)
    # rideshare_df = get_rideshare_pay_breakdown_df(date_filter=None, start_date='2023-12-01', end_date='2024-03-01')
    # delivery_df = get_delivery_pay_breakdown_df(date_filter=None, start_date='2023-12-01', end_date='2024-03-01')

    # Calculate the average for each numeric column
    rideshare_avg = rideshare_df[['income_fees', 'income_pay', 'income_tips', 'income_bonus']].mean().to_dict()
    delivery_avg = delivery_df[['income_fees', 'income_pay', 'income_tips', 'income_bonus']].mean().to_dict()

    # Prepare response data
    data = [
        {
            "name": "Rideshare",
            "pay": [
                {"type": "income_pay","amount": rideshare_avg['income_pay']},
                {"type": "income_tips", "amount": rideshare_avg['income_tips']},
                {"type": "income_bonus", "amount": rideshare_avg['income_bonus']},
                {"type": "income_fees", "amount": rideshare_avg['income_fees']}
            ]
        },
        {
            "name": "Delivery",
            "pay": [
                {"type": "income_pay", "amount": delivery_avg['income_pay']},
                {"type": "income_tips", "amount": delivery_avg['income_tips']},
                {"type": "income_bonus", "amount": delivery_avg['income_bonus']},
                {"type": "income_fees", "amount": delivery_avg['income_fees']}
            ]
        }
    ]

    # Return the data as JSON
    return jsonify(data)

# --------------------------------------------------------------------------------

@app.route('/view-plot')
def view_plot():
    df = load_data_from_sql()
    prepared_data = prepare_data(df)
    image_stream = create_plot(prepared_data)
    
    image_stream.seek(0)  # Go to the beginning of the stream
    base64_data = base64.b64encode(image_stream.read()).decode('utf-8')
    return jsonify({'image': 'data:image/png;base64,' + base64_data})

# --------------------------------------------------------------------------------

@app.route('/trips-per-driver-chart')
def trips_per_account_chart():
    # Fetch and preprocess the rideshare data
    rideshare_df = get_rideshare_data(date_filter='1m', start_date=None, end_date=None)
    
    # Get the number of trips per account
    trips_per_account = rideshare_df['account'].value_counts().reset_index()
    trips_per_account.columns = ['account', 'number_of_trips']
    
    # Plot the number of trips per account
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x='account', y='number_of_trips', data=trips_per_account, color='skyblue')
    plt.title('Number of Trips per Account', fontsize=16)
    plt.xlabel('Account', fontsize=14)
    plt.ylabel('Number of Trips', fontsize=14)
    plt.xticks(rotation=45)
    
    # Annotate rounded count above each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points',
                    weight='bold', fontsize=12)
    
    # Save the plot to a file
    chart_path = '/tmp/count_trips_per_account.svg'
    plt.savefig(chart_path)
    plt.close()
    
    # Serve the file
    return send_file(chart_path, mimetype='image/svg+xml')

# --------------------------------------------------------------------------------

# Define a list of colors for the routes
colors = ['darkred', 'blue', 'green', 'purple', 'orange', 
          'darkblue', 'darkgreen', 'cadetblue', 
          'darkpurple', 'lightblue', 'lightgreen']


# Code adapted from: https://github.com/Princeton-HCI/ff-analysis/blob/main/workflow/notebooks/analyses/initial-exploration.qmd
@app.route('/rideshare/<user_id>/map', methods=['GET'])
def generate_map_for_user(user_id, date_filter='1m', start_date=None, end_date=None):
    # Fetch data using the get_rideshare_data function
    df = get_rideshare_data(date_filter, start_date, end_date)

    # Filter the DataFrame for the specific user and conditions
    df_filtered = df[(df['user'] == user_id) &
                     (df['income_fees'] > 0) &
                     (df['income_total_charge'] > 0)].copy()
    
    # Sort by start_datetime
    df_filtered.sort_values(by='start_datetime', ascending=False, inplace=True)

    # Calculate take_rate
    df_filtered['take_rate'] = df_filtered.apply(
        lambda x: x['income_fees'] / (x['income_total_charge'] - x['income_tips']) 
        if (x['income_total_charge'] - x['income_tips']) != 0 else None, axis=1)
    
    # Filter items where take_rate > 30%
    df_filtered = df_filtered[df_filtered['take_rate'] > 0.30]

    # Initialize a map at a central location
    m = folium.Map(location=[40.748817, -73.985428], zoom_start=13)

    # Loop over data to add routes, markers, and text for take_rate > 20%
    for index, item in df_filtered.iterrows():
        try:
            start_lat = float(item['start_location_lat'])
            start_lng = float(item['start_location_lng'])
            end_lat = float(item['end_location_lat'])
            end_lng = float(item['end_location_lng'])

            # Only proceed if all coordinates are valid
            start_coords = (start_lat, start_lng)
            end_coords = (end_lat, end_lng)

            # Formatting take rate as percentage
            take_rate_text = f"Take Rate: {item['take_rate'] * 100:.2f}%"
            route_color = random.choice(colors)

            # Create popups with take rate information
            start_popup = folium.Popup(f"Start<br>{take_rate_text}", max_width=300)
            end_popup = folium.Popup(f"End<br>{take_rate_text}", max_width=300)

            # Add markers with popups and matching color
            folium.Marker(start_coords, icon=folium.Icon(color=route_color), popup=start_popup).add_to(m)
            folium.Marker(end_coords, icon=folium.Icon(color=route_color), popup=end_popup).add_to(m)
            
            # Drawing the route
            folium.PolyLine(locations=[start_coords, end_coords], color=route_color).add_to(m)

        except (TypeError, ValueError) as e:
            print(f"Skipping item due to invalid coordinates: {item}, Error: {e}")
            continue

    # Return the map's HTML representation
    return m._repr_html_()

# --------------------------------------------------------------------------------

@app.route("/affiliations")
def affiliations():
    query = text("""
    SELECT argyle_account, raw_user_meta_data
    FROM public.user_meta_data;
    """)

    with db.engine.connect() as conn:
        result = conn.execute(query)
        df_user_metadata = pd.DataFrame(result.fetchall(), columns=result.keys())

    df_user_metadata['affiliations_list'] = df_user_metadata['raw_user_meta_data'].apply(lambda x: x.get('affiliation', []) if isinstance(x, dict) else [])

    # Apply cleaning logic to affiliations
    cleaned_affiliations = df_user_metadata['affiliations_list'].apply(clean_user_affiliations)
    
    # Assume each user only has one affiliation for simplicity
    df_user_metadata['cleaned_affiliation'] = cleaned_affiliations.apply(lambda x: x[0] if x else 'unaffiliated')

    # Prepare and return JSON response
    response_data = [
        {"argyle_account": row["argyle_account"], "cleaned_affiliation": row["cleaned_affiliation"]}
        for _, row in df_user_metadata.iterrows()
    ]
    return jsonify(response_data)

# --------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)