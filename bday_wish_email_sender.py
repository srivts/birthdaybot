import google.generativeai as genai
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email.mime.image import MIMEImage

# Configure API key
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not found in environment variables")

genai.configure(api_key=api_key)

# Create a model instance
model = genai.GenerativeModel('gemini-1.0-pro-latest')

def gemeni_generated_message(name):
    prompt = f"Generate a birthday wish for {name}. It should'nt exceed 150 words"
    response = model.generate_content(prompt)
    return response.text

# CSV file path
csv_file = "C:\\Users\\sandh\\OneDrive\\Desktop\\BIRTHDAYS.csv"
birthdays_df = pd.read_csv(csv_file)

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = 'your_email_address'
sender_password = 'password'

image_path = "C:\\Users\\sandh\\OneDrive\\Desktop\\giphy.jpg"


def send_mail(sender_email, sender_password, to_mail, subject, body, image_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if image_path and os.path.isfile(image_path):
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read(), _subtype="jpeg")  # Change _subtype as per your image type
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(img)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_mail, msg.as_string())

today = datetime.now().strftime("%d-%m-%Y")

for index, row in birthdays_df.iterrows():
    Name = row['Name ']
    birthday = datetime.strptime(row['Birthday'], '%d-%m-%Y').strftime("%d-%m-%Y")
    if birthday == today:
        to_email = row['Email']
        subject = "Happy Birthday!"
        body = gemeni_generated_message(Name)
        send_mail(sender_email, sender_password, to_email, subject, body, image_path)
        print(f"Birthday wishes sent successfully to {Name}!")
    else:
        print(f"No birthdays found for {Name} today.")









