import uuid
from datetime import date
from datetime import datetime


def singleton(class_):
    """Singleton"""
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_or_create_model(name) -> str:
    """Get or create model name with uuid.

    Args:
        name (str): Model name.

    Returns:
        str: Original name or uuid name.
    """
    if not name:
        u = uuid.uuid4()
        return f"model_{str(u)}"
    return name
