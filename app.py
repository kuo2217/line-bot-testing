from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('3VzM3y4xeTxks/MHGnqERZ4ZCLg6rR/7jfWFcP3R6Jszu3yN0oEOQvNzVyVZzYM2b6BHVANGWa94ccZyxF98ah95BvROknHPwiCAADDSR6dNUSa+Kygg4SdFX9myCJSKDqvyBB5ypTqsxnJF2nV5sQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b6eaa2fa4e7034798b14cce2cea1d70')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()