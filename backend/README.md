# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks (Completed)

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server (Completed)

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

## API Reference
### Endpoints
GET /drinks
- Description: a public endpoint containing only the drink.short() data representation
- Request Arguments: None
- Error Codes: 404
- Returns: status code 200 and json
 ```javascript
{
"success": True,
 "drinks": drinks
} 
 ```
where drinks is the list of drinks

GET /drinks-detail
- Description: Shows the details of all drinks
- Request Arguments: JWT token, Requires permission 'get:drinks-detail'
- Error Codes: 400, 401, 403, 404
- Returns:
```javascript
{"success": True,
 "drinks": drinks}
```
where drinks is the list of drinks containing the drink.long() data
 representation
 
POST /drinks
- Description: Creates a new row in the drinks table
- Request Arguments: JWT token, requires the 'post:drinks'permission
- Error Codes: 400, 401, 403, 422
- Returns:
```javascript
{"success": True,
 "drinks": drinks}
```
where drinks is the list of drinks containing the drink.long() data
 representation
 
PATCH /drinks/<id>
- Description: Updates drink specified by id
- Request Arguments: JWT token, requires the permission 'patch:drinks
', drink_id integer value
 - Error Codes: 400, 401, 403, 404, 422
- Returns:
```javascript
{
"success": True, 
"drinks": drink
}
```
where drink an array containing only the updated drink

DELETE /drinks/<id>
- Description: Deletes drink specified by id
- Request Arguments: JWT token, requires 'delete:drinks' permission, id
 integer value for the drink to be deleted
- Error Codes: 400, 401, 403, 422
- Returns:
```javascript
{"success": True, 
"delete": drink_id}
```
where drink_id is the id of the deleted drink
