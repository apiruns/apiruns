from api.utils.common import singleton


def test_singleton_two_instances_refer_to_the_same_address():
    @singleton
    class A:
        pass

    class_one = A()
    class_two = A()
    assert class_one == class_two
    assert id(class_one) == id(class_two)
