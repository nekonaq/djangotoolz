#!/usr/bin/env python3
from django.db import models
from djangoexpack.models.fields_inet import IPv4RangeField as IPv4RangeFieldx


class Rx(models.Model):
    pa = IPv4RangeFieldx(null=True, blank=True)
    pb = IPv4RangeFieldx(null=False, blank=False, default=None)
    pc = IPv4RangeFieldx(null=False, blank=False, default='192.168.8.2-192.168.8.20', db_column='pcx')


"""
>>> Rx.objects.all().delete()
(...

>>> n1 = Rx()
>>> n1.pa, n1.pb, n1.pc
IPv4Range(192.168.8.2-192.168.8.20)

>>> n1.pb = '192.168.2.3'
>>> n1.pb
IPv4Range(192.168.2.3-192.168.2.3)

>>> n1.pb = '192.168.2.10-192.168.2.30'
>>> n1.pb
IPv4Range(192.168.2.10-192.168.2.30)

>>> n1.pa = None
>>> n1.pa

>>> n1.pa = ''
>>> n1.pa

>>> n1.pa, n1.pb, n1.pc
>>> n1.clean()
>>> n1.pa, n1.pb, n1.pc
>>> n1.full_clean()
>>> n1.pa, n1.pb, n1.pc
>>> n1.save()

>>> n2 = Rx(pa='10.0.2.3-10.0.2.10', pb='192.2.2.3-192.2.2.10')
>>> n2.pa, n2.pb, n2.pc

>>> n2.clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.full_clean()
>>> n2.pa, n2.pb, n2.pc
>>> n2.save()

>>> n2.pb = '10.0.0.0x'
Traceback (most recent call last):
...
django.core.exceptions.ValidationError: ["'10.0.0.0x' は IPv4 アドレスの範囲として正しくありません。"]


>>> n2x = Rx.objects.last()
>>> n2x.pa, n2x.pb, n2x.pc

>>> n2x.clean()
>>> n2x.save()

>>> n3 = Rx.objects.create(pa='10.0.2.5-10.0.2.22', pb='192.2.2.8-192.2.2.88')
>>> n3x = Rx.objects.get(id=n3.id)
>>> n3x.pa, n3x.pb, n3x.pc

>>> n3x.clean()
>>> n3x.pa, n3x.pb, n3x.pc
>>> n3x.full_clean()
>>> n3x.pa, n3x.pb, n3x.pc

>>> n3x.pa = None

>>> n3x.clean()
>>> n3x.pa, n3x.pb, n3x.pc
>>> n3x.full_clean()
>>> n3x.pa, n3x.pb, n3x.pc
>>> n3x.save()

>>> n3x.pa = '10.10.3.5'
>>> n3x.save()

>>> import pprint
>>> pprint.pprint([ (el.id, el.pa, el.pb) for el in Rx.objects.all() ])
[(1, None, IPv4Range(192.168.2.10-192.168.2.30)),
 (2, IPv4Range(10.0.2.3-10.0.2.10), IPv4Range(192.2.2.3-192.2.2.10)),
 (3, None, IPv4Range(192.2.2.8-192.2.2.88))]

>>> tl = Rx.objects.filter(pa=None)
>>> tl
<QuerySet [<Rx: Rx object (1)>, <Rx: Rx object (3)>]>

>>> tl = Rx.objects.filter(pa='')
>>> tl
<QuerySet [<Rx: Rx object (1)>, <Rx: Rx object (3)>]>

>>> from djangoexpack.types.inet import IPv4Range as IPv4RangeX
>>> n4a = Rx.objects.get(pb=IPv4RangeX('192.2.2.3-192.2.2.10'))
>>> n4a
<Rx: Rx object (2)>

>>> n4b = Rx.objects.get(pb='192.2.2.3-192.2.2.10')
>>> n4b
<Rx: Rx object (2)>
"""

if __name__ == '__main__':
    # import doctest
    # doctest.testmod(optionflags=doctest.ELLIPSIS)
    print("** No doctest available")
    import sys
    sys.exit(3)

# Local Variables:
# compile-command: "./iprange.py"
# End:
