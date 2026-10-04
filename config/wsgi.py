import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Wasmer exige une variable publique `app`.
app = get_wsgi_application()
application = app  # alias classique pour les autres serveurs (gunicorn, etc.)
