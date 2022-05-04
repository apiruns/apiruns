from fastapi import Request


async def set_body(request: Request, b: bytes):
    """Set request body util.

    Args:
        request (Request): Request obj.
        b (bytes): Body bytes obj.
    """
    async def receive():
        body = b"{}" if b == b"" else b
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    """Get body bytes from request.

    Args:
        request (Request): _description_

    Returns:
        bytes: Body seted.
    """
    body = await request.body()
    await set_body(request, body)
    return body
