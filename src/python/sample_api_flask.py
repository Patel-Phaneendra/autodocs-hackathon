from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    """
    Returns a simple greeting message.
    """
    return jsonify(message="Hello, World!")

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Returns details for a specific item by ID.
    """
    return jsonify(item_id=item_id, name="Sample Item")
