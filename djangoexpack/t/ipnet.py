#!/usr/bin/env python3
"""
>>> from djangoexpack.types import IPv4Network
>>> ni = IPv4Network("192.168.22.30/24")
>>> ni
IPv4Network('192.168.22.0/24')

>>> ni.value, ni.first, ni.last, ni.prefixlen
(3232241152, 3232241152, 3232241407, 24)

>>> hex(ni.value), hex(ni.first), hex(ni.last)
('0xc0a81600', '0xc0a81600', '0xc0a816ff')

>>> ni.ip
IPv4Address('192.168.22.0')

>>> ni.network
IPv4Address('192.168.22.0')

>>> ni.broadcast
IPv4Address('192.168.22.255')

>>> ni.netmask
IPv4Address('255.255.255.0')

>>> ni.hostmask
IPv4Address('0.0.0.255')

>>> ni.cidr
IPv4Network('192.168.22.0/24')

>>> ni.ipv4()
IPv4Network('192.168.22.0/24')

>>> ni.ipv6()
Traceback (most recent call last):
...
ValueError: cannot switch IP versions using copy constructor!

>>> ni.next()
IPv4Network('192.168.23.0/24')

>>> ni.previous()
IPv4Network('192.168.21.0/24')

>>> from djangoexpack.types import IPv4Network
>>> nx = IPv4Network('192.23.55.64/26')
>>> list(nx.iter_hosts())
[IPv4Address('192.23.55.65'), IPv4Address('192.23.55.66'), IPv4Address('192.23.55.67'), IPv4Address('192.23.55.68'), IPv4Address('192.23.55.69'), IPv4Address('192.23.55.70'), IPv4Address('192.23.55.71'), IPv4Address('192.23.55.72'), IPv4Address('192.23.55.73'), IPv4Address('192.23.55.74'), IPv4Address('192.23.55.75'), IPv4Address('192.23.55.76'), IPv4Address('192.23.55.77'), IPv4Address('192.23.55.78'), IPv4Address('192.23.55.79'), IPv4Address('192.23.55.80'), IPv4Address('192.23.55.81'), IPv4Address('192.23.55.82'), IPv4Address('192.23.55.83'), IPv4Address('192.23.55.84'), IPv4Address('192.23.55.85'), IPv4Address('192.23.55.86'), IPv4Address('192.23.55.87'), IPv4Address('192.23.55.88'), IPv4Address('192.23.55.89'), IPv4Address('192.23.55.90'), IPv4Address('192.23.55.91'), IPv4Address('192.23.55.92'), IPv4Address('192.23.55.93'), IPv4Address('192.23.55.94'), IPv4Address('192.23.55.95'), IPv4Address('192.23.55.96'), IPv4Address('192.23.55.97'), IPv4Address('192.23.55.98'), IPv4Address('192.23.55.99'), IPv4Address('192.23.55.100'), IPv4Address('192.23.55.101'), IPv4Address('192.23.55.102'), IPv4Address('192.23.55.103'), IPv4Address('192.23.55.104'), IPv4Address('192.23.55.105'), IPv4Address('192.23.55.106'), IPv4Address('192.23.55.107'), IPv4Address('192.23.55.108'), IPv4Address('192.23.55.109'), IPv4Address('192.23.55.110'), IPv4Address('192.23.55.111'), IPv4Address('192.23.55.112'), IPv4Address('192.23.55.113'), IPv4Address('192.23.55.114'), IPv4Address('192.23.55.115'), IPv4Address('192.23.55.116'), IPv4Address('192.23.55.117'), IPv4Address('192.23.55.118'), IPv4Address('192.23.55.119'), IPv4Address('192.23.55.120'), IPv4Address('192.23.55.121'), IPv4Address('192.23.55.122'), IPv4Address('192.23.55.123'), IPv4Address('192.23.55.124'), IPv4Address('192.23.55.125'), IPv4Address('192.23.55.126')]

>>> list(nx.subnet(28))
[IPv4Network('192.23.55.64/28'), IPv4Network('192.23.55.80/28'), IPv4Network('192.23.55.96/28'), IPv4Network('192.23.55.112/28')]

>>> nx.supernet(22)
[IPv4Network('192.23.52.0/22'), IPv4Network('192.23.54.0/23'), IPv4Network('192.23.55.0/24'), IPv4Network('192.23.55.0/25')]

>>> from djangoexpack.types import IPv4Network
>>> ni = IPv4Network("192.168.22.30/24")
>>> IPv4Network(ni.value)
IPv4Network('192.168.22.0/32')

>>> (ni.last - ni.value).bit_length()
8

>>> 32 - (ni.last - ni.value).bit_length()
24

>>> str(ni)
'192.168.22.0/24'

>>> from djangoexpack.types import IPv4Address
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

>>> nc = IPv4Network(IPv4Address(nb.value))
>>> nc
IPv4Network('192.168.22.43/32')

>>> nc._prefixlen = 32 - (nb.last - nb.value).bit_length()
>>> nc
IPv4Network('192.168.22.43/24')

>>> from netaddr import IPNetwork
>>> IPv4Network(IPv4Network('192.23.55.88/26'))
IPv4Network('192.23.55.64/26')
>>> IPv4Network(IPNetwork('192.23.55.88/26'))
IPv4Network('192.23.55.64/26')

>>> import pickle
>>> nx = IPv4Network('192.23.55.64/26')
>>> nx.__getstate__()
(3222746944, 26, 4)

>>> ps = pickle.dumps(nx)
>>> pickle.loads(ps)
IPv4Network('192.23.55.64/26')

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./ipnet.py"
# End:
