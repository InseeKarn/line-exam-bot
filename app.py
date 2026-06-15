from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "2sVoaOcLT1r5Tf8q1Yywy+jHPRhgrqHt7HZnfepNYRs5suAsvjRSNodvdhA0+RVdBCxCkfi+cDbxiATOZsplrAkNnpNgvRHyqcVw0EP/CCd4GtZK9+HuPsRalSk3nZkgedhCefYYJdKEbhJhzAJntAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "d45378e9a13f7feffa217e9757719b64"

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(
                        text=f"Successfully get data: {user_text}"
                    )
                ]
            )
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True)