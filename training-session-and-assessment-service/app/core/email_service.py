from app.core.config import settings
from app.schemas import schemas_user
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="app/templates",
)


def send_email_background(
    background_tasks: BackgroundTasks, subject: str, email: schemas_user.EmailSchema
):
    message = MessageSchema(
        subject=subject,
        recipients=email.get("email"),
        template_body=email.get("body"),
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    background_tasks.add_task(
        fm.send_message, message, template_name="welcome-email.html"
    )
