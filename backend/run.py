# backend/run.py
from dotenv import load_dotenv
load_dotenv()

import os
print(os.environ.get('SQLALCHEMY_DATABASE_URI'))

from app import app

if __name__ == '__main__':
    app.run(debug=True)