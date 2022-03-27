import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

def get_from_db(startTime, endTime, conn_type, attack_type):
    db = mysql.connector.connect(option_files="connector.cnf")
    print("Connection id: {0}".format(db.connection_id))
    cursor = db.cursor(dictionary=True)
    prepared_statement = """SELECT * FROM world.NSLKDD WHERE"""
    if startTime != 0  and endTime > startTime:
        prepared_statement += """ arrivalTime >= {0} AND arrivalTime <= {1}""".format(startTime, endTime)
    if conn_type is not None:
        prepared_statement += """ AND protocol_type == {0}""".format(conn_type)
    if attack_type is not None:
        prepared_statement += """ AND label == {0}""".format(attack_type)
    print(prepared_statement)
    cursor.execute(prepared_statement)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

@app.route("/events", methods=['GET'])
def events():
    startTime = int(request.args.get('startTime'))
    endTime = int(request.args.get('endTime'))
    conn_type = request.args.get('conn_type')
    attack_type = request.args.get('attack_type')
    print(startTime, endTime)
    return jsonify(get_from_db(startTime, endTime, conn_type, attack_type))
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, ssl_context='adhoc')

