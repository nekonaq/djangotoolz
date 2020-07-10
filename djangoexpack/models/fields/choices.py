from django.core import checks
from djangoexpack.types import ChoiceEnum
from djangoexpack.models.fields.custom import CustomTypeCharField, CustomTypeIntegerField


class BaseEnumField():
    def __init__(self, *args, **kwargs):
        content_type = None
        choices = kwargs.pop('choices', None)
        # NOTE: migration から呼び出されるときは引数 type(choices) は None または list
        if isinstance(choices, type(ChoiceEnum)):
            content_type, choices = choices, choices.get_choices()
        super().__init__(*args, choices=choices, content_type=content_type, **kwargs)

    def validate(self, value, model_instance):
        if value and not isinstance(value, self.content_type):
            value = self.content_type(value)
        return super().validate(value, model_instance)

    def check(self, **kwargs):
        return [
            *self._check_choices_type(**kwargs),
            *super().check(**kwargs),
        ]

    def _check_choices_type(self):
        if not self.choices:
            return [
                checks.Error(
                    "{} must define a 'choices' attribute.".format(self.__class__.__name__),
                    obj=self,
                    id='fields.E402',
                ),
            ]
        if not isinstance(self.content_type, type(ChoiceEnum)):
            return [
                checks.Error(
                    "'choices' attribute must be an ChoiceEnum",
                    obj=self,
                    id='fields.E403',
                ),
            ]
        return []

    def _get_flatchoices(self):
        flat = []
        for choice, value in self.choices:
            # if isinstance(value, (list, tuple)):
            #     flat.extend(self._get_flatchoices(value))
            # else:
            #     flat.append((choice, value))
            #     if not isinstance(choice, str):
            #         flat.append((str(choice), value))
            flat.append((choice, value))
        return flat
    flatchoices = property(_get_flatchoices)


class CharEnumField(BaseEnumField, CustomTypeCharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)


class IntEnumField(BaseEnumField, CustomTypeIntegerField):
    pass


"""
>>> tx = Tenant(title="Example", name='example')
>>> tx.save()

>>> zx = Zone(tenant=tx, title="Demo Zone", name='demoz')
>>> zx.save()
>>> zx.status
<ZoneStatus.PLANNED: 'planned'>

>>> za = Zone.objects.first()
>>> za.id
UUID('3eec9cea-2dbd-484d-badc-9d4be3b2724e')

>>> za.status
<ZoneStatus.PLANNED: 'planned'>

>>> za.status = 'active'
>>> za.status
<ZoneStatus.ACTIVE: 'active'>

>>> za.save()

>>> sf = za._meta.get_field('status')
>>> sf.choices
[('', '---------'), ('active', '稼働中'), ('planned', '準備中'), ('retired', '撤去済み')]

"""
