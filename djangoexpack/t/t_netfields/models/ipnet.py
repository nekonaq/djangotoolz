#!/usr/bin/env python3
from django.db import models
from djangoexpack.models.fields_inet import IPv4NetworkField as IPv4NetworkFieldx


class Nx(models.Model):
    pa = IPv4NetworkFieldx(null=True, blank=True)
    pb = IPv4NetworkFieldx(null=False, blank=False, default=None)
    pc = IPv4NetworkFieldx(null=False, blank=False, default='192.168.8.0/24', db_column='pcx')


"""
>>> Nx.objects.all().delete()
(...

>>> n1 = Nx()
>>> n1.__dict__
{'_state': <...>, 'id': None, 'pa': None, 'pb': None, 'pc': IPv4Network('192.168.8.0/24'), 'pc_pfx': 24}

>>> n1.pa, n1.pb, n1.pc
(None, None, IPv4Network('192.168.8.0/24'))

>>> n1.pb = '192.168.2.0/24'
>>> n1.pb
IPv4Network('192.168.2.0/24')
>>> n1.pa, n1.pb, n1.pc

>>> n1.pa = None
>>> n1.pa

>>> n1.pa = ''
>>> n1.pa

>>> n1.pb = '10.0.0.0x#xx'
Traceback (most recent call last):
...
django.core.exceptions.ValidationError: ["'10.0.0.0x#xx' は IPv4 ネットワークの値として正しくありません。"]

>>> n1.clean()
>>> n1.pa, n1.pb, n1.pc
>>> n1.full_clean()
>>> n1.pa, n1.pb, n1.pc
>>> n1.save()

>>> from djangoexpack.types.inet import IPv4Network as IPv4NetworkX
>>> n1.pb = IPv4NetworkX('192.168.2.0/24')
>>> n1.pb
IPv4Network('192.168.2.0/24')

>>> n1.clean()
>>> n1.full_clean()
>>> n1.save()

>>> n2 = Nx(pa='10.0.3.5/26', pb='192.2.2.0/24')
>>> n2.__dict__
{'_state': <...>, 'id': None, 'pa': IPv4Network('10.0.3.0/26'), 'pa_pfx': 26, 'pb': IPv4Network('192.2.2.0/24'), 'pb_pfx': 24, 'pc': IPv4Network('192.168.8.0/24'), 'pc_pfx': 24}

>>> n2.pa, n2.pb, n2.pc
(IPv4Network('10.0.3.0/26'), IPv4Network('192.2.2.0/24'), IPv4Network('192.168.8.0/24'))

>>> n2.clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.full_clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.save()

>>> n2x = Nx.objects.last()
>>> n2x.__dict__
{'_state': <...>, 'id': 9, 'pa': IPv4Network('10.0.3.0/26'), 'pa_pfx': 26, 'pb': IPv4Network('192.2.2.0/24'), 'pb_pfx': 24, 'pc': IPv4Network('192.168.8.0/24'), 'pc_pfx': 24}

>>> n2x.pa, n2x.pb, n2x.pc
(IPv4Network('10.0.3.0/26'), IPv4Network('192.2.2.0/24'), IPv4Network('192.168.8.0/24'))

n2x.pb = '192.2.2.0/28'
n2x.pb
n2x.__dict__

>>> n2x.clean()
>>> n2x.pa, n2x.pb, n2x.pc
>>> n2x.full_clean()
>>> n2x.pa, n2x.pb, n2x.pc
>>> n2x.save()

>>> n3 = Nx.objects.create(pa='10.0.2.0/20', pb='192.2.2.0/24')
>>> n3x = Nx.objects.get(id=n3.id)
>>> n3x.__dict__
{'_state': <...>, 'id': 10, 'pa': IPv4Network('10.0.0.0/20'), 'pa_pfx': 20, 'pb': IPv4Network('192.2.2.0/24'), 'pb_pfx': 24, 'pc': IPv4Network('192.168.8.0/24'), 'pc_pfx': 24}

>>> n3x.pa, n3x.pb, n3x.pc
(IPv4Network('10.0.0.0/20'), IPv4Network('192.2.2.0/24'), IPv4Network('192.168.8.0/24'))

>>> n3x.pa = None
>>> n3x.pa, n3x.pb, n3x.pc
>>> n3.full_clean()
>>> n3x.pa, n3x.pb, n3x.pc
>>> n3x.save()

>>> n3x = Nx.objects.get(id=n3.id)
>>> n3x.pa, n3x.pb, n3x.pc
(None, IPv4Network('192.2.2.0/24'), IPv4Network('192.168.8.0/24'))

>>> import pprint
>>> pprint.pprint([ (el.id, el.pa, el.pb) for el in Nx.objects.all() ])
[(1, None, IPv4Network('192.168.2.0/24')),
 (2, IPv4Network('10.0.3.0/26'), IPv4Network('192.2.2.0/28')),
 (3, None, IPv4Network('192.2.2.0/24')),
 (4, None, IPv4Network('192.168.0.0/16')),
 (5, None, IPv4Network('192.168.2.0/24')),
 (6, IPv4Network('10.0.3.0/26'), IPv4Network('192.2.2.0/28')),
 (7, None, IPv4Network('192.2.2.0/24'))]

>>> tl = Nx.objects.filter(pa=None)
>>> tl
<QuerySet [<Nx: Nx object (1)>, <Nx: Nx object (3)>]>

>>> tl = Nx.objects.filter(pa='')
>>> tl
<QuerySet [<Nx: Nx object (1)>, <Nx: Nx object (3)>]>

>>> from djangoexpack.types.inet import IPv4Network as IPv4NetworkX
>>> n4a = Nx.objects.get(pa=IPv4NetworkX('10.0.3.0/32'))
>>> n4a
<Nx: Nx object (2)>

>>> n4b = Nx.objects.get(pa='10.0.3.0/26')
>>> n4b
<Nx: Nx object (2)>

"""

if __name__ == '__main__':
    # import doctest
    # doctest.testmod(optionflags=doctest.ELLIPSIS)
    print("** No doctest available")
    import sys
    sys.exit(3)

# Local Variables:
# compile-command: "./ipnet.py"
# End:
