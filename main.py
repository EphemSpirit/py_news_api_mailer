from dotenv import load_dotenv
from email.message import EmailMessage
import requests
import os
import smtplib

load_dotenv()

topic = input("What topic would you like? ")

REQUEST_URL = f"https://newsapi.org/v2/everything?q={topic.replace(" ", "_")}&from=2026-03-23&sortBy=publishedAt&apiKey={os.getenv("NEWS_API_KEY")}&language=en"

def get_news_content():
    res = requests.get(
        REQUEST_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    content = res.json()
    return content["articles"][:20]

def format_articles(content):
    return "\n\n".join(
        f"{article['title']}\n{article['description']}\n{article['url']}"
        for article in content
        if article["title"] and article["description"]
    )

def send_news_email(content):
    body = format_articles(content)

    msg = EmailMessage()
    msg["Subject"] = "Daily News"
    msg["From"] = os.getenv("GMAIL_ADDRESS")
    msg["To"] = os.getenv("GMAIL_ADDRESS")

    msg.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), port=587) as connection:
        connection.starttls()
        connection.login(user=os.getenv("GMAIL_ADDRESS"), password=os.getenv("GMAIL_APP_PASSWORD"))
        connection.send_message(msg)


if __name__ == "__main__":
    news_content = get_news_content()
    send_news_email(news_content)