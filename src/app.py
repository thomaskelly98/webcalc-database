from flask import Flask, request, Response
import pandas as pd
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

CSV_FILENAME = "webcalc_data.csv"

# test save: http://0.0.0.0:5000/?time=13:27:02&unique_id=pm6mp&value=1243
# test get: http://0.0.0.0:5000/get_value?unique_id=pm8mo

# save value
@app.route("/")
def save_value():
    # get current list of values
    unique_ids, values = read_csv()

    time = request.args.get("time")
    unique_id = request.args.get("unique_id")
    value = request.args.get("value")

    if time is None or time == "":
        invalid_return = {"error": True, "string": "Param 'time' is missing"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r
    if unique_id is None or unique_id == "":
        invalid_return = {"error": True, "string": "Param 'unique_id' is missing"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r
    if value is None or value == "":
        invalid_return = {"error": True, "string": "Param 'value' is missing"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r

    time = str(time)
    unique_id = str(unique_id)
    try:
        value = int(value)
    except Exception:
        invalid_return = {"error": True, "string": "Param 'value' is not an integer"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r

    data = "\n{},{},{}".format(time, unique_id, value)
    if any(unique_id in s for s in unique_ids):
        invalid_return = {"error": True, "string": "Unique ID already exists"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r

    append_to_csv(data)

    valid_return = {"error": False, "string": f"{unique_id}:{value}"}
    reply = json.dumps(valid_return)
    r = Response(response=reply, status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json"
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


# get value
@app.route("/get_value")
def get_value():
    # get current list of values
    unique_ids, values = read_csv()

    unique_id = request.args.get("unique_id")

    if unique_id is None or unique_id == "":
        invalid_return = {"error": True, "string": "Param 'unique_id' is missing"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r

    unique_id = str(unique_id)

    value = None
    for i in range(len(unique_ids)):
        if unique_id == unique_ids[i]:
            value = values[i]

    if value is None or value == "":
        invalid_return = {"error": True, "string": "No Value is stored for the provided ID"}
        reply = json.dumps(invalid_return)
        r = Response(response=reply, status=200, mimetype="application/json")
        r.headers["Content-Type"] = "application/json"
        r.headers["Access-Control-Allow-Origin"] = "*"
        return r

    valid_return = {"error": False, "string": f"{unique_id}:{value}", "value": value}
    reply = json.dumps(valid_return)
    r = Response(response=reply, status=200, mimetype="application/json")
    r.headers["Content-Type"] = "application/json"
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r


def create_csv():
    csv_header = "Time,ID,Value"
    file = open(CSV_FILENAME, "w")
    file.writelines(csv_header)
    file.close()
    print("Successfully created CSV file")


def read_csv():
    print("Reading Data from CSV File")
    df = pd.read_csv(CSV_FILENAME)

    # get ids and values and add to list
    unique_ids = df["ID"].tolist()
    values = df["Value"].tolist()

    return unique_ids, values


def append_to_csv(data_to_append):
    with open(CSV_FILENAME, "a") as csv_file:
        csv_file.write(data_to_append)
    print("Successfully appended to csv file")


if __name__ == "__main__":
    # create db
    create_csv()
    
    app.run(host="0.0.0.0", port=5000)
