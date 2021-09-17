from unittest.mock import MagicMock

import pytest


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(self, *args, **kwargs)
