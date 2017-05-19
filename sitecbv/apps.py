from __future__ import unicode_literals

from django.apps import AppConfig


class SitecbvConfig(AppConfig):
    name = 'sitecbv'

    def ready(self):
        import sitecbv.signals
