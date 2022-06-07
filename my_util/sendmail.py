import smtplib, os
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

def sendmail(subject, addr, content, files):
    # login for SMTP
    # Gmail 앱 비밀번호 설정을 해주어야 함
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('ckiekim@gmail.com', os.environ['GMAIL_PASSWD'])

    # message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    contents = MIMEText(f'[회신주소]: {addr}\n[내용]:\n{content}')
    msg.attach(contents)
    
    # attach files
    for file in files:
        filepath = 'static/upload/' + file.filename
        with open(filepath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=file.filename)
            msg.attach(part)
            
    # send and quit
    to_addr = 'ckiekim@naver.com'
    msg['To'] = to_addr
    smtp.sendmail('ckiekim@gmail.com', to_addr, msg.as_string())
    smtp.quit()
    return