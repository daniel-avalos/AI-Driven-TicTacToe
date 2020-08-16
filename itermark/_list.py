from ._z_itermark_engine import _ItermarkEngine
from . import ItermarkIndicator, ItermarkError


class ItermarkList(_ItermarkEngine, list, ):
    """_ItermarkEngine string object, Adding bookmarking functionality"""

    def clear(self) -> None:
        """ Remove all items from list, excluding ItermarkIndicator """
        for ndx in range(self.__len__() - 1, 0, -1):
            self.__delitem__(ndx)

    def remove(self, __value) -> None:
        """
        Remove first occurrence of value. Raises ValueError if the value is
        not present; raises ItermarkError If value is ItermarkIndicator
        """
        if __value == ItermarkIndicator:
            raise ItermarkError("Cannot remove ItermarkIndicator!")
        super().remove(__value)

    def pop(self, __index: int = ...):
        """
        Remove and return item at index (default last).  Raises IndexError
        if list is empty or index is out of range; raises ItermarkError if
        item is ItermarkIndicator
        """
        if not __index or isinstance(__index, type(...)):
            try:
                __index = self._mark_range[-1]
            except IndexError:
                # _mark_range == range(1, 1) Only ItermarkIndicator left
                raise ItermarkError("Cannot pop ItermarkIndicator") from None
        if __index not in range(0, self.__len__()):
            raise IndexError("Pop index out of range")
        to_return = self[__index]
        self.__delitem__(__index)
        return to_return

    def reverse(self):
        """Reverses list, keeping ItermarkIndicator at [0]"""
        new_list = []
        for ndx in range(self.__len__()-1, 0, -1):
            new_list.append(self[ndx])
            self.__delitem__(ndx)
        for entry in new_list:
            self.append(entry)
