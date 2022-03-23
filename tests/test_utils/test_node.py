from api.utils.node import build_path_from_params
from api.utils.node import paths_with_slash


def test_build_path_from_params_with_uuid():
    params_with_uuid = ("users", "667605b0-8c34-4dab-8c8e-c7aef7e05bc4")
    url_original, url_modified, _uuid = build_path_from_params(params_with_uuid)
    assert url_original == "/users/667605b0-8c34-4dab-8c8e-c7aef7e05bc4"
    assert url_modified == "/users"
    assert _uuid == "667605b0-8c34-4dab-8c8e-c7aef7e05bc4"


def test_build_path_from_params_without_uuid():
    params_without_uuid = ("users",)
    url_original, url_modified, _uuid = build_path_from_params(params_without_uuid)
    assert url_original == "/users"
    assert url_modified == "/users"
    assert _uuid == None


def test_paths_with_slash():
    path = "/users"
    result = paths_with_slash(path)
    assert result == ["/users", "/users/"]


def test_paths_without_slash():
    path = "/users/"
    result = paths_with_slash(path)
    assert result == ["/users/", "/users"]


def test_build_path_without_params():
    params_with_uuid = ()
    url_original, url_modified, _uuid = build_path_from_params(params_with_uuid)
    assert url_original == "/"
    assert url_modified == "/"
    assert _uuid == None
