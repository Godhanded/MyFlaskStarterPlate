# Sample ReadMe

## Table Of Contents
- [Set up for Local Machine](#set-up-the-server)
- [Base Uri/Live Deployment](#base-uri)
- [Error Handling](#error-handling)
- [Permissions/Roles](#permissionsroles)
- [EndPoints](#endpoints)
  - [Authentication Routes](#authentication)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## This boiler plate supports the following extensions setup and ready to use
| extension  | Usecase |
|-----------|-----------|
| - bcrypt | password hashing|
| - black | code formating|
| - cryptography| encryption|
| - email-validator | validate emails|
| - flask-bcrypt |password hashing |
| - flask-blueprint| Modules |
| - flask-caching|caching |
| - flask-cors | cross origin |
| - flask-limiter| rate limiting|
| - flask-mail|send mails|
| - flask-migrate|data base migrations|
| - flask-session |loggin. server side sessions |
| - flask-sqlalchemy|database orm |
| - gunicorn | production server|
| - pydantic| input type checking |
| - python-dotenv |environment variables|
| - redis | caching|
| - requests| external requests|


## **Api Name API-ENDPOINT DOCUMENTATION**
---
<br>
<br>

### **Set up the server**
#### Install Dependencies
```bash
$ python3 -m venv venv

$ source venv/bin/activate

$ pip install -r requirements.txt
```
#### if you use pipenv

```bash
$ pip install pipenv

# create virtuel environment
$ pipenv --python 3.10

# Activate virtual env
$ pipenv shell

# install dependencies in requirements.txt or pipfile
$ pipenv install
```

#### Set up the Database

With Postgres running, create a `dbname` database:

```bash
$ createdb dbname
```
#### Add env Variables
create .env file and add variables as in [sample.env](sample.env)

#### Run the Server
```bash
$ python3 run.py 
```

### **Base Uri**
----
----
temporarily hosted for live testing on **https://baseuri**
....


<br>

### **Error Handling**
---
---
>Errors are returned as JSON objects in the following format with their error code

```json
{
  "error": "error name",
  "message": "error description"
}
```
The API will return 5 error types, with diffreent descriptions when requests fail;
- 400: Request unprocessable
- 403: Forbidden
- 404: resource not found
- 422: Bad Request
- 429: Too Many Requests(rate limiting)
- 500: Internal server error

<br>

### **Permissions/Roles**
---
---



### **EndPoints**
---
---
<br>

#### **AUTHENTICATION**
  > server side authentication is Used

  `POST '/auth/register'`

- Register new user,
- Request Arguements: JSON object containing
```json
{
  "email":"user email",
  "user_name":"user name",
  "password":"password at least 8 characters",
  "confirm_password":"confirm password",
  "api_key":"User Binance account api key",
  "api_secret":"User Bianance account api secret"
}
```
- Returns `message` ,`user name` and `email`
```json
{
    "message": "Success", 
    "user_name": "user_name", 
    "email": "user email"
}
```
---
<br>

  `GET '/auth/activate/${token}'`
- Activates user account
- Request Arguements: `token`- string jwt code
- Returns: JSON object containing
```json
{
    "message": "Success",
    "user_name":"user_name",
    "is_active": "boolean account is active or not",
}
```

---
<br>




## Authors
- [@Godhanded](https://github.com/Godhanded)

## Acknowledgments

- Binance-Python-Connector
