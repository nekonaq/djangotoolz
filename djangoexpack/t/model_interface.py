from mns.models import define_model_interface
from mnsapp.boxdevice.models import BoxDevice


@define_model_interface('test', BoxDevice)
class SampleInterface(object):
    def meex(self):
        return 'VAR:{}'.format(str(self.instance))


'''
## Activate:
>>> import mns.t.model_interface

>>> bx = BoxDevice.objects.first()
>>> bx.test
<mns.models.model_interface.BoxDevice_SampleInterface object at ...>

>>> bx.test = 'moo'
Traceback (most recent call last):
...
AttributeError: can't set attribute

>>> bx.__dict__['test']
<mns.models.model_interface.BoxDevice_SampleInterface object at ...>

>>> bx.test.meex()
'VAR:8447-126'

>>> bx.test.instance
<BoxDevice: 8447-126>

'''
