#!/usr/bin/env python3
from django.db import models
from djangoexpack.models.fields_inet import MACAddressField as MACAddressFieldx


class Mx(models.Model):
    pa = MACAddressFieldx(null=True, blank=True)
    pb = MACAddressFieldx(null=False, blank=False, default=None)
    pc = MACAddressFieldx(null=False, blank=False, default='d2:da:91:51:15:c7', db_column='pcx')


"""
>>> Mx.objects.all().delete()

>>> m1 = Mx()
>>> m1.pa
>>> m1.pb
>>> m1.pc
MACAddress('d2:da:91:51:15:c7')

>>> m1.pb = '02:42:36:c6:d2:d4'
>>> m1.pb
MACAddress('02:42:36:c6:d2:d4')

>>> m1.pa = None
>>> m1.pa

>>> m1.pa = ''
>>> m1.pa

>>> m1.clean()
>>> m1.save()

>>> m2 = Mx(pa='C0-B6-F9-7D-77-8D', pb='C0-B6-F9-7D-77-91')
>>> m2.pa
MACAddress('c0:b6:f9:7d:77:8d')
>>> m2.pb
MACAddress('c0:b6:f9:7d:77:91')
>>> m2.pc
MACAddress('d2:da:91:51:15:c7')
>>> m2.clean()
>>> m2.save()

>>> m2.pc = 'aa:bbx:cc'
Traceback (most recent call last):
...
django.core.exceptions.ValidationError: ["'aa:bbx:cc' は MAC アドレスとして無効な値です。"]


>>> [ (el.id, el.pa, el.pb) for el in Mx.objects.all() ]
[(1, None, MACAddress('02:42:36:c6:d2:d4')), (2, MACAddress('c0:b6:f9:7d:77:8d'), MACAddress('c0:b6:f9:7d:77:91'))]

>>> tl = Mx.objects.filter(pa=None)
>>> tl
<QuerySet [<Mx: Mx object (1)>]>

>>> tl = Mx.objects.filter(pa='')
>>> tl
<QuerySet [<Mx: Mx object (1)>]>

>>> from djangoexpack.types.inet import MACAddress as MACAddressX
>>> m4a = Mx.objects.get(pb=MACAddressX('02:42:36:c6:d2:d4'))
>>> m4a
<Mx: Mx object (1)>

>>> m4a = Mx.objects.get(pb='02:42:36:c6:d2:d4')
>>> m4a
<Mx: Mx object (1)>

"""

if __name__ == '__main__':
    # import doctest
    # doctest.testmod(optionflags=doctest.ELLIPSIS)
    print("** No doctest available")
    import sys
    sys.exit(3)

# Local Variables:
# compile-command: "./macaddr.py"
# End:
