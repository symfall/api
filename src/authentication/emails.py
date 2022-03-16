from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template


def get_render_template(template_name, context):
    email_txt = get_template(f"{template_name}.txt")
    email_html = get_template(f"{template_name}.html")

    email_txt_content = email_txt.render(context)
    email_html_content = email_html.render(context)

    return email_txt_content, email_html_content


def send_activation_email(
    recipient_list=None,
    activate_url=None,
):
    """
    Send activation email with html template to recipient_list
    """
    subject = "Thank you for your registration!"
    from_email = settings.EMAIL_HOST_USER

    txt_template, html_template = get_render_template(
        template_name="activation",
        context={
            "activate_url": activate_url,
            "project_name": settings.PROJECT_NAME,
        },
    )

    send_mail(
        from_email=from_email,
        recipient_list=recipient_list,
        subject=subject,
        message=txt_template,
        html_message=html_template,
    )
