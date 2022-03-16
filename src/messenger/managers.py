from django.db.models import Manager, Q


class ChatManager(Manager):
    """
    Chat manager
    """

    def exclude_mine_and_invited(self, user):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "creator",
                "invited",
            )
            .exclude(Q(creator=user.id) | Q(invited=user.id))
        )

    def all_mine_and_invited(self, user):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "creator",
                "invited",
            )
            .filter(Q(creator=user.id) | Q(invited=user.id))
        )

    def all_mine(self, user):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "creator",
                "invited",
            )
            .filter(Q(creator=user.id))
        )


class MessageManager(Manager):  # noqa
    """
    Message manager
    """

    def all_mine(self, user):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "chat",
                "chat__creator",
                "chat__invited",
            )
            .filter(Q(chat__creator=user.id) | Q(chat__invited=user.id))
        )


class FileManager(Manager):  # noqa
    """
    File manager
    """

    def all_mine(self, user):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "message",
                "message__chat",
                "message__chat__creator",
                "message__chat__invited",
            )
            .filter(
                Q(message__chat__creator=user.id)
                | Q(message__chat__invited=user.id)
            )
        )
