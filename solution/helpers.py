from werkzeug.exceptions import NotFound, BadRequest
from flask import abort, jsonify, request
from flask_pydantic import ValidationError
from models import db
from exceptions import *


def as_dict(query_result):
    return [record.as_dict() for record in query_result]


def get_first_error(e):
    errors = []

    if e.form_params:
        errors += e.form_params

    if e.query_params:
        errors += e.query_params

    if e.body_params:
        errors += e.body_params

    if e.path_params:
        errors += e.path_params

    error = errors[0]
    return f"{error['msg']}: {error['loc']}"


def creates_response(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({"reason": get_first_error(e)}), 400
        except BadRequest as e:
            return jsonify({"reason": "cant parse request"}), 400
        except NotFound as e:
            return jsonify({"reason": "object not found"}), 404
        except NotUnique as e:
            return jsonify({"reason": "dublicate data"}), 409
        except IncorrectAuth as e:
            return jsonify({"reason": "access denied with provided data"}), 401
        except AccessDenied as e:
            return jsonify({"reason": "access denied"}), 403
        except Exception as e:
            print(e)
            return jsonify({"reason": "server error"}), 500

    wrapper.__name__ = func.__name__
    return wrapper


def transaction(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        db.session.commit()
        return result

    wrapper.__name__ = func.__name__
    return wrapper
