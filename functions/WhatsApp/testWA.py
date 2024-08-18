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
    for admin in os.environ.get('WHATSAPP_ADMINS').split(","):
        await send_WA(admin, message)

# Test the function
asyncio.run(send_WA_admins(f"""Hello Admins!
A new {{1}} replacement request has been made.
* *School*: {{2}}
* *Day*: {{3}}
* *Time Slot*: {{4}}
* *Replacement Date*: {{5}}
* *Old Teacher*: {{6}}
* *New Teacher*: {{7}}
* *Reason*: {{8}}"""))
