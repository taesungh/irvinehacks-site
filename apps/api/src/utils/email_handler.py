from typing import Iterable, Protocol

from pydantic import EmailStr

from models.ApplicationData import Decision
from services import sendgrid_handler
from services.sendgrid_handler import ApplicationUpdatePersonalization, Template

IH_SENDER = ("apply@irvinehacks.com", "IrvineHacks 2024 Applications")
REPLY_TO_HACK_AT_UCI = ("hack@uci.edu", "Hack at UCI")

DECISION_TEMPLATES = {
    Decision.ACCEPTED: Template.ACCEPTED_EMAIL,
    Decision.REJECTED: Template.REJECTED_EMAIL,
    Decision.WAITLISTED: Template.WAITLISTED_EMAIL,
}


class ContactInfo(Protocol):
    first_name: str
    last_name: str


async def send_application_confirmation_email(
    email: EmailStr, user: ContactInfo
) -> None:
    """Send a confirmation email after a user submits an application.
    Will propagate exceptions from SendGrid."""
    await sendgrid_handler.send_email(
        Template.CONFIRMATION_EMAIL,
        IH_SENDER,
        {
            "email": email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        reply_to=REPLY_TO_HACK_AT_UCI,
    )


async def send_guest_login_email(email: EmailStr, passphrase: str) -> None:
    """Email login passphrase to guest."""
    await sendgrid_handler.send_email(
        Template.GUEST_TOKEN,
        IH_SENDER,
        {
            "email": email,
            "passphrase": passphrase,
        },
        reply_to=REPLY_TO_HACK_AT_UCI,
    )


async def send_decision_email(
    applicant_batch: Iterable[tuple[str, EmailStr]], decision: Decision
) -> None:
    """Send a specific decision email to a group of applicants."""
    personalizations = [
        ApplicationUpdatePersonalization(email=email, first_name=first_name)
        for first_name, email in applicant_batch
    ]

    template = DECISION_TEMPLATES[decision]
    await sendgrid_handler.send_email(template, IH_SENDER, personalizations, True)
