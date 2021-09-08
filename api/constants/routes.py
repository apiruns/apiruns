class RouterPath:
    """Router paths constant"""

    NODES = "/admin/nodes"
    LEVEL_ONE = "/{level_one}"
    LEVEL_TWO = "/{level_one}/{level_two}"
    LEVEL_THREE = "/{level_one}/{level_two}/{level_three}"
    LEVEL_FOUR = "/{level_one}/{level_two}/{level_three}/{level_four}"
    LEVEL_FIVE = "/{level_one}/{level_two}/{level_three}/{level_four}/" "{level_five}"
    LEVEL_SIX = (
        "/{level_one}/{level_two}/{level_three}/{level_four}"
        "/{level_five}/{level_six}"
    )
    LEVEL_SEVEN = (
        "/{level_one}/{level_two}/{level_three}/{level_four}"
        "/{level_five}/{level_six}/{level_seven}"
    )


class HTTPMethod:
    """Http Methods"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
