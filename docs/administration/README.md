# Administration

Apiruns a self-configurable api, allows through a predefined resource different actions that can modify the behavior of the api.


* [Main](README.md#contents)
    * [Create a simple model](administration/README.md#Create-a-simple-model)
    * [List all models](administration/README.md#List-all-models)
    * [Delete a model](administration/README.md#Delete-a-model)
    * [Status code custom](administration/README.md#status-code-custom)
    * [Static response](administration/README.md#Static-response)


## Create a simple model


An `endpoint` is a `model` in apiruns. Create a new endpoint is very easy, you only need two fields: the `path` and the `schema`. Once created you will be able to consume it.

**Request**

POST `{host}/admin/models/`

```json
{
    "path": "/food/",
    "schema": {
        "price": {
            "type": "integer",
            "required": true
        }
    }
}
```

| Field       | Description                                    |
| ----------- | -----------------------------------------------|
| **path**    | It is the resource url must start with `/` and may or may not end with `/`, must be of type string.|
| **schema**  | Is the data structure to be persisted in the new resource. by default it is based on [cerberus](https://docs.python-cerberus.org/en/stable/index.html), allows data validation and serialization|


**Response 201 CREATED**

```json
{
    "public_id": "13c52bdf-f118-4ad3-acbb-712dd65e2d00",
    "created_at": "2022-05-31T01:42:52.687250+00:00",
    "updated_at": null,
    "deleted_at": null,
    "path": "/food",
    "name": "model-a92acc2b-1b64-4cf0-8a62-c349c236aa90",
    "schema": {
        "price": {
            "type": "integer",
            "required": true
        }
    },
    "status_code": {},
    "static": null,
}
```


## List all models

If you want to list all the models it is as easy as doing a get to the same resource.

**Request**

GET `{host}/admin/models/`


**Response 200 OK**

```json
[
    {
        "public_id": "13c52bdf-f118-4ad3-acbb-712dd65e2d00",
        "created_at": "2022-05-31T01:42:52.687250+00:00",
        "updated_at": null,
        "deleted_at": null,
        "path": "/food",
        "name": "model-a92acc2b-1b64-4cf0-8a62-c349c236aa90",
        "schema": {
            "price": {
                "type": "integer",
                "required": true
            }
        },
        "status_code": {},
        "static": null,
    }
]
```


## Delete a model

Currently it is not possible to modify a model after it is created, so you can do that from this resource to delete a model.

**Request**

DELETE `{host}/admin/models/model-a92acc2b-1b64-4cf0-8a62-c349c236aa90`


**Response 204 No content**


## Status code custom

If we want to customize the `status codes` in a model, it is possible to do so by adding a [valid code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) to the `status_code` field and defining a valid code for each http method.

**Request**

POST `{host}/admin/models/`

```json
{
    "path": "/products/",
    "schema": {
        "name": {
            "type": "string",
            "required": true
        },
        "price": {
            "type": "integer",
            "required": true
        }
    },
    "status_code": {
        "get": 200,
        "post": 200,
        "put": 200,
        "patch": 404,
        "delete": 200
    }
}
```

| Field       | Description                                    |
| ----------- | -----------------------------------------------|
| **status_code** | This field allows you to customize the response status codes for each http method. If you don't define the status codes, apiruns will take the defaults.|


**Response 201 CREATED**

```json
{
    "public_id": "92dfe9e3-a422-43dd-8047-29aa20adae38",
    "created_at": "2020-06-02T02:18:50.326145+00:00",
    "updated_at": null,
    "deleted_at": null,
    "path": "/products",
    "name": "model-2d6aff5f-f4ac-4b00-8b2f-ec97bcbc4aa5",
    "schema": {
        "name": {
            "type": "string",
            "required": true
        },
        "price": {
            "type": "integer",
            "required": true
        }
    },
    "status_code": {
        "GET": 200,
        "POST": 200,
        "PUT": 200,
        "PATCH": 404,
        "DELETE": 200
    },
    "static": null
}
```


## Static response

It is very common in the industry to return a static response when consuming a resource, which is why this method allows you to return a valid json for each of the available http methods.

**Request**

POST `{host}/admin/models/`

```json
{
    "path": "/articles/",
    "schema": {
        "name": {
            "type": "string",
            "required": true
        },
        "price": {
            "type": "integer",
            "required": true
        }
    },
    "status_code": {
        "get": 200,
        "post": 200,
        "put": 200,
        "patch": 200,
    },
    "static": {
        "get": {"mgs": "I'm a static response"}
    }
}
```

| Field       | Description                                    |
| ----------- | -----------------------------------------------|
| **static** |  This field allows to return a json for each http method, the http methods that are not specified will be automatically disabled |


**Response 201 CREATED**

```json
{
    "public_id": "92dfe9e3-a422-43dd-8047-29aa20adae38",
    "created_at": "2020-06-02T02:18:50.326145+00:00",
    "updated_at": null,
    "deleted_at": null,
    "path": "/articles",
    "name": "model-2d6aff5f-f4ac-4b00-8b2f-ec97bcbc4aa5",
    "schema": {
        "name": {
            "type": "string",
            "required": true
        },
        "price": {
            "type": "integer",
            "required": true
        }
    },
    "status_code": {
        "GET": 200,
        "POST": 200,
        "PUT": 200,
        "PATCH": 404,
        "DELETE": 200
    },
    "static": {
        "get": {"mgs": "I'm a static response"},
        "post": {"error": "I'm a other static response"},
    }
}
```
