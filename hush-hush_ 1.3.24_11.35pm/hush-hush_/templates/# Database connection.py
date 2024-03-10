# Database connection
database_path = r"C:\Users\patna\OneDrive\Desktop\hush-hush_ 1.3.24_11.35pm\hush-hush_\developers.db"  # Change this to your database file
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Fetch candidate emails and IDs from both tables
cursor.execute("SELECT email, hush_jsd_id FROM junior_developers")
junior_candidates = cursor.fetchall()
cursor.execute("SELECT email, hush_ssd_id FROM senior_developer")
senior_candidates = cursor.fetchall()

# Email details
from_address = "h.m@gmail.com"
hosted_link = "http://example.com/coding-test"  # Replace with your actual hosted link
drive_link = "http://example.com/upload-resume"  # Replace with your actual drive link
body_template = """
Dear candidate, you are selected for hush hush coding interview. Please make sure you 
attempt the coding test before 48 hours. Otherwise the link will become invalid.<br>
The link for coding platform is: <a href='{hosted_link}'>{hosted_link}</a>.<br>
<br>
Please upload your resume in the below link:<br>
<a href='{drive_link}'>{drive_link}</a>.<br>
Note: Rename your resume name exactly same as recruitment id, mentioned in subject.
"""

# Set up the SMTP server
smtp_server = "smtp.gmail.com"  # For Gmail
smtp_port = 587  # For Gmail with STARTTLS
smtp_user = "h.m@gmail.com"  # Your email
smtp_password = "your_email_password"  # Your email password

# Sending emails to candidates
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_user, smtp_password)

for candidates, role in [(junior_candidates, 'hush_jsd_id'), (senior_candidates, 'hush_ssd_id')]:
    for email, rec_id in candidates:
        # Prepare the email
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = email
        msg['Subject'] = f"Your recruitment id is {rec_id}"
        
        # Prepare the email body
        body = body_template.format(hosted_link=hosted_link, drive_link=drive_link)
        html = MIMEText(body, "html")
        msg.attach(html)
        
        # Send the email
        server.sendmail(from_address, email, msg.as_string())
        print(f"Mail sent to {email}")

# Close server and database connection
server.quit()
connection.close()