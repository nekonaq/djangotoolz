#!/usr/bin/env python3
from django.db import models
from djangoexpack.models.fields_inet import IPv4AddressField as IPv4AddressFieldx


class Ax(models.Model):
    pa = IPv4AddressFieldx(null=True, blank=True)
    pb = IPv4AddressFieldx(null=False, blank=False, default=None)
    pc = IPv4AddressFieldx(null=False, blank=False, default='192.168.8.2', db_column='pcx')


"""
>>> Ax.objects.all().delete()
(...

>>> n1 = Ax()
>>> n1.pa
>>> n1.pb
>>> n1.pc
IPv4Address('192.168.8.2')

>>> n1.pb = '192.168.2.3'
>>> n1.pb
IPv4Address('192.168.2.3')

>>> n1.pa = None
>>> n1.pa

>>> n1.pa = ''
>>> n1.pa

>>> n1.clean()
>>> n1.save()

>>> n2 = Ax(pa='10.0.2.3', pb='192.2.2.2')
>>> n2.pa
IPv4Address('10.0.2.3')
>>> n2.pb
IPv4Address('192.2.2.2')
>>> n2.pc
IPv4Address('192.168.8.2')
>>> n2.clean()
>>> n2.save()

>>> n2x = Ax.objects.last()
>>> n2x.pa
IPv4Address('10.0.2.3')
>>> n2x.pb
IPv4Address('192.2.2.2')
>>> n2x.pc
IPv4Address('192.168.8.2')

>>> n2x.pb = '10.0.0.0x'
Traceback (most recent call last):
...
django.core.exceptions.ValidationError: ["'10.0.0.0x' は有効な IPv4 アドレスではありません。"]

>>> n2x.clean()
>>> n2x.save()

>>> n3 = Ax.objects.create(pa='10.0.2.5', pb='192.2.2.8')
>>> n3x = Ax.objects.get(id=n3.id)
>>> n3x.pa
IPv4Address('10.0.2.5')
>>> n3x.pb
IPv4Address('192.2.2.8')
>>> n3x.pc
IPv4Address('192.168.8.2')

>>> n3x.pa = None
>>> n3x.save()

>>> n3x.pa = '10.10.3.5'
>>> n3x.save()

>>> from djangoexpack.types.inet import IPv4Address as IPv4AddressX

>>> [ (el.id, el.pa, el.pb) for el in Ax.objects.all() ]
[(1, None, IPv4Address('192.168.2.3')), (2, IPv4Address('10.0.2.3'), IPv4Address('192.2.2.2')), (3, IPv4Address('10.10.3.5'), IPv4Address('192.2.2.8'))]
>>> tl = Ax.objects.filter(pa=None)
>>> tl
<QuerySet [<Ax: Ax object (1)>]>

>>> tl = Ax.objects.filter(pa='')
>>> tl
<QuerySet [<Ax: Ax object (1)>]>

>>> from djangoexpack.types.inet import IPv4Address as IPv4AddressX
>>> n4a = Ax.objects.get(pb=IPv4AddressX('192.2.2.8'))
>>> n4a
<Ax: Ax object (3)>

>>> n4b = Ax.objects.get(pb='192.2.2.2')
>>> n4b
<Ax: Ax object (2)>

"""

if __name__ == '__main__':
    # import doctest
    # doctest.testmod(optionflags=doctest.ELLIPSIS)
    print("** No doctest available")
    import sys
    sys.exit(3)

# Local Variables:
# compile-command: "./ipaddr.py"
# End:
