# backend/app/routes.py
from flask import Flask, jsonify, send_file, send_from_directory
from app import app, db
from sqlalchemy import text
from .utils import *
import folium
import random
import time
import pandas as pd
import seaborn as sns
import flask

# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# import os

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

import random
# --------------------------------------------------------------------------------

# app = Flask(__name__)
# app = flask.Flask(__name__, template_folder='../../frontend/src/routes')

# Load database URI from environment variables
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS to allow requests from frontend origin
# CORS(app)

# db = SQLAlchemy(app)

# --------------------------------------------------------------------------------

# Define a list of colors for the routes
colors = ['darkred', 'blue', 'green', 'purple', 'orange', 
          'darkblue', 'darkgreen', 'cadetblue', 
          'darkpurple', 'lightblue', 'lightgreen']

# --------------------------------------------------------------------------------

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('../../frontend/src', 'app.html')
    return send_from_directory('../../frontend/src/routes', '+page.svelte')

@app.route("/rand")
def hello():
    return str(random.randint(0, 100))

# --------------------------------------------------------------------------------

@app.route('/api/rideshare-data')
def rideshare_data_route():
    rideshare_df = get_rideshare_df()
    # Convert DataFrame to JSON or other desired format for the response
    rideshare_data = rideshare_df.to_dict(orient='records')
    return jsonify({"rideshare_data": rideshare_data})


@app.route('/api/rideshare/average-trip-duration')
def average_trip_duration():
    rideshare_df = get_rideshare_df()
    average_trip_duration = rideshare_df['duration'].mean()
    return jsonify({"average_trip_duration": average_trip_duration})

# --------------------------------------------------------------------------------

@app.route('/api/trips-per-driver-chart')
def trips_per_account_chart():
    # Fetch and preprocess the rideshare data
    rideshare_df = get_rideshare_df()
    
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



# --------------------------------------------------------------------------------

@app.route('/api/data')
def get_data():
    # Get a database connection
    conn = db.engine.connect()
    
    # Fetch a limited number of records from the database
    query = """
    SELECT *
    FROM public.argyle_driver_activities ada
    LIMIT 10  -- Adjust the limit later
    """
    result = conn.execute(query)
    items = [dict(row) for row in result]

    # Close the database connection
    conn.close()

    return jsonify({"items": items})

# --------------------------------------------------------------------------------

# Route to generate and display a map for a specific user's driving activities.
# To-do: Need to modify code to access user_id through user_metadata table
@app.route('/api/data/user/<user_id>/map', methods=['GET'])
def generate_map_for_user(user_id):
    """
    Generates an interactive map displaying the driving activities for a specified user, identified by user_id.
    Each activity is represented as a route from the starting location to the ending location, 
    with markers indicating the start and end points. The routes are color-coded to distinguish between different activities.
    
    This function retrieves the last 100 qualifying driving activities from the `argyle_driver_activities` table,
    where both income fees and total charge are greater than zero. It calculates the take rate for each activity
    as the ratio of income fees to the net income (total charge minus tips), excluding any activities where this calculation is not possible.
    The resulting activities are sorted by take rate in descending order for display.
    
    Each marker's popup contains the activity's take rate, formatted as a percentage up to two decimal places. 
    The colors of the routes and their corresponding start/end markers are matched for visual clarity.
    
    Parameters:
    - user_id (str): The unique identifier for the user whose driving activities are to be mapped.
    
    Returns:
    - map_html (str): An HTML representation of the generated map, ready to be rendered in a web browser.
    """
    start_time = time.time()

    # Fetch and process data
    query = text("""
    SELECT id, start_location_lng, start_location_lat, end_location_lng, end_location_lat,
           income_total_charge, income_other, income_fees, income_pay, income_tips,
           distance, duration, start_location_formatted_address, end_location_formatted_address,
           start_datetime
    FROM public.argyle_driver_activities
    WHERE user = :user_id
      AND income_fees > 0
      AND income_total_charge > 0
    ORDER BY start_datetime DESC
    LIMIT 100;
    """)

    result = db.session.execute(query, {'user_id': user_id})

    # Ensure each row fetched from the database is properly converted into a dictionary
    items = [dict(row) for row in result.mappings()]
    # print(items)

    # # Print out all the coordinates retrieved from the database (for debugging)
    # for item in items:
    #     print(f"Start: ({item['start_location_lat']}, {item['start_location_lng']}), End: ({item['end_location_lat']}, {item['end_location_lng']})")

    for item in items:
        income_total_charge = item.get('income_total_charge', 0)
        income_tips = item.get('income_tips', 0)
        income_fees = item.get('income_fees', 0)

        if (income_total_charge - income_tips) != 0:
            item['take_rate'] = income_fees / (income_total_charge - income_tips)
        else:
            item['take_rate'] = None

    # Filter and sort
    filtered_sorted_items = sorted([item for item in items if item.get('take_rate') is not None], key=lambda x: x['take_rate'], reverse=True)

    # Initialize a map at a central location
    m = folium.Map(location=[40.748817, -73.985428], zoom_start=13)

    # Loop over data to add routes, markers, and text
    for item in filtered_sorted_items:
        try:
            start_lat = float(item['start_location_lat'])
            start_lng = float(item['start_location_lng'])
            end_lat = float(item['end_location_lat'])
            end_lng = float(item['end_location_lng'])

            # Only proceed if all coordinates are valid
            start_coords = (start_lat, start_lng)
            end_coords = (end_lat, end_lng)

            # Formatting take rate as percentage up to two decimal places
            take_rate_text = f"Take Rate: {item['take_rate'] * 100:.2f}%"
            route_color = random.choice(colors)

            # Create popups with take rate information
            start_popup = folium.Popup(f"Start<br>{take_rate_text}", max_width=300)
            end_popup = folium.Popup(f"End<br>{take_rate_text}", max_width=300)

            # Add markers with popups and matching color
            folium.Marker(start_coords, icon=folium.Icon(color=route_color), popup=start_popup).add_to(m)
            folium.Marker(end_coords, icon=folium.Icon(color=route_color), popup=end_popup).add_to(m)
            
            # Drawing the route with the matching color
            route_coords = [start_coords, end_coords]
            folium.PolyLine(locations=route_coords, color=route_color).add_to(m)

        except (TypeError, ValueError) as e:
            print(f"Skipping item due to invalid coordinates: {item}, Error: {e}")
            continue

    # Save the map as an HTML file or return it directly
    map_html = m._repr_html_()
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"Function execution time: {duration:.2f} seconds")

    return map_html

# --------------------------------------------------------------------------------

# Generate Maps (Without take rate)
@app.route('/api/data/user/<user_id>/map/old', methods=['GET'])
def generate_map_for_user_old(user_id):
    # Fetch and process data
    query = text("""
    SELECT id, start_location_lng, start_location_lat, end_location_lng, end_location_lat,
           income_total_charge, income_other, income_fees, income_pay, income_tips,
           distance, duration, start_location_formatted_address, end_location_formatted_address,
           start_datetime
    FROM public.argyle_driver_activities
    WHERE user = :user_id
      AND income_fees > 0
      AND income_total_charge > 0
    ORDER BY start_datetime DESC
    LIMIT 100;
    """)
    
    result = db.session.execute(query, {'user_id': user_id})

    # Ensure each row fetched from the database is properly converted into a dictionary
    items = [dict(row) for row in result.mappings()]
    print(items)
    
    # Initialize a map at a central location
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    for item in items:
        try:
            start_coords = (float(item['start_location_lat']), float(item['start_location_lng']))
            end_coords = (float(item['end_location_lat']), float(item['end_location_lng']))

            # Debug print to inspect the coordinates
            print("Start coords:", start_coords, "End coords:", end_coords)

            folium.Marker(start_coords, popup='Start').add_to(m)
            folium.Marker(end_coords, popup='End').add_to(m)
            
            folium.PolyLine(locations=[start_coords, end_coords], color='blue').add_to(m)
        except ValueError as e:
            # Catch any issues converting coordinates to floats and print the error
            print(f"Error processing item: {e}")
            continue  

    map_html = m._repr_html_()
    
    return map_html

if __name__ == '__main__':
    app.run(debug=True)
