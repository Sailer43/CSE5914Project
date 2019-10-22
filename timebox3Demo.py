from assistant import send_input, add_example_to_intent
from Converter import Converter
from NLU import nlu
import webbrowser as wb
from nltk_functions import extract_keywords, find_keywords
from fetch_web import read_web
from sys import argv
import spotipy.util as util
from spotify_search import search
from json import loads, dumps
from profile_custom import Profiler

FOOD_URL = "https://www.yelp.com/search?find_desc={input}&find_loc=Columbus%2C+OH&ns=1"
MUSIC_URL = "https://open.spotify.com/search/{input}"
MOVIE_URL = "https://www.imdb.com/find?ref_=nv_sr_fn&q={input}&s=all"
WEATHER_URL = "https://weather.com/weather/tenday/l/Columbus+OH+USOH0212:1:US"

SP_SCOPE = "user-read-private"


def setup_spotify():
    with open("spotify.config", "r") as config_file:
        config_string = "\n".join(config_file.readlines())
    config = loads(config_string)
    if config["username"] == "":
        config["username"] = input("Please enter your Spotify username: ")
        with open("spotify.config", "w") as config_file:
            config_file.write(dumps(config))
    return util.prompt_for_user_token(config["username"],
                                      scope=SP_SCOPE,
                                      client_id=config["client_id"],
                                      client_secret=config["client_secret"],
                                      redirect_uri="https://open.spotify.com/browse/featured")


SP_TOKEN = setup_spotify()


def query_food(keywords: list):
    wb.open(FOOD_URL.format(input="+".join(keywords)))
    return


def query_music(keywords: list):
    if len(keywords) > 2:
        keywords = keywords[0:2]
    title, url = search("%20".join(keywords), SP_TOKEN)
    wb.open(url)
    return [title]


def query_movie(keywords: list):
    url = MOVIE_URL.format(input="+".join(keywords))
    keyword_list = extract_keywords("WORK_OF_ART", find_keywords(read_web(url)))
    wb.open(url)
    return keyword_list[1:5]


def query_weather(keywords: list):
    wb.open(WEATHER_URL)
    return


function_map = {"Ask_Recommendation_Movie": query_movie,
                "Ask_Recommendation_Music": query_music,
                "Ask_Recommendation_Restaurant": query_food,
                "Ask_Weather": query_weather}


def testing():
    converter = Converter()
    while True:
        intent = input("Please enter your intent: ")
        print("Start recording")
        converter.record()
        print("End recording")
        user_input = converter.listen()
        if user_input[0]:
            print('"{}"'.format(user_input[1]))
            print(add_example_to_intent(user_input[1], intent))
        else:
            print("s2t failed")


def refine_keywords(keyword_list, profile, THRESHOLD=0.7):
    result = []
    for keyword in keyword_list:
        entry = profile.get_keyword(keyword)
        relevance = entry["relevance"]
        sadness = entry["sadness"]
        joy = entry["joy"]
        fear = entry["fear"]
        disgust = entry["disgust"]
        anger = entry["anger"]
        if relevance >= THRESHOLD or max([sadness, joy, fear, disgust, anger]) > THRESHOLD:
            result.append(keyword)
    return result


def refine_entities(entity_list, profile, THRESHOLD=0.85):
    result = []
    for entity in entity_list:
        entry = profile.get_entity(entity)
        confidence = entry["confidence"]
        if confidence > THRESHOLD:
            result.append(entity)
    return result


def main():
    verbose = False
    profile = Profiler()
    if len(argv) > 1 and argv[1] == "-e":
        testing()
        return
    if len(argv) > 1 and argv[1] == "-v":
        verbose = True
    converter = Converter()
    while True:
        print("Start recording")
        converter.record()
        print("End recording")
        user_input = converter.listen()
        # testing
        # user_input = (True, "Could you play David Bowie's songs for me?")
        if user_input[0]:
            print('"{}"'.format(user_input[1]))
            try:
                text, action, intent = send_input(user_input[1])
            except IndexError:
                text = "I don't understand what you are saying."
                intent = None
            if intent in ["Ask_Recommendation_Movie",
                          "Ask_Recommendation_Music",
                          "Ask_Recommendation_Restaurant",
                          "Ask_Weather"]:
                try:
                    r = nlu(user_input[1])
                    keywords = [sub_r["text"] for sub_r in r["keywords"]]
                    entities = [sub_r["text"] for sub_r in r["entities"]]
                    if verbose:
                        print(keywords, entities)
                    profile.record(r["keywords"], r["entities"])
                    keywords = refine_keywords(keywords, profile)
                    entities = refine_entities(entities, profile)
                    keyword_list = list()
                    if len(entities) > 0:
                        for entity in entities:
                            keyword_list.extend([k for k in entity.split() if k not in ["HESITATION", "movie", "song"]])
                    else:
                        for keyword in keywords:
                            keyword_list.extend([k for k in keyword.split() if k not in ["HESITATION", "movie", "song"]])
                    if verbose:
                        print(keyword_list)
                    result = function_map[intent](keyword_list)
                    if result and result != [] and result != ["Not Found"] or intent != "Ask_Recommendation_Music":
                        text = str(text)
                        text = text.format(result=", ".join(result))
                    else:
                        text = "I cannot find any results, sorry."
                except Exception as e:
                    print(e)
                pass
            print(text)
            converter.text2speech(text)
            if intent == "General_Ending":
                break
            input()
        else:
            converter.text2speech(user_input[1])


if __name__ == '__main__':
    main()
