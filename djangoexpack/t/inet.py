#!/usr/bin/env python3
"""
#-----------------------------------------------------------------------------
>>> from mns.types import IPv4Target
>>> ta = IPv4Target('192.168.23.55/26')
>>> ta
IPv4Target('192.168.23.55/26')

>>> tb = IPv4Target('192.168.23.55')
>>> tb
IPv4Target('192.168.23.55')

#-----------------------------------------------------------------------------
>>> from mns.types import IPv4Range
>>> nr = IPv4Range("192.168.22.30-192.168.22.100")
>>> nr
IPv4Range(192.168.22.30-192.168.22.100)

>>> nr._start, nr._end
(IPAddress('192.168.22.30'), IPAddress('192.168.22.100'))

>>> nr.first, nr.last
(3232241182, 3232241252)

>>> str(nr)
'192.168.22.30-192.168.22.100'

>>> nr._start
IPAddress('192.168.22.30')

>>> nr._end
IPAddress('192.168.22.100')

>>> nr = IPv4Range.from_range("192.168.22.30", "192.168.22.100")
>>> nr
IPv4Range(192.168.22.30-192.168.22.100)

>>> from mns.types import IPv4Address
>>> nr = IPv4Range.from_range(IPv4Address("192.168.22.30"), IPv4Address("192.168.22.100"))
>>> nr
IPv4Range(192.168.22.30-192.168.22.100)

>>> nr.first
3232241182
>>> IPv4Address(nr.first)
IPv4Address('192.168.22.30')

>>> nr.last
3232241252
>>> IPv4Address(nr.last)
IPv4Address('192.168.22.100')

#-----------------------------------------------------------------------------
>>> from mns.types import IPv4Network
>>> ni = IPv4Network("192.168.22.30/24")
>>> ni
IPv4Network('192.168.22.0/24')

>>> ni.value, ni.last, ni.prefixlen
(3232241152, 3232241407, 24)

>>> hex(ni.value), hex(ni.last)
('0xc0a81600', '0xc0a816ff')

>>> nx = IPv4Network(ni.value)
>>> nx
IPv4Network('192.168.22.0/32')

>>> (ni.last - ni.value).bit_length()
8

>>> 32 - (ni.last - ni.value).bit_length()
24

>>> str(ni)
'192.168.22.0/24'

>>> from mns.types import IPv4Address
>>> na = IPv4Address('192.168.22.43')
>>> na
IPv4Address('192.168.22.43')

>>> nb = IPv4Network(na.value)
>>> nb
IPv4Network('192.168.22.43/32')

>>> nb = IPv4Network(na)
>>> nb
IPv4Network('192.168.22.43/32')

>>> nb = IPv4Network('192.168.22.43')
>>> nb
IPv4Network('192.168.22.43/32')

>>> nb._prefixlen = 24
>>> nb
IPv4Network('192.168.22.43/24')

>>> nb.value, nb.last
(3232241195, 3232241407)

>>> nc = IPv4Network(IPv4Address(nb.value))
>>> nc
IPv4Network('192.168.22.43/32')

>>> nc._prefixlen = 32 - (nb.last - nb.value).bit_length()
>>> nc
IPv4Network('192.168.22.43/24')

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./inet.py"
# End:
