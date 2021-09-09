FROM python:3.7

RUN pip install poetry

COPY ./api /api
COPY pyproject.toml pyproject.toml
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
