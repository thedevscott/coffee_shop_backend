import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# NOTE: Uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN

db_drop_and_create_all()


# ----------------------------------------------------------------------------
# API ROUTES
# ----------------------------------------------------------------------------
@app.route('/drinks')
def get_drinks():
    """
    GET /drinks
        a public endpoint containing only the drink.short() data representation
    :return: status code 200 and json {"success": True, "drinks": drinks} where
     drinks is the list of drinks
    """
    drinks = []

    try:
        drink_query = Drink.query.all()

        for drink in drink_query:
            drinks.append(drink.short())

        return jsonify(
            {"success": True, "drinks": drinks}
        )
    except Exception as e:
        abort(404)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    """
    GET /drinks-detail
        Requires the 'get:drinks-detail' permission
         the drink.long() data representation
    :return: status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks containing the drink.long() data
    representation
    """
    drinks = []

    try:
        drink_query = Drink.query.all()

        for drink in drink_query:
            drinks.append(drink.long())

        return jsonify(
            {"success": True, "drinks": drinks}
        )
    except Exception as e:
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    """
    Creates a new row in the drinks table and requires the 'post:drinks'
    permission
    :return: status code 200 and json {"success": True, "drinks": drink}
    """
    try:
        drink = Drink(title=request.json.get('title'),
                      recipe=json.dumps(request.json.get('recipe')))

        drink.insert()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, drink_id):
    """
    Updates drink specified by drink_id
    :param jwt: Token containing correct permissions 'patch:drinks'
    :param drink_id: ID of drink to update
    :return: status code 200 and json {"success": True, "drinks": drink}
     where drink an array containing only the updated drink
    """
    try:
        drink = Drink.query.get(drink_id)

        # Make sure we have something to work with
        if drink:

            if 'title' in request.json:
                drink.title = request.json.get('title')

            if 'recipe' in request.json:
                drink.recipe = request.json.get('recipe')

            drink.update()

            return jsonify({
                "success": True,
                "drinks": [drink.long()]
            })
        else:
            # Did not find the record
            abort(404)

    except Exception as e:
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, drink_id):
    """
    Deletes drink specified by drink_id
    :param jwt: Token containing correct permissions 'patch:drinks'
    :param drink_id: ID of drink to update
    :return: status code 200 and json {"success": True, "delete": drink_id}
    """
    try:
        drink = Drink.query.get(drink_id)

        # Make sure we have something to work with
        if drink:

            drink.delete()

            return jsonify({
                "success": True,
                "delete": drink_id
            })
        else:
            # Did not find the record
            abort(404)

    except Exception as e:
        abort(422)


# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------

@app.errorhandler(422)
def unprocessable(error):
    """Error handling for unprocessable entity
    :param error: The error object
    :return JSON indication failure with keys 'success', 'error' & 'message'
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    """
    Error handler for 404 HTTP status code
    :param error: The error object
    :return: JSON indicating failure 'success' bool, 'error' code & 'message'
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    """Authorization error handler. Takes AuthErrors and puts them in JSON
    format
    :param error: The error object
    :return JSON with 'code' and 'description' of the authorization error
    """

    return jsonify(error.error), error.status_code
