# This file runs the backend control of the web/mobile apps
from backend.web import app

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)