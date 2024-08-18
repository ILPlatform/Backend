import aiohttp
import json
import os
from dotenv import load_dotenv
import asyncio

load_dotenv("../.env")

# Send WhatsApp message
async def send_WA(recipient, message):
    async with aiohttp.ClientSession(trust_env=True) as session:
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('WHATSAPP_ACCESS_TOKEN')}",
        }
        url = f"https://graph.facebook.com/v20.0/{os.environ.get('WHATSAPP_PHONE_ID')}/messages"
        wa_data = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {
                "body": message
            }
        })
        try:
            async with session.post(url, data=wa_data, headers=headers, ssl=False) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-Type:", response.headers['content-type'])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))

# Send a message to all admins
async def send_WA_admins(message):
    if os.getenv("FUNCTIONS_EMULATOR") == "true":
        admins = os.environ.get('WHATSAPP_ADMINS_TEST').split(",")
    else:
        admins = os.environ.get('WHATSAPP_ADMINS').split(",")
    for admin in admins:
        await send_WA(admin, message)
