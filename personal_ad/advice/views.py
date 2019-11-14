from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader

from . import converter
from . import assistant

converter_instant = converter.Converter()


def index(request: HttpRequest):
    if request.method == "GET":
        template = loader.get_template("advice/index.html")
        return HttpResponse(template.render(dict(), request))


def input_audio(request: HttpRequest):
    if request.method == "POST":
        input_audio = request.body
        status, input_text = converter_instant.listen(input_audio)
        if status:
            try:
                output_text, action, intent = assistant.send_input(input_text)
            except IndexError:
                output_text = "I don't understand what you are saying."
                intent = None
        output_audio = converter_instant.read(output_text)
        output_audio = [e for e in output_audio]
        return JsonResponse({"audio": output_audio,
                             "input_text": input_text,
                             "output_text": output_text})