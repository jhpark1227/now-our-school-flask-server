from flask import Flask, request, json, jsonify
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

@app.route("/test", methods=['GET'])
def test():

    response = {
        "result": "ok"
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8090)