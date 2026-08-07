from channels.routing import ProtocolTypeRouter, URLRouter
import vis_go_app.routing 
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack
  
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SessionMiddlewareStack(
        URLRouter(
            vis_go_app.routing.websocket_urlpatterns
        )
    ),
})