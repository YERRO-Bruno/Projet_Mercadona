from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
# from mercadona.views import recipient_email
# global recipient_email


class CustomEmailBackend(EmailBackend):

    def send_messages(self, messages):

        for message in messages:
            if settings.DEBUG:
                message.subject = "{subject} [{to}]".format(
                    subject=message.subject,
                    to=', '.join(message.to)
                )
            message.to = message.to
            print(message.to)
        return super(CustomEmailBackend, self).send_messages(messages)
