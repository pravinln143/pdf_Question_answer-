import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from pdf_app import consumers  # Your app consumers for WebSockets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            os.path("ws/ask_question/", consumers.QuestionConsumer.as_asgi()),
        ])
    ),
})
