import logging, os, re
import azure.functions as func
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

PCIEX_BASE_ADDRESS = int('0xc0000000', 16)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # get x-line-signature header value
    signature = req.headers['x-line-signature']

    # get request body as text
    body = req.get_body().decode("utf-8")
    logging.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)

    return func.HttpResponse('OK')

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    # userInput = 'B00D14F00' as example
    userInput = event.message.text

    pattern = re.compile(r"^b\d{2}d\d{2}f\d{2}")
    pattern2 = re.compile(r"\d{2}.\d{2}.\d{2}")
    if pattern.match(userInput.lower()):
        Bus = int(userInput[1:3], 16)
        Dev = int(userInput[4:6], 16)
        Fun = int(userInput[7:9], 16)
        result = PCIEX_BASE_ADDRESS + (Bus << 20) + (Dev << 15) + (Fun << 12)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(hex(result)))
        )
    elif pattern2.match(userInput.lower()):
        Bus = int(userInput[0:2], 16)
        Dev = int(userInput[3:5], 16)
        Fun = int(userInput[6:8], 16)
        result = PCIEX_BASE_ADDRESS + (Bus << 20) + (Dev << 15) + (Fun << 12)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(hex(result)))
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("Please use BxxDxxFxx as input format"))