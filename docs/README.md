# <center> What's Apisrun ? </center>


Apisrun a self-configurable api based on [fastapi](https://github.com/tiangolo/fastapi), it allows you to create, modify and delete resources with a simple request. *Creating an api has never been so easy.*


## Start project.

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

2. DB.

Run this project it is necessary to have a [mongodb](https://www.mongodb.com/en/what-is-mongodb) service up. if it is your preference you can use docker: `docker run -it -v mongodata:/data/db -p 27017:27017 --name mongodb -d mongo`. By default it connects to this container.

(Opcional) If you want to modify the api configuration you can make the environment variables available.

```bash
export ENGINE_NAME="MONGO"
export ENGINE_DB_NAME="mydb"
export ENGINE_URI="mongodb://{user}:{password}@{host|ip}:{port}/"
```

3. Launch the service.

```bash
uvicorn api.main:app

INFO:     Started server process [25318]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

This command exposes the resource `http://localhost` on the port `:8000`.


**This api exposes 2 main resources:**
* API Health `GET http://localhost:8000/ping/`
* API Administration `GET|POST|DELETE http://localhost:8000/admin/models/`

## Create a new endpoint.

Creating a new endpoint is as easy as defining 2 fields in the body of the following resource:

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

This new endpoint `/users/` exposes **2 https methods**: 

- `GET /users/` This method allows us to list records.
- `POST /users/` This method allows us to create a record.


### Create a new record.

To create a new record in `/users/` we need to execute the following request.

POST `http://localhost:8000/users/`

*Request*
```json
{
    "username": "some",
    "age": 30,
    "is_admin": false,
    "level": 10.1
}
```

*Response 201*
```json
{
    "username": "some",
    "age": 30,
    "is_admin": false,
    "level": 10.1,
    "public_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
}
```

**public_id:** It is the identifier of the record.


#TODO

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


### Static Model.

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
    "static": {
        "all": {"this": "mock"}
    }
}
```
* **static:** this feature allows to return a static json according to the defined method, in this example it returns the same json for `all` the methods.

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
    "static": {
        "all": {"this": "mock"}
    }
}
```

Example by method:

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
    "static": {
        "get": {"this": "mock get"},
        "post": {"this": "mock post"},
        "put": {"this": "mock put"},
    }
}
```
