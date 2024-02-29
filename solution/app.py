from helpers import *
from manage import *
from methods.countries import *
from methods.users import *


@app.route('/api/ping', methods=['GET'])
def send():
    return jsonify({"status": "ok"}), 200


@app.route('/api/countries', methods=['GET'])
@creates_response
@validate()
def get_countries(query: CountriesRequest):
    return jsonify(as_dict(fetch_countries(query.region))), 200


@app.route('/api/countries/<alpha2>', methods=['GET'])
@creates_response
@validate()
def get_country(alpha2: str):
    return jsonify(find_country(alpha2).as_dict()), 200


@app.route('/api/auth/register', methods=['POST'])
@creates_response
@validate()
def register_user(body: RegisterUserRequest):
    user = create_user(body)
    return jsonify({"profile": user.as_dict()}), 201


if __name__ == "__main__":
    app.run(port=SERVER_PORT, debug=APP_DEBUG)
