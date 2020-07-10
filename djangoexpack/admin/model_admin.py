from functools import update_wrapper
from django.contrib.admin import helpers
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import TO_FIELD_VAR, IS_POPUP_VAR, flatten_fieldsets
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import quote, unquote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from . import signals as admin_signals


class ChangeListToInfoView(ChangeList):
    #NOTE: changelist からのリンクを info にする仕掛け
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        return reverse(
            'admin:%s_%s_info' % (
                self.opts.app_label,
                self.opts.model_name,
            ),
            args=(quote(pk),),
            current_app=self.model_admin.admin_site.name,
        )


class ModelAdminMixin_InfoView:
    def info_view(self, request, object_id, form_url='', extra_context=None):
        #NOTE: ModelAdmin._changeform_view() を info 表示用に加工したもの
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_view_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        ModelForm = self.get_form(request, obj, change=False, info=True)
        form = ModelForm(instance=obj)
        formsets, inline_instances = self._create_formsets(request, obj, change=True)

        readonly_fields = flatten_fieldsets(self.get_fieldsets(request, obj))
        adminForm = helpers.AdminForm(
            form,
            list(self.get_fieldsets(request, obj)),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj) if self.has_change_permission(request, obj) else {},
            readonly_fields,
            model_admin=self)
        media = self.media + adminForm.media

        inline_formsets = self.get_inline_formsets(request, formsets, inline_instances, obj)
        for inline_formset in inline_formsets:
            media = media + inline_formset.media

        title = _('View %s')
        context = {
            **self.admin_site.each_context(request),
            'title': title % opts.verbose_name,
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET,
            'to_field': to_field,
            'media': media,
            'inline_admin_formsets': inline_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'preserved_filters': self.get_preserved_filters(request),
        }

        context.update(extra_context or {})
        return self.render_change_form(request, context, add=False, change=False, obj=obj, form_url=form_url)

    def response_post_save_change(self, request, obj):
        # change 後に info に戻る仕掛け
        opts = self.model._meta
        if self.has_view_or_change_permission(request):
            post_url = reverse(
                'admin:{}_{}_info'.format(opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
                kwargs={'object_id': obj.pk},
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
            return HttpResponseRedirect(post_url)

        return self._response_post_save(request, obj)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['show_save_and_continue'] = False  # 「保存して編集を続ける」ボタンを非表示

        # info でインラインがあるとき「保存」ボタンになってしまうのを強制抑止
        if request.modeladmin_info:
            context['show_save'] = False
        return super().render_change_form(request, context, add=add, change=change, form_url=form_url, obj=obj)

    def get_changelist(self, request, **kwargs):
        #NOTE: changelist からのリンクを info にする仕掛け
        return ChangeListToInfoView

    def get_inline_instances(self, request, obj=None):
        # info のときだけインラインを表示
        if request.modeladmin_info:
            return super().get_inline_instances(request, obj=obj)
        return []

    def get_urls(self):
        from django.urls import path

        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns = [
            path('<path:object_id>/info/',
                 self.model_admin_view(self.info_view), name='%s_%s_info' % info),
        ] + super().get_urls()
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


class ModelAdminMixin_InfoView_Fieldset:
    # NOTE:
    # info の場合 ModelAdmin.get_fieldsets() で ModelAdmin.fieldsets ではなく
    # ModelAdmin.fieldsets_on_info を返す
    fieldsets_on_info = None

    def get_fieldsets(self, request, obj=None):
        if getattr(request, 'modeladmin_info', False):
            if self.fieldsets_on_info:
                return self.fieldsets_on_info
        return super().get_fieldsets(request, obj=obj)

    def get_form(self, request, obj=None, change=False, info=False, **kwargs):
        # info のしるしを付ける
        request.modeladmin_info = info
        return super().get_form(request, obj=obj, change=change, **kwargs)


class ModelAdminMixin_Logging:
    # 操作ログ
    def log_addition(self, request, object, message):
        admin_signals.admin_addition.send(
            sender=object.__class__,
            request=request,
            user=request.user,
            instance=object,
        )
        return super().log_addition(request, object, message)

    def log_change(self, request, object, message):
        admin_signals.admin_change.send(
            sender=object.__class__,
            request=request,
            user=request.user,
            instance=object,
        )
        return super().log_change(request, object, message)

    def log_deletion(self, request, object, object_repr):
        admin_signals.admin_deletion.send(
            sender=object.__class__,
            request=request,
            user=request.user,
            instance=object,
            instance_repr=object_repr,
        )
        return super().log_deletion(request, object, object_repr)


class ModelAdminMixin(
        ModelAdminMixin_InfoView,
        ModelAdminMixin_InfoView_Fieldset,
        ModelAdminMixin_Logging,
):
    def model_admin_view(self, view):
        #NOTE: ModelAdmin.get_urls() の中で定義している wrap() を取り出したもの。
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        wrapper.model_admin = self
        return update_wrapper(wrapper, view)

    def set_default_query(self, request, all_name, name, value):
        # query string が設定されていないときに value を付与する util メソッド。
        # ActiveFieldListFilter などといっしょに使う
        if name not in request.GET and all_name not in request.GET:
            query = request.GET.copy()
            query[name] = value
            request.GET = query
            request.META['QUERY_STRING'] = request.GET.urlencode()
