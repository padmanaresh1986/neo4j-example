from flask import Flask, send_from_directory, jsonify, render_template

app = Flask(__name__)

# Serve the index.html file from the static folder
@app.route('/')
def index():
    return render_template('index.html')

# Serve CSS files
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

# Serve JavaScript files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

# Sample API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, this is your data!'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
