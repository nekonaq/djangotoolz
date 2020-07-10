#!/usr/bin/env python3
"""
>>> from mns.types import MACAddress
>>> ma = MACAddress('d2:da:91:51:15:c7')
>>> ma
MACAddress('d2:da:91:51:15:c7')

>>> ma.value
231836182713799

>>> int(ma)
231836182713799

>>> str(ma)
'd2:da:91:51:15:c7'

>>> assert(hex(id(ma)) != hex(id(MACAddress(ma))))

>>> MACAddress('2001::aaaa:bbbb:cccc:1111')
Traceback (most recent call last):
...
netaddr.core.AddrFormatError: failed to detect EUI version:...

>>> from netaddr import EUI
>>> MACAddress(MACAddress('d2:da:91:51:15:c7'))
MACAddress('d2:da:91:51:15:c7')
>>> MACAddress(EUI('d2:da:91:51:15:c7'))
MACAddress('d2:da:91:51:15:c7')

>>> import pickle
>>> mx = MACAddress('d2:da:91:51:33:c7')
>>> mx.__getstate__()
(231836182721479, 48, <class 'netaddr.strategy.eui48.mac_unix_expanded'>)

>>> ps = pickle.dumps(mx)
>>> pickle.loads(ps)
MACAddress('d2:da:91:51:33:c7')

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./macaddr.py"
# End:
