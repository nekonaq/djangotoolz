import netaddr

# for export
from netaddr.core import (                 # noqa: F401
    AddrFormatError,
    NotRegisteredError,
)


class IPv4Address(netaddr.IPAddress):
    def __init__(self, addr):
        super().__init__(addr, version=4)


class IPv4Range(netaddr.IPRange):
    def __init__(self, addr):
        if isinstance(addr, (self.__class__, netaddr.IPRange)):
            val1, val2 = (addr._start, addr._end)
        elif isinstance(addr, str) and '-' in addr:
            val1, val2 = addr.split('-', 1)
        else:
            val1 = val2 = addr

        val1 = IPv4Address(val1)
        val2 = IPv4Address(val2)
        if val1 > val2:
            val1, val2 = val2, val1
        self._start, self._end = val1, val2
        self._module = val1._module
        # super().__init__() で行っている処理はこれですべてなので super() は呼び出さない。
        pass

    def __repr__(self):
        return '{}({}-{})'.format(
            self.__class__.__name__,
            self._start,
            self._end,
        )

    @classmethod
    def from_range(cls, start, end):
        instance = super().__new__(cls)
        super().__init__(instance, start, end)
        return instance

    def cidrs(self):
        return [IPv4Network(addr) for addr in super().cidrs()]


class IPv4Network(netaddr.IPNetwork):
    def __init__(self, addr, version=None):
        version = version or 4
        if isinstance(addr, int):
            addr = IPv4Address(addr)

        super().__init__(addr, version=version)
        self.value = self.network.value    # ネットワークアドレス補正

    @property
    def ip(self):
        return IPv4Address(super().ip)

    @property
    def network(self):
        return IPv4Address(super().network)

    @property
    def broadcast(self):
        value = super().broadcast
        return None if value is None else IPv4Address(value)

    @property
    def netmask(self):
        return IPv4Address(super().netmask)

    @property
    def hostmask(self):
        return IPv4Address(super().hostmask)

    @property
    def cidr(self):
        return self.__class__(super().cidr)

    def iter_hosts(self):
        for addr in super().iter_hosts():
            yield IPv4Address(addr)


class IPv4Target(netaddr.IPNetwork):
    def __init__(self, addr):
        if isinstance(addr, str) and addr.find('/') < 0:
            addr = '{}/32'.format(addr)
        elif isinstance(addr, int):
            addr = IPv4Address(addr)
        super().__init__(addr)

    def __str__(self):
        addr = self._module.int_to_str(self._value)
        return addr if self.prefixlen == 32 else "%s/%s" % (addr, self.prefixlen)


class MACAddress(netaddr.EUI):
    def __init__(self, addr, version=None, dialect=None):
        dialect = dialect or netaddr.mac_unix_expanded
        if isinstance(addr, netaddr.EUI):
            addr = int(addr)
        super().__init__(addr, version=version, dialect=dialect)

    def __repr__(self):
        return "%s('%s')" % (self.__class__.__name__, self)

    @property
    def oui_org(self):
        try:
            return self.info['OUI']['org']
        except NotRegisteredError:
            return None
