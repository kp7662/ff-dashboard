# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ffreadonly.aojwofrwvbkplkyfmosi:Shoto1ungee2lae@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Load database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure CORS to allow requests from frontend origin
CORS(app)

db = SQLAlchemy(app)

from app import routes
