import factory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from messenger.models import Chat, File, Message

User = get_user_model()


class TokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Token


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    token = factory.RelatedFactory(
        TokenFactory,
        factory_related_name="user",
    )
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class ChatFactory(factory.django.DjangoModelFactory):

    title = factory.Faker("sentence", nb_words=4)
    creator = factory.SubFactory(UserFactory)

    @factory.post_generation
    def invited(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for user in extracted:
                self.invited.add(user)

    class Meta:
        model = Chat


class MessageFactory(factory.django.DjangoModelFactory):

    text = factory.Faker("sentence", nb_words=10)
    sender = factory.SubFactory(UserFactory)
    chat = factory.SubFactory(ChatFactory)

    class Meta:
        model = Message


class FileFactory(factory.django.DjangoModelFactory):

    message = factory.SubFactory(MessageFactory)

    class Meta:
        model = File
