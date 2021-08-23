from pydantic import BaseModel


def get_meta_validator(structure: dict):

    MetaClass = type(
        "MetaClass",
        (BaseModel,),
        {"name": str()}
    )
    return MetaClass
