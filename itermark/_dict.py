from ._z_itermark_engine import _ItermarkEngine, ItermarkIndicator
# todo warning if using Dict on python <3.6


# Note that this is designed around 3.6+'s insertion ordered dictionaries
# Recommend a Collections.OrderedDict for earlier implementations
class ItermarkDict(_ItermarkEngine, dict):
    """_ItermarkEngine dict object, extending default dict functionality"""

    @property
    def active(self) -> tuple:
        self._ensure_loaded()
        return self.activekey, self.activeval

    @active.setter
    def active(self, val):
        raise TypeError("Set using .activeval, .activekey immutable!")

    @property
    def activekey(self):
        """Get active key, based on bookmark"""
        self._ensure_loaded()
        for ndx, key in enumerate(self.__iter__()):    # Iterates through keys
            if ndx == self._mark:
                return key

    @activekey.setter
    def activekey(self, key):
        raise TypeError("ItermarkDict does not support key assignment")

    @property
    def activeval(self):
        self._ensure_loaded()
        return self[self.activekey]

    @activeval.setter
    def activeval(self, val):
        self._ensure_loaded()
        self[self.activekey] = val

    def keys(self):
        all_dict = self.copy()
        all_dict.__delitem__(ItermarkIndicator)
        return all_dict.keys()

    def values(self):
        all_dict = self.copy()
        all_dict.__delitem__(ItermarkIndicator)
        return all_dict.values()
