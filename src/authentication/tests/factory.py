import factory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

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
