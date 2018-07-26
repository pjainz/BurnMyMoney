from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import SimpleCard

class BurnIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "BurnIntent")

    def handle(self, handler_input):
        speech_text = "Burn Intent"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Burn Intent", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         return handler_input.request_envelope.request.object_type == "LaunchRequest"

     def handle(self, handler_input):
         speech_text = "Welcome to burn my moeny!"

         handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Burn My Money", speech_text)).set_should_end_session(
            False)
         return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent")

    def handle(self, handler_input):
        speech_text = "You can say burn 5 to 10 dollars!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Say burn x to y dollars", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
            and (handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent"
                 or handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent"))

    def handle(self, handler_input):
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Burn my money", speech_text))
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.object_type == "SessionEndedRequest"

    def handle(self, handler_input):
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
    BurnIntentHandler(),
    HelpIntentHandler(),
    CancelAndStopIntentHandler(),
    SessionEndedRequestHandler()])

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
