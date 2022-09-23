import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MainAPP.settings.development")

django.setup()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,

    # # WebSocket chat handler
    # "websocket": AllowedHostsOriginValidator(
    #     TokenAuthMiddlewareStack(
    #         URLRouter([
    #             url(r'^socket/app/$', AppConsumer.as_asgi()),
    #         ])
    #     )
    # ),
})
