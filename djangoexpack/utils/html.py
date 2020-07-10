import string
from django.utils.html import format_html


def format_html_string(text, context={}):
    return format_html(string.Template(text).substitute(context))
