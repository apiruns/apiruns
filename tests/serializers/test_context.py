from starlette.datastructures import QueryParams

from api.serializers.context import ContextSerializer


class TestContextSerializer:
    def test_query_params_null(self):
        # Mocks
        q = QueryParams("")
        # process
        data = ContextSerializer.query_params(q)
        # asserts
        assert data == {}

    def test_query_params_with_error(self):
        # Mocks
        q = QueryParams("pag=1&lim=0")
        # process
        data = ContextSerializer.query_params(q)
        # asserts
        assert data == {}

    def test_query_params_sucesss(self):
        # Mocks
        q = QueryParams("page=1&limit=2")
        # process
        data = ContextSerializer.query_params(q)
        # asserts
        assert data == {"limit": 2, "page": 1}
