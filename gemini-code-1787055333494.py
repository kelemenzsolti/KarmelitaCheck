import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playwright.sync_api import sync_playwright

URL = "https://szabadkarmelita.jegy.hu/"

# Adatok kiolvasása a GitHub titkosítóból (Secrets)
SENDER_EMAIL = os.environ.get("MAIL_USER")
APP_PASSWORD = os.environ.get("MAIL_PASS")
RECEIVER_EMAIL = os.environ.get("MAIL_TO")

def send_email_notification():
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "FIGYELEM: Megnyílt a Karmelita jegyvásárlás!"

        body = "A szabadkarmelita.jegy.hu oldalon eltűnt a lezárásra utaló szöveg. Lehet, hogy jegyet lehet venni!"
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("E-mail sikeresen elküldve!")
    except Exception as e:
        print(f"Hiba az e-mail küldésekor: {e}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_load_state("networkidle")
        content = page.content()
        
        if "regisztráció lezárult" not in content.lower():
            print("Lehet, hogy megnyílt a jegyvásárlás!")
            send_email_notification()
        else:
            print("Még mindig zárva a regisztráció.")
            
        browser.close()

if __name__ == "__main__":
    main()