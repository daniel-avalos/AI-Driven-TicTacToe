"""
Extensions of iterable data types, enabling bounds wise bookmarking indexing and active item setting
Enables iterable passing while preserving bookmarks
"""
from collections import OrderedDict


class ItermarkIndicator:
    """Indication that item is itermark. Equipped on index 0"""


class ItermarkError(Exception):
    """Generic Exception for general Itermark engine usage"""


def Itermark(iterable):
    """
    Extensions for iterable data types, enabling boudwise bookmarking and
    active item tracking/ and setting (type allowing)
    Whole itermark obj can be passed, preserving bookmark

    - mark: Bookmark index. Supports direct and operator assignment where
    allowed
    - active: Active item, based off current mark. Allows read/write where
    allowed

    Args:
        iterable: Iterable object type, to add Itermark functionality to

    Returns:
        Itermark object, matching the given iterable type
    """
    # todo separate elif into functions

    if ItermarkIndicator in iterable:
        # Why is user nesting Itermark obj? Stop that
        return iterable

    elif isinstance(iterable, list):
        new_list = [ItermarkIndicator] + iterable
        from ._list import ItermarkList
        return ItermarkList(new_list)

    elif isinstance(iterable, dict):
        new_dict = {ItermarkIndicator: ItermarkIndicator}
        new_dict.update(iterable)

        if type(iterable) == type(OrderedDict()):
            # OrderedDict shows as instance of dict
            from ._ordict import ItermarkOrDict
            return ItermarkOrDict(new_dict)

        from ._dict import ItermarkDict
        return ItermarkDict(new_dict)

    elif isinstance(iterable, tuple):
        new_tup = (ItermarkIndicator, ) + iterable
        from ._tuple import ItermarkTuple
        return ItermarkTuple(new_tup)

    else:
        raise TypeError(f"Currently unsupported type! \n {type(iterable)}")
