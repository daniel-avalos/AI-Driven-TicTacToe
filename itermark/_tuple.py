from ._z_itermark_engine import _ItermarkEngine


class ItermarkTuple(tuple, _ItermarkEngine):
    """_ItermarkEngine Tuple object, Adding bookmarking functionality"""

    @property
    def active(self):
        """Call to super's active property. Here for setter's reference"""
        return super(_ItermarkEngine).active

    @active.setter
    def active(self, val):
        raise TypeError("ItermarkTuple object does not support item assignment")
