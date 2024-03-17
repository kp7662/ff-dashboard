# backend/run.py
from dotenv import load_dotenv
load_dotenv()  # This loads the variables from .env

import os
print(os.environ.get('SQLALCHEMY_DATABASE_URI'))

from app import app

if __name__ == '__main__':
    app.run(debug=True)




# def main():
#     if len(sys.argv) != 2:
#         print('Usage: ' + sys.argv[0] + ' port', file=sys.stderr)
#         sys.exit(1)
    
#     try:
#         port = int(sys.argv[1])
#     except Exception:
#         print('Port must be an integer.', file=sys.stderr)
#         sys.exit(1)

#     try:
#         app.run(host='0.0.0.0', port=port, debug=True)
#     except Exception as ex:
#         print(ex, file=sys.stderr)
#         sys.exit(1)

# if __name__ == '__main__':
#     main()
#     # app.run(debug=True)