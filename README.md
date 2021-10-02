# What's Apisrun ?

Apisrun is a tool to create microservices in an agile way. 


## Start project from docker.

NOTE: Before executing the image it is necessary to have a [mongodb](https://www.mongodb.com/en/what-is-mongodb) service started locally in the port `27017` and in the same network.

```bash
docker run --name api --network apisrun_default -p 8000:8000 josesalasdev/apisrun
```

This command executes a container with an api that exposes two resources on the port that was previously defined in this case `:8000`.

Available resources:
* API Health `GET http://localhost:8000/ping/`
* Administration `GET|POST http://localhost:8000/admin/nodes/`

if you want to point to an external database engine add the following environment variables:

```bash
export ENGINE_DB_NAME=mydb
export ENGINE_URI="mongodb://root:password@ip:27017/"
docker run --env ENGINE_URI --env ENGINE_DB_NAME --name api -p 8000:8000 josesalasdev/apisrun
```

## Start project from python.

1. Create & Activate the virtual environment.

```bash
poetry install && poetry shell
```

2. Launch the service.

```bash
uvicorn api.main:app
```

## How to use this api.

### Create a new resource in the api.

To create a new resource we just send a post to the following url:

POST `http://localhost:8000/admin/nodes/`

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
