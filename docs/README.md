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
    }
}
```

* **path:** is the url that your new resource, must be unique.
* **schema:** is the data structure to be persisted in the new resource. by default it is based on [cerberus](https://docs.python-cerberus.org/en/stable/index.html).
* **name:** is the model name that identifies your resource. must be unique, this parameter is `optional`.

*Response 201*

```json
{
    "public_id": "c056e69e-b0e0-4fcb-a946-85f6c9f6caed",
    "created_at": "2022-03-23T00:09:45.708193+00:00",
    "updated_at": null,
    "deleted_at": null,
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
    "name": "model_c077e69e-b0e0-4fcb-a946-85f6c9f6cero",
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
    "public_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
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
    "public_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
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
        "public_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
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

GET `http://localhost:8000/admin/models/`

*Request*
```json
[
    {
        "public_id": "c056e69e-b0e0-4fcb-a946-85f6c9f6caed",
        "created_at": "2022-03-23T00:09:45.708193+00:00",
        "updated_at": null,
        "deleted_at": null,
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
        "name": "model_c077e69e-b0e0-4fcb-a946-85f6c9f6cero",
    }
]
```

### Status code custom.

POST `http://localhost:8000/admin/models/`

*Request*
```json
{
    "path": "/inventory",
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
    "status_code": {
        "get": 200,
        "post": 201,
        "put": 200,
        "patch": 400,
        "delete": 404
    }
}
```
* **status_code:** customize the status codes to return for each http method.

*Response 201*

```json
{
    "public_id": "c056e69e-b0e0-4fcb-a946-85f6c9f6caed",
    "created_at": "2022-03-23T00:09:45.708193+00:00",
    "updated_at": null,
    "deleted_at": null,
    "path": "/inventory",
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
    "name": "model_c077e69e-b0e0-4fcb-a946-85f6c9f6cero",
    "status_code": {
        "get": 200,
        "post": 201,
        "put": 200,
        "patch": 400,
        "delete": 404
    }
}
```
