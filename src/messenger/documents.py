from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from messenger.models import Chat, File, Message


@registry.register_document
class ChatDocument(Document):
    class Index:
        name = "chats"

    class Django:
        model = Chat
        fields = ["id", "name", "users"]


@registry.register_document
class MessageDocument(Document):
    class Index:
        name = "messages"

    class Django:
        model = Message
        fields = ["id", "text", "chat", "created"]


@registry.register_document
class FileDocument(Document):
    class Index:
        name = "files"

    class Django:
        model = File
        fields = ["id", "file", "chat", "created"]
