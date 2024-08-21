#!/usr/bin/env python3
"""Basic Flask app."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home end point."""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
