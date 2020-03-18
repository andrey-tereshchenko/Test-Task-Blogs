from django.core.mail import send_mail
from django.template.loader import render_to_string

from test_task_blog.settings import EMAIL_HOST_USER


def send_letter(subject, context, email):
    # template_html = render_to_string('emails/' + template_name, context)
    if not type(email) is list:
        email = [email]

    send_mail(
        subject,
        # template_html,
        context,
        EMAIL_HOST_USER,
        email,
        # html_message=template_html,
    )