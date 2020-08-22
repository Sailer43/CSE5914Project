import spotipy.util as util
from . import spotify_search
from . import nltk_functions
from . import fetch_web
from json import loads

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
    return None, FOOD_URL.format(input="+".join(keywords))


def query_music(keywords: list):
    if len(keywords) > 2:
        keywords = keywords[0:2]
    title, url = spotify_search.search("%20".join(keywords), SP_TOKEN)
    return [title], url


def query_movie(keywords: list):
    url = MOVIE_URL.format(input="+".join(keywords))
    keyword_list = nltk_functions.extract_keywords("WORK_OF_ART", nltk_functions.find_keywords(fetch_web.read_web(url)))
    return keyword_list[1:5], url


def query_weather(keywords: list):
    return None, WEATHER_URL


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

