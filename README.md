# What's Apisrun ?

Apisrun is a tool to create microservices in an agile way. 


## Start project.

NOTE: Before executing the image it is necessary to have a [mongodb](https://www.mongodb.com/en/what-is-mongodb) service started locally in the port `27017` and in the same network, maybe use docker `docker run -it -v mongodata:/data/db -p 27017:27017 --name mongodb -d mongo`.

1. Create & Activate the virtual environment.

Pip

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

or Poetry

```bash
poetry install && poetry shell
```

2. (Opcional) If you want to modify the api configuration you can make the environment variables available.

```bash
export ENGINE_NAME="MONGO"
export ENGINE_DB_NAME="mydb"
export ENGINE_URI="mongodb://{user}:{password}@{host|ip}:{port}/"
```

3. Launch the service.

```bash
uvicorn api.main:app
```

This command exposes the resource on the port `:8000`.


Available resources:
* API Health `GET http://localhost:8000/ping/`
* Administration `GET|POST http://localhost:8000/admin/models/`


## How to use this api.

### Create a new resource in the api.

To create a new resource we just send a post to the following url:

POST `http://localhost:8000/admin/models/`

*Request*
```json
{
    "path": "/users/",
    "schema": {
        "username": {
            "type": "string",
            "required": true
        },
        "age": {
            "type": "integer",
            "required": true
        },
        "is_admin": {
            "type": "boolean",
            "required": true
        },
        "level": {
            "type": "float",
        }
    },
    "model": "users"
}
```

* path: is the url that your new resource, must be unique.
* schema: is the data structure to be persisted in the new resource. by default it is based on [cerberus](https://docs.python-cerberus.org/en/stable/index.html).
* model: is the name that identifies your resource. must be unique.

*Response 201*

```json
{
    "reference_id": "bf069dc7-db7f-4639-a47f-16fb6748fd4d",
    "path": "/users/",
    "schema": {
        "username": {
            "type": "string",
            "required": true
        },
        "age": {
            "type": "integer",
        },
        "is_admin": {
            "type": "boolean",
        },
        "level": {
            "type": "float"
        }
    },
    "model": "users",
    "is_active": true,
    "created_at": "2021-09-08T19:38:25.826517"
}
```

### Full Documentation

👉  [https://josesalasdev.github.io/apisrun/](https://josesalasdev.github.io/apisrun/) 👈
