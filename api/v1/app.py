#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''Closes connection to storage'''
    if storage is not None:
        storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error handler for the 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
