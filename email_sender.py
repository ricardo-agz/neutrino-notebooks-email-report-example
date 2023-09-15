import os
import requests
from dotenv import load_dotenv
from typing import List, Optional
from jinja2 import Environment, FileSystemLoader


load_dotenv()


class EmailSender:
    """
    A class that provides functionality to send emails using Mailgun.

    Attributes:
        mailgun_domain (str): The Mailgun domain to use for sending emails.
        mailgun_api_key (str): The Mailgun API key to use for authentication.
        templates_dir (str): The path to the directory containing email templates.
    """

    def __init__(
        self,
        templates_dir=None,
        mailgun_domain: Optional[str] = None,
        mailgun_api_key: Optional[str] = None,
    ):
        self.mailgun_domain = mailgun_domain or os.environ.get('MAILGUN_DOMAIN')
        self.mailgun_api_key = mailgun_api_key or os.environ.get('MAILGUN_API_KEY')

        if not self.mailgun_domain or not self.mailgun_api_key:
            raise ValueError("Undefined Mailgun domain or API key")

        # Update the templates directory to use an absolute path
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = templates_dir or os.path.join(base_path, 'templates')

        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

    def send_email(
        self,
        source: str,
        recipients: List[str],
        subject: str,
        template_name: Optional[str] = None,
        context: Optional[dict] = None,
        body: Optional[str] = None,
    ):
        """
        Sends an email using the configured email provider.

        Args:
            source (str): The email address the email should be sent from.
            recipients (list[str]): A list of email addresses of the recipients.
            subject (str): The subject of the email.
            template_name (str, optional): The name of the email template to use.
            context (dict, optional): The context to use when rendering the email template.
            body (str, optional): The body of the email if no template is provided.

        Returns:
            None
        """
        if not template_name and not body:
            raise ValueError("Either a template_name or a body must be provided")

        if template_name and context is not None:
            body = self._render_template(template_name, context)

        self._send_message(recipients, subject, body, source)

    def _render_template(self, template_name: str, context: dict) -> str:
        """
        Renders an email template using the specified context.

        Args:
            template_name (str): The name of the email template to use.
            context (dict): The context to use when rendering the email template.

        Returns:
            str: The rendered email message.
        """
        template = self.env.get_template(template_name)
        return template.render(context)

    def _send_message(self, recipients: list[str], subject: str, body: str, source: str) -> None:
        """
        Sends an email message using the configured email provider.

        Args:
            recipients (list[str]): A list of email addresses of the recipients.
            subject (str): The subject of the email.
            body (str): The body of the email.
            source (str): The email address the email should be sent from.

        Returns:
            None
        """
        requests.post(
            f"https://api.mailgun.net/v3/{self.mailgun_domain}/messages",
            auth=("api", self.mailgun_api_key),
            data={
                "from": source,
                "to": recipients,
                "subject": subject,
                "html": body,
            },
        )


email_sender = EmailSender()