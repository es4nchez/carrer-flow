from peewee import SqliteDatabase
from flask import Flask, request
from pyngrok import ngrok
import pyperclip
from model import Company, Student, Offer, StudentOffer


db = SqliteDatabase('database.db')

def setup_db():
    db.connect()
    db.create_tables([Company, Student, Offer, StudentOffer])

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data:
        payload = data.get('payload', {})
        qa = payload.get('questions_and_answers', [{}]*3)
        Company.create(
            name=payload.get('name', ''),
            email=payload.get('email', ''),
            entreprise=qa[0].get('answer') if len(qa) > 0 else None,
            email2=qa[1].get('answer') if len(qa) > 1 else None,
            email3=qa[2].get('answer') if len(qa) > 2 else None,
        )
        Companys = Company.select()
        for item in Companys:
            print(item.name, item.email, item.entreprise, item.email2, item.email3)
    return {"message": "Webhook received"}

if __name__ == "__main__":
    setup_db()
    public_url = ngrok.connect(5000).public_url
    print(f"Webhook public URL: {public_url}")
    pyperclip.copy(public_url)
    app.run(port=5000)