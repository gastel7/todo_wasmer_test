import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

_django_app = get_wsgi_application()


def _clean_headers(wsgi_app):
    """Django émet 'Set-Cookie' avec un espace en tête (' csrftoken=...').
    Les WSGI classiques le tolèrent, mais uvicorn + h11 (utilisés par Wasmer) le
    refusent : 'Illegal header value' -> erreur 500 sur toute page qui pose un cookie.
    On nettoie donc les valeurs d'en-têtes avant de les passer à uvicorn."""

    def middleware(environ, start_response):
        def _start_response(status, headers, exc_info=None):
            headers = [(name, value.strip()) for name, value in headers]
            return start_response(status, headers, exc_info)

        return wsgi_app(environ, _start_response)

    return middleware


# Wasmer exige une variable publique `app`.
app = _clean_headers(_django_app)
application = app  # alias classique pour les autres serveurs