#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask
from flask import jsonify
from flask import request

from utilities.converters import RegexConverter

PROJECT_ROOT = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

TMPL_DIR = os.path.join(os.path.normpath(os.path.realpath(os.path.dirname(__file__))), 'www', 'templates')
STATIC_DIR = os.path.join(os.path.normpath(os.path.realpath(os.path.dirname(__file__))), 'www', 'static')

app = Flask(__name__, 
            template_folder=TMPL_DIR,
            static_folder=STATIC_DIR)
app.url_map.converters['regex'] = RegexConverter

@app.errorhandler(404)
def not_found(error=None):
    error_message = 'Not Found: ' + request.url
    message = {
        'status': 404,
        'message': error_message
    }
    resp = jsonify(message)
    resp.status_code = 404
    resp.headers['X-Status-Reason'] = error_message
    return resp


from www import population
app.register_blueprint(population.app)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))

    app.run(use_debugger=True, debug=True,
            use_reloader=True, host='0.0.0.0', port=port)
