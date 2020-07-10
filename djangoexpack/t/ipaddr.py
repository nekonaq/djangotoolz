#!/usr/bin/env python3
"""
>>> from djangoexpack.types import IPv4Address
>>> na = IPv4Address('192.168.33.2')
>>> na
IPv4Address('192.168.33.2')

>>> na.value
3232243970

>>> int(na)
3232243970

>>> str(na)
'192.168.33.2'

>>> assert(hex(id(na)) != hex(id(IPv4Address(na))))

>>> IPv4Address('2001::aaaa:bbbb:cccc:1111')
Traceback (most recent call last):
...
netaddr.core.AddrFormatError: base address ... is not IPv4

>>> from netaddr import IPAddress
>>> IPv4Address(IPv4Address('192.23.55.88'))
IPv4Address('192.23.55.88')
>>> IPv4Address(IPAddress('192.23.55.88'))
IPv4Address('192.23.55.88')

>>> import pickle
>>> nx = IPv4Address('192.23.55.88')
>>> nx.__getstate__()
(3222746968, 4)

>>> ps = pickle.dumps(nx)
>>> pickle.loads(ps)
IPv4Address('192.23.55.88')

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./ipaddr.py"
# End:
