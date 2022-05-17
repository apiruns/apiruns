from typing import List


def status_code_allowed() -> List[int]:
    """Return status code allowed"""
    return list(range(100, 600))


def lower():
    """Return lambda with lower string"""
    return lambda s: s.lower()


def upper():
    """Return lambda with upper string"""
    return lambda s: s.upper()
