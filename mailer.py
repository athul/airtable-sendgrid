import os
from airtable import Airtable
import argparse
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import markdown2 as md


def get_emails(base, table, api_key):
    airtable = Airtable(base, table, api_key=api_key)
    airtable_emails = airtable.get_all(fields='Email')
    emails = []
    for email in airtable_emails:
        emails.append(email['fields']['Email'])
    return emails


def render_markdown(file):
    return md.markdown(file.read(), extras=["metadata"])


def send_emails(from_addr, subject, content, email_list):
    client = SendGridAPIClient()

    unsubscribe = f"<a href='mailto:{from_addr}?subject=Unsubscribe'>Unsubscribe</a>"
    for i, email in enumerate(email_list):
        message = Mail(subject=subject, html_content=f"{content}\n{unsubscribe}", from_email=from_addr, to_emails=[email])
        try:
            resp = client.send(message)
            print(f"{i+1} emails sent")
        except Exception as exc:
            print(f"Could not send email to {email} due {str(exc)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--content', required=True, help="A markdown file for contents of the Email", type=argparse.FileType("r"))
    args = parser.parse_args()

    load_dotenv()

    base_key = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")
    from_addr = os.getenv("FROM_ADDRESS")
    api_key = os.getenv("AIRTABLE_API_KEY")

    md_content = render_markdown(args.content)
    subject = md_content.metadata.get("subject")
    if subject != None:
        emails = get_emails(base=base_key, table=table_name, api_key=api_key)
        send_emails(from_addr=from_addr, subject=subject, content=md_content, email_list=emails)
    else:
        print("Subject not found in the Markdown file")
