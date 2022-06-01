# Administration

Apisrun a self-configurable api, allows through a predefined resource different actions that can modify the behavior of the api.

## Create a simple resource

**request**
POST `{host}/admin/models/`

*Request*
```json
{
    "path": "/food/",
    "schema": {
        "name": {
            "type": "string",
            "required": true
        }
    }
}
```

| Field       | Description                                    |
| ----------- | -----------------------------------------------|
| **path**    | It is the resource url must start with `/` and may or may not end with `/`, must be of type string.|
| **schema**  | Is the data structure to be persisted in the new resource. by default it is based on [cerberus](https://docs.python-cerberus.org/en/stable/index.html), allows data validation and serialization|