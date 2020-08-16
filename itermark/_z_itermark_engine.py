"""
Base engine for itermark functionality.

Extension for iterable data types; adds boundwise bookmark iteration, enabling
active item tracking/setting (type allowing)
"""

from typing import Optional
from . import ItermarkIndicator, ItermarkError


class _ItermarkEngine:
    """
    Itermark functions, to build on top of default iterable object types
    Type specifics inherit and supplement with any needed functions/properties

    - mark: Bookmark index of underlying iterable. Supports direct and
    operator assignment
    - active: Active item based off mark index. Read/write usage, type allowing
    """

    # -------------------------------------------------------------------------
    # Itermark Properties
    # -------------------------------------------------------------------------

    # Note: Because all public functions use _ensure_loaded(), any internal
    # calls to these functions will cause recursion. Code should only call
    #  private functions

    _mark: int = None
    """Protected bookmark index; access via mark() so boundary checks are 
    run. When there are no entries, _mark is set to None"""
    _mark_default = 1

    @property
    def mark(self) -> Optional[int]:
        """
        Get current active bookmark index

        Returns:
                Active bookmark index, or None if len=0
        """
        self._ensure_loaded()
        return self._mark

    @mark.setter
    def mark(self, new_mark: int):
        """
        Attempts to set active mark. Raises IndexError if new_mark is OOB

        Arguments:
            new_mark:
                Desired new bookmark index
        """

        mark_to_set = self._calc_if_negative_index(new_mark)
        # Preserve orig new_mark. in case of OOB, raise IndexErr w/ given mark

        if mark_to_set not in self._mark_range:
            raise IndexError(f"Given mark [{new_mark}] outside itermark index "
                             f"range 1-{self._mark_range[-1]}")

        self._mark = mark_to_set
        self._ensure_loaded()

    @property
    def active(self) -> any:
        """
        Get current active item, based off bookmark index

        Returns:
                Active item, or None if len=0
        """
        self._ensure_loaded()
        return self[self._mark]

    @active.setter
    def active(self, val: any):
        """
        Set active list item, based on current mark value

        Args:
            val: new value for current active item
        """
        self._ensure_loaded()
        self[self._mark] = val

    # -------------------------------------------------------------------------
    # Default item overrides/extensions
    # -------------------------------------------------------------------------

    def __setitem__(self, key, value):
        if key == 0:
            if value != ItermarkIndicator:
                raise ItermarkError(
                    "Cannot change or remove Itermark Indicator!")
        super().__setitem__(key, value)

    def __next__(self):
        """Emulates iterator next while preserving .mark. When reaches end of
        list, throws StopIteration and notifies user to reset .mark"""
        try:
            self._ensure_loaded()
            active_to_return = self.active
            self._mark += 1
        except IndexError:
            raise StopIteration('End of itermark iteration. set mark to -1 '
                                 'or reset to 1') from None
        return active_to_return

    # -------------------------------------------------------------------------
    # _ItermarkEngine maintenance
    # -------------------------------------------------------------------------

    def _ensure_loaded(self):
        """Ensures items exist for itermark to track. If none,
        throws excpetion ItermarkNonActive.  All public functions call this
         first; calling itermark funcs on non-existent self throws errors"""
        # self._ensure_placeholder_exists()
        if self._is_loaded:
            self._activate_mark()
        else:
            self._deactivate_mark()
            raise ItermarkError("No items for itermark to track!")

    @property
    def _is_loaded(self) -> bool:
        """bool representing if items exist in self, using __len__ check.
        Seperate from _ensure_loaded so maint funcs can run a check without
        de/activating or causing recursive loop"""
        if self.__len__() <= 1:
            return False
        return True

    @property
    def _mark_range(self) -> range:
        """Current acceptable bookmark range, using builtin obj's range and
        __len__. Excludes 0, as 0 is ItermarkIndicator"""
        return range(1, self.__len__())

    def _calc_if_negative_index(self, mark_to_calc: int) -> int:
        """Converts a negative index to actual index"""
        if mark_to_calc < 0:
            return self.__len__() + mark_to_calc
        return mark_to_calc

    def _activate_mark(self):
        """Current iterator has items, activate itermark. Checks for itermark
         iterator shortened and old mark too high and'll raise IndexError"""
        if not self._mark:
            self._mark = self._mark_default
        elif self._mark not in self._mark_range:
            raise IndexError(f"Mark [{self._mark}] out of bounds [1-"
                             f"{self._mark_range[-1]}]")
    def _deactivate_mark(self):
        """Used to disable callable attributes, if iterable becomes empty"""
        self._mark = None
