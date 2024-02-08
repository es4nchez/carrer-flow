from flask import Flask, request
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)  # affiche les données du webhook
    return {"message": "Webhook received"}

if __name__ == "__main__":
    public_url = ngrok.connect(5000).public_url
    print(f"Webhook public URL: {public_url}")
    app.run(port=5000)