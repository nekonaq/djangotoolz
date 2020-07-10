import enum


class ChoiceEnumMeta(enum.EnumMeta):
    def __new__(metacls, cls, bases, classdict):
        enum_class = super().__new__(metacls, cls, bases, classdict)
        enum_class.__labels__ = getattr(enum_class, '__labels__', {})
        for name, el in enum_class.__members__.items():
            el.label = enum_class.__labels__.get(el.value, el.value)
        return enum_class

    def get_choices(cls):
        return [(el, el.label) for el in cls._member_map_.values()]


class ChoiceEnum(enum.Enum, metaclass=ChoiceEnumMeta):
    def __str__(self):
        return self.value
