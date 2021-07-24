from crud import *

@app.route('/create', methods=['POST'])
def create_schedule():
    request_data = request.get_json()
    try:
        return_value = create_rule(
            request_data['schedule_name'],
            request_data['instance'],
            request_data['days'],
            request_data['status']
        )
    except KeyError as e:
        return jsonify("missing parameter "+str(e))
    return jsonify(return_value)


@app.route('/update', methods=['POST'])
def update_schedule():
    request_data = request.get_json()
    try:
        return_value = create_rule(
            request_data['schedule_name'],
            request_data['instance'],
            request_data['days'],
            request_data['status']
        )
    except KeyError as e:
        return jsonify("missing parameter "+str(e))
    return jsonify(return_value)

@app.route('/delete', methods=['POST'])
def delete_schedule():
    request_data = request.get_json()
    try:
        return_value = delete_rule(
            request_data['schedule_name'],
            request_data['instance']
        )
    except KeyError as e:
        return jsonify("missing parameter "+str(e))
    return jsonify(return_value)

@app.route('/read', methods=['GET'])
def read_schedules():
    return_value = fetch_schedules()
    return jsonify(return_value)
