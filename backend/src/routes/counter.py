from flask import (
    Blueprint,
    jsonify
)

import datetime

blueprint = Blueprint('counter', __name__)

RESPONSE_TEMPLATE = 'Flask server running on port 8080. Pinged {count} {times}, \
most recently on {date}.'


@blueprint.route('/')
def index():
    response = 'Flask server'
    return jsonify(response=response)


@blueprint.route('/api/v1/reset/')
def reset():
    # Instead of using Counter, return simple response
    return jsonify(response=0)


@blueprint.route('/api/v1/')
def api():
    # Instead of using Counter, use timestamp to create response
    date = datetime.datetime.now()
    dateStr = date.strftime('%c')
    
    # Create response without database
    response = f'Flask server running on port 8080. Server is active, \
most recently on {dateStr}.'
    
    return jsonify(response=response)
