# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os
import logging

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ffreadonly.aojwofrwvbkplkyfmosi:Shoto1ungee2lae@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Load database URI from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure cache
# app.config['CACHE_TYPE'] = 'SimpleCache' 
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app)

# Configure basic logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more verbosity
logger = logging.getLogger(__name__)

# Configure CORS to allow requests from frontend origin
CORS(app)

db = SQLAlchemy(app)
cache = Cache(app)

from app import routes
