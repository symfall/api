from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def send_email(
    recipient_list=None,
    activate_url=None,
):
    """
    Doo for send email
    """
    subject = "Thank you for your registration!"
    message = "it  means a world to us."
    from_email = settings.EMAIL_HOST_USER

    template = get_template("activation.html")

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=template.render(
            context={
                "activate_url": activate_url,
            }
        ),
    )
