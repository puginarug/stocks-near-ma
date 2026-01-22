"""Simple web server to display stock alerts data."""

from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

def read_alerts_data():
    """Read the latest alerts data from file."""
    try:
        if os.path.exists('alerts_data.json'):
            with open('alerts_data.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading alerts data: {e}")
    return {'stocks': [], 'last_update': None}

@app.route('/')
def index():
    """Main page showing stock alerts."""
    data = read_alerts_data()
    return render_template('index.html', data=data)

@app.route('/api/data')
def api_data():
    """API endpoint to get latest data as JSON."""
    data = read_alerts_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
