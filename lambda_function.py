import logging
import json
import random

#import spreadsheet

import boto3
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import SimpleCard
from ask_sdk_dynamodb.partition_keygen import user_id_partition_keygen as uid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

MASTER_FILE = "master.txt"

def parseFile(min_price = 0.0, max_price = float('inf'), index = 0):
    import re
    items = []
    with open(MASTER_FILE) as f:
        for line in f.readlines():
            tokens = re.split(r'\t+', line)
            if len(tokens) < 3:
            	continue
            price = re.findall('\d+\.\d+', tokens[2])
            items.append((tokens[0], tokens[1], price))
    idx = int(index) % len(items)
    while idx < len(items):
        if len(items[idx][2]) == 0:
            price = [9223372036854775807, 0]
        elif len(items[idx][2]) == 1:
            price = [items[idx][2][0], 0]
        if price[0] > min_price and price[1] < max_price:
            return items[idx]
        idx += 1
    return None

def getLine():
    with open(MASTER_FILE) as f:
        lines = f.readlines()
        return lines[random.randrange(len(f))].split('\t')

class SearchIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "SearchIntent")

    def handle(self, handler_input):

        try:
            lower_bound = float(handler_input.request_envelope.request.intent.slots.lower_bound)
        except AttributeError:
            lower_bound = float(0)
        try:
            upper_bound = float(handler_input.request_envelope.request.intent.slots.upper_bound)
        except AttributeError:
            upper_bound = float('inf')

        speech_text = "Here's a product I found: "

        item = parseFile(index=random.randrange(1000))
        speech_text += item[1]

        #get item and add to speech text
        

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Search Intent", speech_text)).set_should_end_session(
            True).set_should_end_session(False)
        return handler_input.response_builder.response

class GetNextItemIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "GetNextItemIntent")

    def handle(self, handler_input):
        speech_text = "Here's a product I found: "
        #TODO
        #get item and add to speech text
        #update database

        item = parseFile(index=random.randrange(1000))
        speech_text += item[1]

        user_id = uid(handler_input.request_envelope)
        #data = spreadsheet.read(user_id)[0]
        #pos = data["pos_in_file"]
        #lower = data["price_lower"]
        #upper = data["price_upper"]

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Window Shopping", speech_text)).set_should_end_session(False)
        
        return handler_input.response_builder.response

class AddItemIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "GetNextItemIntent")

    def handle(self, handler_input):
        speech_text = "Okay, I've added that item to your cart"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Window Shopping", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         return handler_input.request_envelope.request.object_type == "LaunchRequest"

     def handle(self, handler_input):
         speech_text = "Give me a price range"

         handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("WindowShopping", speech_text)).set_should_end_session(
            False)
         return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent")

    def handle(self, handler_input):
        speech_text = "You can search for interesting items."

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Window Shopping", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
            and (handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent"
                 or handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent"))

    def handle(self, handler_input):
        speech_text = "Cancelling"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Window Shopping", speech_text))
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.object_type == "SessionEndedRequest"

    def handle(self, handler_input):
        #TODO
        #any cleanup logic goes here

        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.request_handlers.extend([
    LaunchRequestHandler(),
    SearchIntentHandler(),
    GetNextItemIntentHandler(),
    AddItemIntentHandler(),
    HelpIntentHandler(),
    CancelAndStopIntentHandler(),
    SessionEndedRequestHandler()])

sb.add_exception_handler(AllExceptionHandler())

lambda_handler = sb.lambda_handler()
