<p align="center">
  <a href="#"><img src="pictures/apiruns.png" alt="Apiruns"></a>
</p>

# <center> What's Apiruns ? </center>


Apiruns a self-configurable api based on [fastapi](https://github.com/tiangolo/fastapi), it allows you to create, modify and delete resources with a simple request. *Creating an api has never been so easy.*


## Contents

- [Start project](#start-project)
  - [Create a new endpoint](#create-a-new-endpoint)
  - [Create a new record](#create-a-new-record)
  - [Get all records](#get-all-records)
  - [Retrieve a record](#retrieve-a-record)
  - [Edit a record](#edit-a-record)
  - [Update a record](#update-a-record)
  - [Delete a record](#delete-a-record)
- [Administration](administration/README.md#Administration)
    - [Create a simple model](administration/README.md#Create-a-simple-model)
    - [List all models](administration/README.md#List-all-models)
    - [Delete a model](administration/README.md#Delete-a-model)
    - [Status code custom](administration/README.md#status-code-custom)
    - [Static response](administration/README.md#Static-response)
- [Full documentation](https://josesalasdev.github.io/apiruns/)


### Start project.

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

2. Start DB.

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

### Create a new endpoint.

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

When creating a new record, it returns a `public_id` field that represents a unique identifier of the resource. This new record enables 4 method http:

- GET `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`
- PATCH `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`
- PUT `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`
- DELETE `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`


### Get all records.

To list all records in `/users/` we need to execute the following request.

GET `http://localhost:8000/users/`

*Response 200*
```json
[
    {
        "username": "some",
        "age": 30,
        "is_admin": false,
        "level": 10.1,
        "public_id": "422594e5-ad62-4d56-837e-eab6270bf0f5"
    }
]
```

### Retrieve a record.

To retrieve a record in `/users/` we need to execute the following request with `public_id` identifier.

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



### Edit a record.

To edit a record in `/users/` we need to execute the following request with `public_id` identifier.

PATCH `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`

*Request*
```json
{
    "age": 38,
}
```

*Response 204 no content*

### Update a record.

To update a record in `/users/` we need to execute the following request with `public_id` identifier.


PUT `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`

*Request*
```json
{
    "username": "Jorge",
    "age": 39,
    "is_admin": false,
    "level": 11.1
}
```

*Response 204 no content*


### Delete a record.

To delete a record in `/users/` we need to execute the following request with `public_id` identifier.


DELETE `http://localhost:8000/users/422594e5-ad62-4d56-837e-eab6270bf0f5/`


*Response 204 con content*

### Documentation

👉  [Go to Documentation](https://josesalasdev.github.io/apiruns/) 👈
