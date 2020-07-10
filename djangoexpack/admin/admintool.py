from django import views
from django.contrib.admin.utils import quote
from django.core.exceptions import ImproperlyConfigured
from django.db import router, transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import classonlymethod


class ModelAdminView(views.generic.TemplateView):
    template_name = None                   # サブクラスで必須
    model_admin = None                     # as_view() で設定
    success_url = None                     # サブクラスで必須

    def __init__(self, **kwargs):
        if 'model_admin' in kwargs:
            kwargs['opts'] = kwargs['model_admin'].model._meta

        super().__init__(**kwargs)

    @classonlymethod
    def as_admin_view(cls, model_admin, **initkwargs):
        return model_admin.model_admin_view(cls.as_view(model_admin=model_admin))

    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic(using=router.db_for_write(self.model_admin.model)):
            return super().dispatch(request, **kwargs)

    def response_success(self):
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.model_admin.has_change_permission(self.request, None):
            '''
            success_url = reverse(
                'admin:%s_%s_changelist' % (self.opts.app_label, self.opts.model_name),
                current_app=self.model_admin.admin_site.name,
            )
            preserved_filters = self.model_admin.get_preserved_filters(self.request)
            success_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': self.opts}, success_url
            )
            '''
            success_url = reverse(
                'admin:%s_%s_change' % (self.opts.app_label, self.opts.model_name),
                args=(quote(self.object.pk),),
                current_app=self.model_admin.admin_site.name,
            )
        else:
            success_url = reverse('admin:index', current_app=self.model_admin.admin_site.name)

        return success_url

    def is_request_permitted(self):
        """ 要求の内容が許されるものであるか
        """
        '''
        self.perms_needed = False
        self.protected = False
        '''
        pass

    def get_context_data(self, **kwargs):
        model_admin = self.model_admin
        opts = model_admin.model._meta

        context = super().get_context_data(
            **model_admin.admin_site.each_context(self.request),
            title=getattr(self, 'title', ''),
            object_name=str(opts.verbose_name),
            object=self.object,
            opts=opts,
            app_label=opts.app_label,
            media=model_admin.media,
            preserved_filters=model_admin.get_preserved_filters(self.request),
            **kwargs)
        return context

    def get_template_names(self):
        if self.template_name:
            return self.template_name.format(opts=self.opts)

        raise ImproperlyConfigured(
            "AdminToolView requires either a definition of "
            "'template_name' or an implementation of 'get_template_names()'")

'''
class ModelAdminToolViewX(ModelAdminView):

    def get_object(self):
        # 使っていない???
        import pdb; pdb.set_trace()
        obj = None
        if not self.has_permission(obj):
            raise PermissionDenied

        self.is_request_permitted(obj)
        return obj

    def has_permission(self, obj):
        """ 対象となるオブジェクトへの直接的なパーミッションがあるかどうか
        """
        return True

    def dispatch(self, request, object_id, **kwargs):
        with transaction.atomic(using=router.db_for_write(self.model_admin.model)):
            obj = self.object = self.model_admin.get_object(self.request, unquote(object_id))
            if not self.has_permission():
                raise PermissionDenied

            if obj is None:
                return self.model_admin._get_obj_does_not_exist_redirect(request, self.opts, object_id)

            self.is_request_permitted()
            return super().dispatch(request, object_id=object_id, **kwargs)


    @csrf_protect_m
    def post(self, request, **kwargs):
        if self.precheck_process():
            self.process()
            return self.response_success()

        return self.render_to_response(self.get_context_data())

    def precheck_process(self):
        if self.perms_needed:
            raise PermissionDenied

        return not self.protected

    def process(self):
        raise ImproperlyConfigured(
            "AdminToolView requires a definition of 'post()' or  'process()'")


class AdminToolFormView(AdminToolView):
    def get(self, request, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form
        return self.render_to_response(self.get_context_data())

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # return self.form_valid(form)
            return HttpResponseRedirect(self.get_success_url())

        # return self.form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))

#  TemplateView
#    .get
#    TemplateResponseMixin	//template
#      .render_to_response
#      .get_template_names
#    ContextMixin		//context
#      .get_context_data
#    View			//view
#      .as_view
#      .setup
#      .dispatch
#
#  FormView
#    TemplateResponseMixin	//template
#      .render_to_response
#      .get_template_names
#    BaseFormView		//form context view
#     FormMixin			//form context
#       .get_initial
#       .get_prefix
#       .get_form_class
#       .get_form
#       .get_form_kwargs
#       .get_success_url
#       .get_form_valid
#       .get_context_data
#       ContextMixin@
#     ProcessFormView		//view
#       .get
#       .post
#       .put
#       View@
#
#  CreateView
#    SingleObjectTemplateResponseMixin //template
#      .get_template_names
#      TemplateResponseMixin
#        .render_to_response
#        .get_template_names
#    BaseCreateView		//form.modelform context view
#      .get
#      .post
#      ModelFormMixin		//form.modelform context
#        .get_form_class
#        .get_form_kwargs
#        .get_successs_url
#        .form_valid
#        FormMixin		//form
#          .get_initilal
#          .get_prefix
#          .get_form_class
#          .get_form
#          .get_form_kwargs
#          .get_successs_url
#          .form_valid
#          .form_invalid
#          .get_context_data
#        SingleObjectMixin	//context
#          .get_object
#          .get_queryset
#          .get_slug_field
#          .get_context_object_name
#          .get_context_data
#          ContextMixin@
#      ProcessFormView		//view
#       .get
#       .post
#       .put
#       View@
#
#  UpdateView
#    SingleObjectTemplateResponseMixin@	//template
#    BaseUpdateView			//form.modelform context view
#      .get
#      .post
#      ModelFormMixin@		//form.modelform context
#      ProcessFormView@		//view
#
#  DeleteView			=> AdminToolBoxDeviceRegisterView
#    SingleObjectTemplateResponseMixin@	//template
#      .get_template_names
#      TemplateResponseMixin
#        .render_to_response
#        .get_template_names
#    BaseDeleteView
#      DeletionMixin
#        .delete
#        .post
#        .get_success_url
#      BaseDetailView		=> AdminToolView
#        .get
#        SingleObjectMixin	//context
#          .get_object
#          .get_queryset
#          .get_slug_field
#          .get_context_object_name
#          .get_context_data
#          ContextMixin		//context
#            .get_context_data
#        View
#
'''
