from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template import loader

from . import converter
from . import assistant
from . import helper
from . import NLU

converter_instant = converter.Converter()


def index(request: HttpRequest):
    if request.method == "GET":
        template = loader.get_template("advice/index.html")
        return HttpResponse(template.render(dict(), request))


def input_audio(request: HttpRequest):
    url = ""
    if request.method == "POST":
        input_audio = request.body
        status, input_text = converter_instant.listen(input_audio)
        if status:
            try:
                output_text, action, intent = assistant.send_input(input_text)
            except IndexError:
                output_text = "I don't understand what you are saying."
                intent = None
            if intent in ["Ask_Recommendation_Movie",
                          "Ask_Recommendation_Music",
                          "Ask_Recommendation_Restaurant",
                          "Ask_Weather"]:
                try:
                    r = NLU.nlu(input_text)
                    keywords = [sub_r["text"] for sub_r in r["keywords"]]
                    entities = [sub_r["text"] for sub_r in r["entities"]]
                    print(keywords, entities)
                    # profiling
                    # keywords = helper.refine_keywords(keywords, profile)
                    # entities = helper.refine_entities(entities, profile)
                    keyword_list = list()
                    if len(entities) > 0:
                        for entity in entities:
                            keyword_list.extend([k for k in entity.split() if k not in ["HESITATION", "movie", "song"]])
                    else:
                        for keyword in keywords:
                            keyword_list.extend([k for k in keyword.split() if k not in ["HESITATION", "movie", "song"]])
                    print(keyword_list)
                    result, url = helper.function_map[intent](keyword_list)
                    if result and result != [] and result != ["Not Found"] or intent != "Ask_Recommendation_Music":
                        output_text = str(output_text)
                        if result:
                            output_text = output_text.format(result=", ".join(result))
                    else:
                        output_text = "I cannot find any results, sorry."
                except Exception as e:
                    print("entered")
                    raise e
                pass
        else:
            output_text = input_text
        output_audio = converter_instant.read(output_text)
        output_audio = [e for e in output_audio]
        input_text = input_text.replace("%HESITATION", "(...)")
        return JsonResponse({"audio": output_audio,
                             "input_text": input_text,
                             "output_text": output_text,
                             "external_link": url})
