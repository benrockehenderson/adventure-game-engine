"""Adventure Game 1: Module including all custom errors.
"""


class LocationError(Exception):
    """Error raised when the location ID is not found in the map.
    """


class MapSyntaxError(Exception):
    """Error raised when the map.txt file has a bad syntax.
    """


class InvalidDirection(Exception):
    """Error raised when an invalid direction is tried to be converted from
    string to enum representation.
    """


class UnknownExecutionCondition(Exception):
    """Error raised when an invalid execution condition is tried to be converted from
    string to enum representation.
    """


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
    })
