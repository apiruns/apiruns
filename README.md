# What's Apisrun ?

Apisrun is a tool to create microservices in an agile way. 


## Start project from docker.

NOTE: Before executing the image it is necessary to have a [mongodb](https://www.mongodb.com/en/what-is-mongodb) service started locally in the port `27017`.

```bash
docker run --name api -p 8000:8000 josesalasdev/apisrun
```

This command executes a container with an api that exposes two resources on the port that was previously defined in this case `:8000`.

Available resources:
* API Health `GET http://localhost:8000/ping/`
* Administration `GET|POST http://localhost:8000/admin/nodes/`

if you want to point to an external database engine add the following environment variables:

```bash
export ENGINE_DB_NAME=mydb
export ENGINE_URI="mongodb://root:password@localhost:27017/"
docker run --env ENGINE_DB_NAME --env ENGINE_URI --name api -p 8000:8000 josesalasdev/apisrun
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

### Test the new resource.

* Creating

POST `http://localhost:8000/users/`

*Request*
```json
{
    "username": "pepito",
    "age": 30,
    "is_admin": false,
    "level": 10.1
}
```

*Response 201*
```json
{
    "username": "pepito",
    "age": 30,
    "is_admin": false,
    "level": 10.1,
    "reference_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
}
```

* Creating with errors

POST `http://localhost:8000/users/`

*Request*
```json
{
    "username": "pepito",
    "age": 30,
    "is_admin": 30
}
```

*Response 400*
```json
{
    "is_admin": [
        "must be of boolean type"
    ]
}
```

* Retrieve

GET `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`

*Response 200*
```json
{
    "username": "pepito",
    "age": 30,
    "is_admin": false,
    "level": 10.1,
    "reference_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
}
```

* List

GET `http://localhost:8000/users/`

*Response 200*
```json
[
    {
        "username": "pepito",
        "age": 30,
        "is_admin": false,
        "level": 10.1,
        "reference_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
    }
]
```

* Updating

PUT `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`

*Request*
```json
{
    "username": "juan",
    "age": 38,
    "is_admin": false,
    "level": 11.1
}
```

*Response 204*

* Editing

PATCH `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`

*Request*
```json
{
    "username": "sofi"
}
```

*Response 204*

* Deleting

DELETE `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`


*Response 204*

### List created resources.

GET `http://localhost:8000/admin/nodes/`

*Request*
```json
[
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
        "model": "users",
        "reference_id": "bf069dc7-db7f-4639-a47f-16fb6748fd4d"
    }
]
```
