from backend.app import app

@app.route('/', methods=['GET'])
def index():
    return "Hello World"