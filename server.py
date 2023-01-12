import os
from flask import Flask, request
from src.routes import api
from src.utils import APIException

app = Flask(__name__)


# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/v1')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
