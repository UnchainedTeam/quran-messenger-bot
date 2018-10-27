import os, binascii
webhook_endpoint = (binascii.b2a_hex(os.urandom(30))).decode("utf-8")
print(webhook_endpoint)

VERIFY_TOKEN = (binascii.b2a_hex(os.urandom(25))).decode("utf-8") # put this value in bot.views.py
print(VERIFY_TOKEN)