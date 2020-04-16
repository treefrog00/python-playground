from flask import Flask, jsonify, request
import logging
import os
import requests

log = logging.getLogger()

app = Flask(__name__)


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form["name"]
        return jsonify(dict(msg=f"Hello {name}"))
    else:
        return "hello"


@app.route('/fish', methods=['GET'])
def get_fish():
    base_url = "https://fishbase.ropensci.org/"

    response = requests.get(
        base_url + "ecology",
    )

    if response.status_code != 200:
        raise Exception(
            "status code {}".format(
                response.status_code
            )
        )

    data = response.json()

    return data


@app.route('/postman', methods=['POST'])
def post_to_the_postman():
    base_url = "https://postman-echo.com/"

    if not request.is_json:
        return "expected json", 400

    response = requests.post(
        base_url + "post",
        json=request.json,
    )

    if response.status_code != 200:
        raise Exception(
            "status code {}".format(
                response.status_code
            )
        )

    data = response.json()

    return jsonify(data)


if __name__ == "__main__":
    port = 5000
    os.environ["FLASK_ENV"] = "development"
    log.info("Starting http server on port %s" % port)
    app.run(host="0.0.0.0", port=port)
