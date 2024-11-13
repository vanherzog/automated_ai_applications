import logging
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
import os
import re
import email_credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApplicationSender:
    def __init__(self):
        print(f"ZZZZZZZ {email_credentials.SMTP_USERNAME}")
        # These would typically come from environment variables
        self.smtp_server = email_credentials.SMTP_SERVER
        self.smtp_port = email_credentials.SMTP_PORT
        self.smtp_username = email_credentials.SMTP_USERNAME
        self.smtp_password = email_credentials.SMTP_PASSWORD
        self.sender_email = email_credentials.SENDER_EMAIL

        # Create applications directory if it doesn't exist
        self.applications_dir = "sent_applications"
        os.makedirs(self.applications_dir, exist_ok=True)

    def save_application(self, job_id: int, application_text: str) -> bool:
        """Save the application to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.applications_dir}/application_{job_id}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Job ID: {job_id}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write("Application:\n")
                f.write(application_text)

            logger.info(f"Application saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving application: {str(e)}")
            return False

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email from text using regex"""
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_regex, text)
        return match.group(0) if match else None

    def send_email(self, job_id: int, application_text: str, job_description: str) -> bool:
        """Send the application via email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email

            # Extract email from job description or use default
            recipient_email = self.extract_email(job_description) or "recruiter@example.com"
            logger.info(f"Sending email to {recipient_email}")
            msg['To'] = recipient_email

            msg['Subject'] = f"Job Application - ID: {job_id}"

            body = application_text
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Application for job {job_id} sent successfully to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

    def process_application(self, job_id: int, application_text: str, job_description: str) -> dict:
        """Process the application by saving and optionally sending it"""
        result = {
            "success": False,
            "message": "",
            "saved": False,
            "sent": False
        }

        # Always try to save the application
        save_success = self.save_application(job_id, application_text)
        result["saved"] = save_success

        # Only try to send email if SMTP credentials are configured
        if all([self.smtp_username, self.smtp_password, self.sender_email]):
            send_success = self.send_email(job_id, application_text, job_description)
            result["sent"] = send_success
        else:
            print("YYYY SMTP credentials not configured")

        # Determine overall success
        if save_success:
            result["success"] = True
            result["message"] = "Application processed successfully"
        else:
            result["message"] = "Failed to process application"

        return result


def send_application(job_id: int, application_text: str, job_description: str) -> dict:
    """Main function to handle application sending"""
    sender = ApplicationSender()
    return sender.process_application(job_id, application_text, job_description)


if __name__ == "__main__":
    # Example usage
    test_job_id = 1
    test_application = "This is a test application"
    test_job_description = "Send your application to test@example.com"
    result = send_application(test_job_id, test_application, test_job_description)
    print(json.dumps(result, indent=2))