import json

import random
import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from bot.models import Message
from .logic_constants import LOGIC_RESPONSES
from .logic import answer

from misba7.settings import FB_ENDPOINT, PAGE_ACCESS_TOKEN, VERIFY_TOKEN


def parse_and_send_fb_message(fbid, received_message):
    message, created = Message.objects.get_or_create(
        text=received_message
    )
    message.frequency += 1
    message.save()

    normalized = received_message.lower().strip()
    if normalized in LOGIC_RESPONSES:
        msg = {"text": random.choice(LOGIC_RESPONSES[normalized])}
    else:
        results = answer(received_message)
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "elements": [
                        {
                            "title": result['title'],
                            "subtitle": result['body'],

                        } for result in results
                    ],
                    "buttons": []
                }
            }
        }

    if msg is not None:
        endpoint = "{}/me/messages?access_token={}".format(FB_ENDPOINT, PAGE_ACCESS_TOKEN)
        response_msg = json.dumps(

            {
                "recipient": {"id": fbid},
                "message": msg}
        )
        status = requests.post(
            endpoint,
            headers={"Content-Type": "application/json"},
            data=response_msg)
        print(status.json())
        return status.json()
    return None


class FacebookWebhookView(View):
    @method_decorator(csrf_exempt)  # required
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookWebhookView, self).dispatch(request, *args, **kwargs)  # python3.6+ syntax

    '''
    hub.mode
    hub.verify_token
    hub.challenge
    Are all from facebook. We'll discuss soon.
    '''

    def get(self, request, *args, **kwargs):
        hub_mode = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status_code=403)
        return HttpResponse(hub_challenge)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(request.body.decode('utf-8'))
        # print(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    fb_user_id = message['sender']['id']  # sweet!
                    fb_user_txt = message['message'].get('text')
                    if fb_user_txt:
                        parse_and_send_fb_message(fb_user_id, fb_user_txt)
        return HttpResponse("Success", status=200)
