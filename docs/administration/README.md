# Administration

Apisrun a self-configurable api, allows through a predefined resource different actions that can modify the behavior of the api.

## Create a simple resource

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


## List all resources

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


## Delete a resources

**Request**

DELETE `{host}/admin/models/model-a92acc2b-1b64-4cf0-8a62-c349c236aa90`


**Response 204 No content**
