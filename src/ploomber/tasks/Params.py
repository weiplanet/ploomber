from copy import copy
from collections import abc


class Params(abc.Mapping):
    """
    Read-only mapping to represent params passed in Task constructor. It
    initializes with a copy of the passed dictionary. It verifies that the
    dictionary does not have a key "upstream" nor "product" because they'd
    clash with the ones added upon Task rendering
    """
    def __init__(self, params=None):
        if params is None:
            self._dict = {}
        else:
            if 'upstream' in params:
                raise ValueError('Task params cannot be initialized with an '
                                 '"upstream" key as it automatically added '
                                 'upon rendering')

            if 'product' in params:
                raise ValueError('Task params cannot be initialized with an '
                                 '"product" key as it automatically added '
                                 'upon rendering')

            self._dict = copy(params)

    @classmethod
    def _from_dict(cls, params, copy_=True):
        """
        Private API for initializing Params objects with arbitrary dictionary
        """
        obj = cls(params=None)

        if copy_:
            obj._dict = copy(params)
        else:
            obj._dict = params

        return obj

    def to_dict(self):
        return copy(self._dict)

    def __getitem__(self, key):
        try:
            return self._dict[key]
        except KeyError:
            raise KeyError('Cannot obtain Task param named '
                           '"{}", declared params are: {}'.format(
                               key, list(self._dict.keys())))

    def __setitem__(self, key, value):
        raise RuntimeError('Task params are read-only, if you need a copy'
                           ' use Params.to_dict() (returns a shallow copy)'
                           ' of the underlying dictionary')

    def __iter__(self):
        for name in self._dict.keys():
            yield name

    def __len__(self):
        return len(self._dict)

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return 'Params({})'.format(repr(self._dict))

    def get(self, key):
        return self._dict.get(key)

    def __delitem__(self, key):
        del self._dict[key]
