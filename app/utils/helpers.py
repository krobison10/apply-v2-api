from ..config import *


def implode(elements, delimiter=""):
    """
    Joins the elements of the list into a single string, with an optional delimiter.

    Parameters:
        elements (list): The list of elements to join.
        delimiter (str, optional): The string to insert between each element of the list.

    Returns:
        str: The resulting string after joining the list elements with the delimiter.
    """
    return delimiter.join(map(str, elements))


def safe_execute(function, *args, exception=Exception, default=None):
    try:
        return function(*args)
    except exception:
        return default


class Helpers:
    pass
