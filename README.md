# What's Apisrun ?

It is a service that allows you to create microservices with a dynamic structure.


## Start project

1. Create & Activate the virtual environment.

```bash
poetry install && poetry shell
```

2. Launch the service.

```bash
uvicorn api.main:app
```

3. Versifying service.

```bash
curl 127.0.0.1:8000/ping
```

