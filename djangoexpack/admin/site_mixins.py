from django.contrib import admin
from django.conf import settings


class AdminSiteTitleMixin:
    site_title = getattr(settings, 'SITEADMIN_SITE_TITLE', None) or admin.AdminSite.site_title
    site_header = getattr(settings, 'SITEADMIN_SITE_HEADER', None) or admin.AdminSite.site_header
    index_title = getattr(settings, 'SITEADMIN_SITE_INDEX_TITLE', None) or admin.AdminSite.site_header
