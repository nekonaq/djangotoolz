#!/usr/bin/env python3
"""
>>> from mns.types import IPv4Range
>>> ni = IPv4Range("192.168.22.30-192.168.22.42")
>>> ni
IPv4Range(192.168.22.30-192.168.22.42)

>>> str(ni)
'192.168.22.30-192.168.22.42'

>>> int(ni)
Traceback (most recent call last):
...
TypeError: int() argument must be a string, a bytes-like object or a number, not 'IPv4Range'

>>> ni._start, ni._end
(IPv4Address('192.168.22.30'), IPv4Address('192.168.22.42'))

>>> ni.first, ni.last, ni.size
(3232241182, 3232241194, 13)

>>> ni._value
Traceback (most recent call last):
...
AttributeError: _value

>>> ni.value
Traceback (most recent call last):
...
AttributeError: _value

>>> ni.cidrs()
[IPv4Network('192.168.22.30/31'), IPv4Network('192.168.22.32/29'), IPv4Network('192.168.22.40/31'), IPv4Network('192.168.22.42/32')]

>>> IPv4Range("192.168.33.80-192.168.33.93x")
Traceback (most recent call last):
...
netaddr.core.AddrFormatError: base address ... is not IPv4

>>> IPv4Range("192.168.22.44-192.168.22.31")
IPv4Range(192.168.22.31-192.168.22.44)

>>> from mns.types import IPv4Range
>>> ni = IPv4Range("192.168.33.80-192.168.33.93")
>>> IPv4Range.from_range(ni.first, ni.last)
IPv4Range(192.168.33.80-192.168.33.93)
>>> IPv4Range(ni)
IPv4Range(192.168.33.80-192.168.33.93)

>>> from mns.types import IPv4Address
>>> IPv4Range.from_range(IPv4Address("192.168.33.80"), IPv4Address("192.168.33.93"))
IPv4Range(192.168.33.80-192.168.33.93)

>>> import pickle
>>> nx = IPv4Range("192.168.33.80-192.168.33.93")
>>> nx.__getstate__()
(3232244048, 3232244061, 4)

>>> ps = pickle.dumps(nx)
>>> pickle.loads(ps)
IPv4Range(192.168.33.80-192.168.33.93)

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./iprange.py"
# End:
