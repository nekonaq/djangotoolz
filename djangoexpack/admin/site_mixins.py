from django.contrib import admin
from django.conf import settings


class AdminSiteTitleMixin:
    site_title = getattr(settings, 'SITEADMIN_SITE_TITLE', None) or admin.AdminSite.site_title
    site_header = getattr(settings, 'SITEADMIN_SITE_HEADER', None) or admin.AdminSite.site_header
    index_title = getattr(settings, 'SITEADMIN_SITE_INDEX_TITLE', None) or admin.AdminSite.site_header


class AdminSiteAppOrderingMixin:
    def get_app_ordering(self, app_label, object_name=None):
        """AdminSite 上の (app, model) の表示順を settings から取得
        """
        try:
            app_ordering = self._app_ordering
        except AttributeError:
            app_ordering_conf = getattr(settings, 'ADMIN_APP_ORDERING', {})

            app_ordering = {
                (name, None): num
                for num, name in enumerate(app_ordering_conf.keys(), start=1)
            }

            for app_label, model_ordering in app_ordering_conf.items():
                app_ordering.update({
                    (app_label, name): num
                    for num, name in enumerate(model_ordering or [], start=1)
                })
            self._app_ordering = app_ordering

        return app_ordering.get((app_label, object_name), 1000)

    #// overrides: django.contrib.admin.AdminSite
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)

        app_list = sorted(
            app_dict.values(),
            key=lambda x: (self.get_app_ordering(x['app_label']), x['name'].lower()),
        )

        for app in app_list:
            app['models'].sort(key=lambda x: (self.get_app_ordering(app['app_label'], x['object_name']), x['name']))

        return app_list
