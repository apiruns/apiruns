from api.serializers.types.validations import lower
from api.serializers.types.validations import status_code_allowed
from api.serializers.types.validations import upper


def test_status_code_allowed():
    resp = status_code_allowed()
    assert isinstance(resp, list)
    assert resp[0] == 100
    assert resp[-1] == 599
    assert len(resp) == 500


def test_string_lower():
    f = lower()
    string = "A"
    expec = "a"
    assert f(string) == expec


def test_string_upper():
    f = upper()
    string = "a"
    expec = "A"
    assert f(string) == expec
