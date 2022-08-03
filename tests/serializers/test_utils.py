from api.serializers.utils import lower
from api.serializers.utils import status_code_allowed
from api.serializers.utils import upper


def test_status_code_allowed_success():
    resp = status_code_allowed()
    assert isinstance(resp, list)
    assert len(resp) == 500


def test_lower_call_function():
    fn = lower()
    assert "mock" == fn("MOCK")


def test_upper_call_function():
    fn = upper()
    assert "MOCK" == fn("mock")
