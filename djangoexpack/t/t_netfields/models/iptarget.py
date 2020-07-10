#!/usr/bin/env python3
from django.db import models
from djangoexpack.models.fields_inet import IPv4TargetField as IPv4TargetFieldx


class Tx(models.Model):
    pa = IPv4TargetFieldx(null=True, blank=True)
    pb = IPv4TargetFieldx(null=False, blank=False, default=None)
    pc = IPv4TargetFieldx(null=False, blank=False, default='192.168.8.8', db_column='pcx')


"""
>>> Tx.objects.all().delete()
(...

>>> n1 = Tx()
>>> n1.__dict__
{'_state': <...>, 'id': None, 'pa': None, 'pb': None, 'pc': IPv4Target('192.168.8.0/24'), 'pc_pfx': 24}

>>> n1.pa, n1.pb, n1.pc
(None, None, IPv4Target('192.168.8.8'))

>>> n1.pb = '192.168.2.0/24'
>>> n1.pb
IPv4Target('192.168.2.0/24')

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

>>> from djangoexpack.types.inet import IPv4Target as IPv4TargetX
>>> n1.pb = IPv4TargetX('192.168.2.71')
>>> n1.pb
IPv4Target('192.168.2.71')

>>> n1.clean()
>>> n1.save()

>>> n2 = Tx(pa='10.0.3.5/26', pb='192.2.2.13')
>>> n2.__dict__
{'_state': <...>, 'id': None, 'pa': IPv4Target('10.0.3.5/26'), 'pa_pfx': 26, 'pb': IPv4Target('192.2.2.13'), 'pb_pfx': 32, 'pc': IPv4Target('192.168.8.8'), 'pc_pfx': 32}

>>> n2.pa, n2.pb, n2.pc
(IPv4Target('10.0.3.5/26'), IPv4Target('192.2.2.13'), IPv4Target('192.168.8.8'))

>>> from djangoexpack.types.inet import IPv4Target as IPv4TargetX
>>> n2.pb = IPv4TargetX('192.168.2.0/28')
>>> n2.pb

>>> n2.clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.full_clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.save()

>>> n2x = Tx.objects.last()
>>> n2x.__dict__
{'_state': <...>, 'id': 2, 'pa': IPv4Target('10.0.3.5/26'), 'pa_pfx': 26, 'pb': IPv4Target('192.2.2.13'), 'pb_pfx': 32, 'pc': IPv4Target('192.168.8.8'), 'pc_pfx': 32}

>>> n2x.pa, n2x.pb, n2x.pc
(IPv4Target('10.0.3.5/26'), IPv4Target('192.2.2.13'), IPv4Target('192.168.8.8'))

>>> n2x.clean()
>>> n2x.save()

>>> n3 = Tx.objects.create(pa='10.0.2.0/20', pb='192.2.2.0/24')
>>> n3x = Tx.objects.get(id=n3.id)
>>> n3x.__dict__
{'_state': <...>, 'id': 3, 'pa': IPv4Target('10.0.2.0/20'), 'pa_pfx': 20, 'pb': IPv4Target('192.2.2.0/24'), 'pb_pfx': 24, 'pc': IPv4Target('192.168.8.8'), 'pc_pfx': 32}

>>> n3x.pa, n3x.pb, n3x.pc
(IPv4Target('10.0.2.0/20'), IPv4Target('192.2.2.0/24'), IPv4Target('192.168.8.8'))

>>> n3x.pa = None
>>> n3x.save()

>>> n3x = Tx.objects.get(id=n3.id)
>>> n3x.pa, n3x.pb, n3x.pc
(IPv4Target('10.0.2.0/20'), IPv4Target('192.2.2.0/24'), IPv4Target('192.168.8.8'))

>>> import pprint
>>> pprint.pprint([ (el.id, el.pa, el.pb) for el in Tx.objects.all() ])
[(1, None, IPv4Target('192.168.2.0/24')),
 (2, IPv4Target('10.0.3.5/26'), IPv4Target('192.168.2.0/28')),
 (3, IPv4Target('10.0.2.0/20'), IPv4Target('192.2.2.0/24'))]

>>> tl = Tx.objects.filter(pa=None)
>>> tl
<QuerySet [<Tx: Tx object (1)>, <Tx: Tx object (3)>]>

>>> tl = Tx.objects.filter(pa='')
>>> tl
<QuerySet [<Tx: Tx object (1)>, <Tx: Tx object (3)>]>

>>> from djangoexpack.types.inet import IPv4Target as IPv4TargetX
>>> n4a = Tx.objects.get(pa=IPv4TargetX('10.0.3.5/26'))
>>> n4a
<Tx: Tx object (1)>

>>> n4b = Tx.objects.get(pa='10.0.3.5/26')
>>> n4b
<Tx: Tx object (1)>

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
