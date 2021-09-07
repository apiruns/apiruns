from pydantic import BaseModel


class Ping(BaseModel):
    """Ping Model"""

    pong: str
