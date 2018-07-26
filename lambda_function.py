from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import SimpleCard

class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "HelloWorldIntent")

    def handle(self, handler_input):
        speech_text = "Hello World"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest"
    
    def handle(self, handler_input):
        handler_input.response_builder.speak(
            handler_input.request_envelope.request.intent.name)
        return handler_input.response


class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         return handler_input.request_envelope.request.object_type == "LaunchRequest"

     def handle(self, handler_input):
         speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

         handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
         return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
                and handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent")

    def handle(self, handler_input):
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (handler_input.request_envelope.request.object_type == "IntentRequest"
            and (handler_input.request_envelope.request.intent.name == "AMAZON.CancelIntent"
                 or handler_input.request_envelope.request.intent.name == "AMAZON.StopIntent"))

    def handle(self, handler_input):
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
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
    HelloWorldIntentHandler(),
    HelpIntentHandler(),
    CancelAndStopIntentHandler(),
    SessionEndedRequestHandler()])

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
