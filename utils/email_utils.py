import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Initialize SES client here (so you can reuse it)
ses = boto3.client("ses", region_name="us-east-1")

def send_email(to_email, subject, pdf_path, filename="recommendation.pdf"):
    print(f"📤 Sending FROM: steve@omicron.studio TO: {to_email}")

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "steve@omicron.studio"
    msg['To'] = to_email

    text_part = MIMEText("Please see the attached PDF for your product packaging recommendation.", "plain")
    msg.attach(text_part)

    with open(pdf_path, 'rb') as f:
        pdf_part = MIMEApplication(f.read())
        pdf_part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(pdf_part)

    try:
        response = ses.send_raw_email(
            Source=msg['From'],
            Destinations=[to_email],
            RawMessage={'Data': msg.as_string()}
        )
        print("✅ SES send_raw_email response:", response['MessageId'])
        return response
    except Exception as e:
        print("❌ SES error:", str(e))
        raise
