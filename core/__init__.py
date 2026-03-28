from __future__ import absolute_import, unicode_literals

# Este garantirá que o app sempre seja importado quando
# o Django iniciar para que shared_task possa usar este app.
from .celery import app as celery_app

__all__ = ('celery_app',)


# default_app_config = 'virstables.core.apps.CoreConfig'