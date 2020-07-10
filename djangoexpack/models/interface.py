class ModelInterfacePropertyBase(property):
    def __init__(self, **kwargs):
        # NOTE: kwargs は @define_model_interface() に与えた kwargs
        self.initkwargs = kwargs

    @property
    def interface_class(self):
        raise NotImplementedError(
            "property must be defined: {}.interface_class".format(self=self)
        )

    def contribute_to_class(self, model, name):
        self.name = name
        self.model = model
        setattr(model, name, self)

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        try:
            return instance.__dict__[self.name]
        except KeyError:
            pass

        # NOTE: self.initkwargs は @define_model_interface() に与えた kwargs
        interface_object = instance.__dict__[self.name] = self.interface_class(instance, **self.initkwargs)
        return interface_object

    # def __set__(self, instance, value):
    #     instance.__dict__[self.name] = value


class ModelInterfaceBase(object):
    def __init__(self, instance):
        self.instance = instance


class define_model_interface(object):
    def __init__(self, name, model, **kwargs):
        self.name = name
        self.model = model
        self.initkwargs = kwargs

    def __call__(self, klass):
        interface_klass_name = '{}_{}'.format(self.model.__name__, klass.__name__)
        interface_klass = type(interface_klass_name, (klass, ModelInterfaceBase), {})

        # class ModelInterfaceProperty(ModelInterfacePropertyBase):
        #     interface_class = interface_klass

        property_base = (ModelInterfacePropertyBase,)
        try:
            class_interface_klass = getattr(klass, 'class_interface')
            property_base = (class_interface_klass,) + property_base
        except AttributeError:
            pass

        property_klass_name = '{}_{}_property'.format(self.model.__name__, klass.__name__)
        property_klass = type(property_klass_name, property_base, {'interface_class': interface_klass})

        # self.model.add_to_class(self.name, ModelInterfaceProperty(**self.initkwargs))
        self.model.add_to_class(self.name, property_klass(**self.initkwargs))
